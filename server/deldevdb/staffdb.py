""" DelDev Staff table """

from .db import DB

class StaffDB(DB):

    def __init__(self, f=None):

        super().__init__()

        self.user_row_format = 'text';

        self.wildcard = True
        self.include_inactive = False
        self.include_all = True
        self.max_level = 20
        self.table_name = 'staff'

        self.columns = ['user_id', 'name', 'email', 'title', 'manager_user_id']
        #self.read_config(f)

    def get_user(self, user_id):
        self.build_select_query( {'user_id': user_id })
        self.open_query()
        return self.next_row()

    def whois(self, user_id):
        self.build_select_query( {'user_id': user_id })
        self.open_query()
        row = self.next_row()
        return self.format_user_row(row)

    def lookup_email(self, email):
        self.build_select_query( {'email': email })

        text = self.lookup_results()
        if not text == '':
            return text

        self.sql = "select staff.* from staff join staff_email as se on se.fkstaff = staff.id and se.email = '%s' " % email
        text =  self.lookup_results()
        if text == '':
            return "No matches found "
        return text

    def lookup_results(self):
        self.open_query()
        a = []
        n = 0
        na = 0
        text = ''
        while True:
            row =  self.next_row()
            if not row:
                break

            n += 1
            if row['active'] == 1:
                na += 1
            elif not self.include_inactive:
                continue
            text += self.format_user_row(row)
            text += "\n"

        return text

    def lookup_name(self, name):
        self.build_select_query( {'name': name })

        self.open_query()
        a = []
        n = 0
        text = ''
        while True:
            row =  self.next_row()
            if not row:
                break
            n += 1
            text += self.format_user_row(row)
            text += "\n"

            if row['active'] == 1:
                a.append(row)

        if n == 0:
            print("q=%s" % self.sql )
            return "No names match"

        if n > 1:
            ###print("%d matches " % n)
            # try active
            if len(a) > 0:
                text = ''
                for row in a:
                    text += self.format_user_row(row)
                    text += "\n"

                return text
            #print("no active matches")

        return text

    def list_managers(self,user_id_in, format='text'):
        text = '';
        user_id = user_id_in
        n = 0
        lines = []
        while True:
            n += 1
            ###print("u=%s" % user_id)
            row = self.get_user(user_id)
            if not row:
                text = "No match on %s\n%s" % ( user_id, text)
                break

            #print('row={}'.format(row))
            lines.append(  self.format_user_row(row) )
            if not text == '':
                text = "\n" + text
            text = self.format_user_row(row) + text
            if not row['manager_user_id'] or user_id == row['manager_user_id']:
                text = "...." + text
                break

            user_id = row['manager_user_id']

            if n > 20:
                break # sanity check

        l = 0
        text = ''
        lines.reverse()
        for line in lines:
            text += '. ' * l
            text += line + "\n"
            l += 1

        return text


    def _list_reports(self, manager_user_id, l=0):
        self.build_select_query( {'manager_user_id': manager_user_id })

        #print("r: q=%s" % self.sql)
        self.open_query()
        cur = self.current_cursor # need separate cursor for each level

        text = ''
        nr = 0
        if l > self.max_level:
            #print("got max level=%s" % l)
            return text
        while True:
            row = self.next_row(cur)
            if not row:
                #print("%d no more" % l)
                break
            if not self.include_inactive and row['active'] == 0:
                #print("%s skip inactive" % row['user_id'])
                continue

            nr += 1
            text +=  '. ' * l
            text += self.format_user_row(row)
            text += "\n"
            ###print("%d t=%s" % (nr, text))
            # TODO: get sub-reports
            text += self._list_reports( row['user_id'], l+1)

            ###print("%d t=%s" % (nr, text))
            if nr > 500:
                print("%s: quitting at %d reports" % (manager_user_id, nr))
                break

        #print("%d reports, l=%d" % ( nr, l))
        return text

    def list_reports(self, user_id):
        text = ''
        n = 0
        row = self.get_user(user_id)
        #print("start q=" + self.sql)
        if not row:
            text += "No match on %s\n%s" % ( user_id, text)
            return text

        text = self._list_reports( user_id, 1)
        if text == '':
            text = "No reports found "
        text = self.format_user_row(row) + "\n" + text
        #text += self._list_reports( user_id, 1)
        return text

    def format_user_row(self, row):
        text = ''
        if not row:
            return "No user found"

        aflag = ''
        if row['active'] == 0:
            aflag += "X "

        if self.user_row_format == 'text':
            text += "%s%s (%s)  - %s [ %s ]" % ( aflag, row['name'], row['user_id'], row['title'], row['department'])
        elif self.user_row_format == 'email':
            text += "%s%s (%s) - %s  - %s [ %s ]" % ( aflag, row['name'], row['user_id'], row['email'], row['title'], row['department'])
        elif self.user_row_format == 'md':
            text += "%s[%s|mailto:%s] (%s) _%s_ [ %s ]" % ( aflag, row['name'], row['user_id'], row['email'], row['title'], row['department'])
        else:
            text = row['name']

        return text
