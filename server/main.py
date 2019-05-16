"""
My example server

Flask application to provide RESTful interface for Something.

POST /hello
   TBD

GET /hello
   return a message

"""

from flask import Flask
from flask import request, abort, Response, send_from_directory
import json
#import sys
import re
import os
from auth import check_auth
from deldevdb.staffdb import StaffDB

app = Flask(__name__)
dbh = None
last_err = None
staff_dbh = None
staff_dbh = StaffDB()

@app.route("/")
def about(info=''):
    return "PezBot " + info


@app.errorhandler(401)
def not_authorized(error):
    info = {'error': 'not authorized'}
    info['auth-err'] = str(error)
    text = json.dumps( info, indent=4)
    return text, 401

@app.errorhandler(404)
def page_not_found(error):
    info = {'error': 'no such page'}
    info['path'] = request.path
    text = json.dumps( info, indent=4)
    return text, 404

@app.route("/test", methods=['GET', 'POST'])
def test():
    err = check_auth(request.headers)
    if err:
        abort(401, err)

    text = ''
    info  = { 'method': request.method}

    #print request.headers
    print("got here method={}".format( request.method))
    for item in ['Content-Length', 'User-Agent']:
        #info['header-' + item] = request.headers[item]
        info['header-' + item] = request.headers.get(item, '')

    n = staff_dbh.count()
    info['rows' ] = str(n)

    #info['headers'] = request.headers
    text = json.dumps( info, indent=4)
    return text

@app.route("/whois", methods=['GET', 'POST'])
def whois():
    info = {}

    err = check_auth(h=request.headers)
    if err:
        info['error'] = err
        return json.dumps( info, indent=4)
    if request.method == 'POST':

        #info['header'] = request.headers
        #print request.headers
        info['state'] = "got headers"
        #return json.dumps( info, indent=4)

        if not request.is_json:
            info['error'] = "not json"
            #abort(400)
            #abort( {'400': "not json"})
            return json.dumps( info, indent=4)
        try:
            obj = request.get_json()
        except Exception as err:
            #print err
            info['data_in'] = request.data
            info['error'] = "no json object" + str(err)
            return json.dumps( info, indent=4)

        if not obj:
            info['error'] = "no json object"
            return json.dumps( info, indent=4)

        staff_dbh.build_select_query( {'user_id': obj['user_id']})
        staff_dbh.open_query()
        row = staff_dbh.next_row()
        if not row:
            return "%s - no user found q=%s " % ( obj['user_id'], staff_dbh.sql)
        return format_row(row)

    return "Hello World! "

def format_row(row):
    text = ''
    if not row:
        return "No user found"
    text += "%s (%s)  - %s [ %s ]" % ( row['name'], row['user_id'], row['title'], row['department'])
    return text

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    text = ''
    info  = { 'method': request.method}

    err = check_auth(h=request.headers)
    if err:
        #abort(401, err)
        info['auth'] = 'failed'
        info['auth_err'] = err
    else:
        info['auth'] = 'OK'

    name = 'World'
    print("got here method={}".format( request.method))
    if request.method == 'POST':

        #info['header'] = request.headers
        #print request.headers
        info['state'] = "got headers"
        #return json.dumps( info, indent=4)

        if not request.is_json:
            info['error'] = "not json"
            #abort(400)
            #abort( {'400': "not json"})
            return json.dumps( info, indent=4)

        info['state'] = "is json"
        #return json.dumps( info, indent=4)

        #obj = request.get_json(silent=True)
        try:
            obj = request.get_json()
        except Exception as err:
            #print err
            info['data_in'] = request.data
            info['error'] = "no json object" + str(err)
            return json.dumps( info, indent=4)

        if not obj:
            info['error'] = "no json object"
            return json.dumps( info, indent=4)

        info['state'] = "got obj"
        # do stuff
        info['success'] = 'OK'
        if 'name' in obj:
            name = obj['name']

    elif request.method == 'GET':
        info['success'] = 'OK'
        info['q'] = str(request.query_string)

        if 'name' in request.args:
            name = request.args['name']
            pass

    info['message'] = 'Hello, %s!' % ( name )
    text = json.dumps( info, indent=4)
    return text

if __name__ == "__main__":
    app.run()
