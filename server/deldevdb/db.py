"""
wrapper for database access

see: http://pymysql.readthedocs.io/en/latest/

Usage:
  from utils import db

  dbh = db.DB()
  dbh = db.DB(f='/path/to/config', t='TABLE')

  n = dbh.count()
  print("%s rows" % n)


"""

import pymysql.cursors
import sys
import os

from configparser import ConfigParser

class DB:
    #cfg_file = 'deldev_db.cfg'
    cfg_file = 'deldev_db.ini'
    cfg = None
    errors = []
    messages = []
    table_name = None
    colinfo = {}
    sql = None

    def __init__(self,f=None, t=None, columns=[]):

        self.dbh = None # the database connection
        self.sql = None

        self.current_cursor = None
        if t:
            self.table_name = t

        self.columns = columns

        self.read_config(f)

    def read_config(self,f=None):

        if not f:
            f = os.environ.get('DB_CONFIG_FILE')

        if f:
            self.cfg_file = f

        if not self.cfg_file:
            raise Exception('no config file')

        #print("read %s" % self.cfg_file )
        fh = open(self.cfg_file)
        if not fh:
            raise Exception("cannot open " + self.cfg_file)

        #print("read %s" % self.cfg_file)
        try:
            config = ConfigParser()
            config.read(self.cfg_file)
            self.cfg = config['client']
        except Exception as err:
            print("ERROR: config file {} failed: {}".format( self.cfg_file, err))
        return

    def open(self):
        #print("open connection to %s" % ( self.cfg.get('host')))
        if self.dbh:
            if self.dbh.open:
                #print('still open')
                return
        try:
            self.dbh = pymysql.connect(
                host=self.cfg.get('host', 'localhost'),
                user=self.cfg.get('user'),
                password=self.cfg.get('password'),
                port=self.cfg.get('port',3306),
                db=self.cfg.get('database', 'deldev'),
                #charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
                )
        except Exception as err:
            raise Exception("connect failed: {}".format(err) )
            return

    def close(self):
        if self.dbh:
            self.dbh.close()  # close the database connection

    def add_item(self, item ):
        #print "add item: p=", item['project']
        self.open()

        flist = ''
        vlist  = ''
        # calling program is responsible for making sure
        #  all values are of type 'string'
        for f in self.columns:
            if f in item:
                if item[f] == None:
                    continue

                if flist:
                    flist += ', '
                    vlist += ', '
                flist += "`"  + f + "`"
                vlist += "'" + item[f] + "'"

        #raise Exception("got here")
        if flist == '':
            raise Exception("no valid fields")
            #print "ERROR: no valid fields"
            #return

        sql =  "INSERT INTO `%s`  ( %s ) VALUES ( %s ) " % ( self.table_name, flist, vlist )

        #cursor = self.dbh.cursor( dictionary=True)
        cursor = self.dbh.cursor( )
        if not cursor:
            raise Exception('no cursor')
        cursor.execute(sql)
        #return
        self.dbh.commit()
        id = cursor.lastrowid
        self.close
        return id

    def build_select_query(self, data):
        q = ''
        wh = ''
        if not self.table_name:
            return

        for f in self.columns:
            if not f in data:
                continue
            if data[f] == None:
                continue

            if not wh == '':
                wh +=  ' AND '
            # TODO: sanitize data
            #   escape quotes
            # all values must be str
            neg = False
            op = None

            if data[f][0] == '!':
                neg = True
                data[f] = data[f][1:]

            if data[f] == 'NULL':
                op = 'IS'
                if neg:
                    op = 'IS NOT'
                wh += "%s %s NULL " % ( f, op )
                continue

            if data[f][0] == '<' or data[f][0] == '>':
                op = data[f][0]
                data[f] = data[f][1:]
            if f in self.colinfo and self.colinfo[f] == 'i':
                if not op:
                    op = '='
                    if neg:
                        op = '!='
                wh += '%s %s %s' % ( f, op, data[f ])
            else:
                if not op:
                    op = 'like'
                    if neg:
                        op = 'not like'
                wh += '%s %s "%s"' % ( f, op, data[f ])

        sql = 'select * from %s where %s ' % ( self.table_name, wh)

        self.sql = sql
        return sql

    def open_query(self, sql=None):
        """open cursor for a query"""
        #global current_cursor
        if sql:
            self.sql = sql

        self.open()
        if not self.dbh:
            print("no DB handle")
            return
        try:
            self.current_cursor = self.dbh.cursor()
            self.current_cursor.execute(self.sql)
        except Exception as err:
            #return "count failed: " + str(err)
            #??? self.close()
            # self.current_cursor = None
            print( "open failed: " + str(err))
            return

    def next_row(self, cur=None):
        if not cur:
            cur = self.current_cursor
        try:
            result = cur.fetchone()
            if not result:
                #self.close() # ????
                # close cursor
                # cur.close()
                return
            return result

        except Exception as err:
            self.close()
            print( "query failed: " + str(err))
            return

    def count_column(self, col):
        """ return the number of occurrences of the values
        in a specified column"""

        self.open()
        n = 0

        # set:
        #  columns, col_name, select_field
        if type(col) is list:
            #print "list", col
            for c in col:
                if not c in self.columns:
                    raise Exception("invalid column " + c)
                    return
            fields = ', '.join(col)
            col_name =  '_'.join(col)

            x = '," ",'.join( col )
            select_field = 'concat(' + x + ') as ' + col_name


        else:
            ###print col,"type", type(col)
            if not col in self.columns:
                raise Exception("invalid column " + col)
                return
            fields = col
            select_field = col
            col_name = col

        sql =  "select count(*) as num, %s from %s group by %s order by count(*) DESC " % ( select_field, self.table_name, fields )

        clist = []
        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            while True:
                result = cursor.fetchone()
                if not result:
                    # self.close # ???
                    break
                n += 1
                #print("{} r={}".format( n, result ))

                clist.append( { 'name': result[col_name], 'count': result['num']})
        except Exception as err:
            #return "count failed: " + str(err)
            self.close()
            print( "count failed: " + str(err))
            return

        return clist

    def count(self, args=None):
        self.open()
        n = 0
        sql = "select count(*) as num from %s " % self.table_name
        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            # self.close()
            #print "got results, type", type(result)
        except Exception as err:
            return( "count failed: " + str(err))

        return result['num']
