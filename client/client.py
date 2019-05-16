"""
client.py - client for the AppUsage REST application

Usage:

    client.py  <actions> <options>

Actions:

  --hello

  call hello world endpoint

Options:


Authorization:

You can specify the authorization token either by setting the environment variable

   export PEZ_AUTH_TOKEN=MyToken
   python client.py

or on the command line

    python client.py --token MyToken


"""

import sys
import requests
import json
import datetime
import os
import argparse

#
# http://docs.python-requests.org/en/master/
#

server = 'host'
server = 'prod'
#server = 'bot'
host = None
show_json = False
token = None

name = None
userid = None
email = None

def init():
    global host, token, admin_token

    if not token:
        t = os.environ.get('PEZ_AUTH_TOKEN')
        if t:
            token = t
            admin_token = t
        else:
            raise Exception('NO token specified')

    t = os.environ.get('PEZ_ADMIN_AUTH_TOKEN')
    if t:
        ###print( "token", t )
        admin_token = t
    #print( "using token ", token, admin_token )

    if server == 'host':
        #host = 'http://localhost:5000'
        pass # not supported
    elif server == 'local':
        host = 'http://localhost:8020'
    elif server == 'bot' or server == 'ace':
        host = 'http://deldev.ucalpha.com:8020'
    elif server == 'prod':
        host = 'https://deldev.ucalpha.com/pez'
    else:
        host = 'http://deldev.ucalpha.com:8020'


def get_headers( admin=False ):
    headers = None
    headers = {'Content-Type': 'application/json'}
    if admin:
        headers['Authorization'] = 'Bearer ' + admin_token
    else:
        headers['Authorization'] = 'Bearer ' + token

    return headers

def hello():
    headers = get_headers()
    url = host + '/hello'
    data = { 'name': 'John Doe'}

    print("get: %s" % url)
    #r = requests.get( url, headers=headers)
    r = requests.get( url, headers=headers, params=data)
    if r.status_code == 200:
        #print( "OK" )
        print("got text:{}".format(r.text) )
    else:
        print( "url %s failed (%s) \n%s" % (url, r.status_code, r.text) )


def test():
    headers = get_headers()
    url = host + '/test'
    data = { 'name': 'John Doe'}

    print("get: %s" % url)
    r = requests.get( url, headers=headers, params=data)
    if r.status_code == 200:
        print("success - got text:{}".format(r.text) )
    else:
        print( "url %s failed (%s) \n%s" % (url, r.status_code, r.text) )

def post_hello():
    headers = get_headers()
    url = host + '/hello'
    #url = host + '/testxxx'
    #data = { 'project': 'VTI-Phone-Home', 'application': 'pho', 'user': user, 'details': details}
    data = { 'name': 'John Doe'}

    print("get: %s" % url)
    r = requests.post( url, headers=headers, json=data)
    if r.status_code == 200:
        #print( "OK" )
        print("got text:{}".format(r.text) )
    else:
        print( "url %s failed (%s) \n%s" % (url, r.status_code, r.text) )

def post(path, data):
    headers = get_headers()

    url = host + path
    print("get: %s" % url)
    r = requests.post( url, headers=headers, json=data)
    if r.status_code == 200:
        #print( "OK" )
        print("got text:{}".format(r.text) )
        return r.text
    else:
        print( "url %s failed (%s) \n%s" % (url, r.status_code, r.text) )

def whois(user_id):
    t = post('/whois', {'user_id': user_id})

def main():
    action = None
    global server, token, show_json
    global name, userid, email


    parser = argparse.ArgumentParser()

    # actions
    parser.add_argument("--hello", help="test access", action='store_true' )
    parser.add_argument("--test", help="test access", action='store_true' )

    parser.add_argument("--whois", help="show user", action='store_true' )
    parser.add_argument("--lookup", help="find a user", action='store_true' )
    parser.add_argument("--reports", help="show users reporting to current user ",  action='store_true' )
    parser.add_argument("--reportsto", help="show hierarchy of current user",  action='store_true' )

    parser.add_argument("--name", help="full or partial name" )
    parser.add_argument("--email" )
    parser.add_argument("--userid", help="AD User ID (sAMAccountName)" )

    parser.add_argument("--server", help="server type: one of bot, host, local " )

    args = parser.parse_args()
    if args.server:
        server = args.server
    init()


    print("s=%s" % server)

    if args.name:
        name = args.name
    if args.email:
        email = args.email
    if args.userid:
        userid = args.userid

    if args.whois:
        whois( args.userid )
    elif args.lookup:
        lookup()
    elif args.reports:
        show_reports()
    elif args.reportsto:
        show_reports_to()
    elif args.hello:
        hello()
    elif args.test:
        test()
    else:
        raise Exception("invalid action")

    return 0

if __name__ == "__main__":
    sys.exit(main())
