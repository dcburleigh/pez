
#import os
import re
import sys
import json
import argparse
from pathlib import Path
from deldevdb.staffdb import StaffDB
from spark.hook_message import HookMessage
#from spark.hook_handler import pez_handler
from spark import hook_handler

staff_dbh = None
help_pattern = re.compile('[^\S]*help[^\S]*')
whois_pattern = re.compile('[^\S]*whois (\w+)[^\S]*')

def get_dbh():
    global staff_dbh
    if not staff_dbh:
        staff_dbh = StaffDB()
    return staff_dbh

def test_hook(f = 'hook_message.json'):
    hfile = Path(f)
    if not hfile.exists():
        raise Exception("No such file %s" % f)

    with hfile.open() as fh:
        text = fh.read()

    #print("got h=%s" % text)
    info = json.loads( text )
    msg = HookMessage( info )
    msg.get_creator()
    msg.get_text()
    #print("process: %s" % msg.test_message)
    #print("process: %s" % msg.message_text)
    if not msg.check_org():
        print("INVALID ORG")
        return

    #print( pez_handler( msg ))
    #print( hook_handler.pez_handler( msg ))
    print( hook_handler.response_message( msg ))

def show_hook(f = 'hook_message.json'):
    hfile = Path(f)
    if not hfile.exists():
        raise Exception("No such file %s" % f)

    with hfile.open() as fh:
        text = fh.read()

    #print("got h=%s" % text)
    info = json.loads( text )

    msg = HookMessage( info )
    if msg.check_org():
        print("OK")
    else:
        print("INVALID ORG")

    msg.get_creator()
    msg.get_text()
    msg.show()

def show_db():
    staff_dbh = get_dbh()
    n = staff_dbh.count()
    print("%d rows in %s " % ( n, staff_dbh.table_name) )

    staff_dbh.build_select_query( { 'user_id': '2474'}  )
    print("q=%s" % staff_dbh.sql )

    staff_dbh.open_query()
    row = staff_dbh.next_row()

    if row:
        print("got: {}".format(row)  )
    else:
        print("no match")

def main():
	#show_db()
	#show_hook()
    parser = argparse.ArgumentParser()
    parser.add_argument("--hook", help="read and parse a webhook file, and post" )
    args = parser.parse_args()

    if args.hook:
        test_hook(args.hook)

if __name__ == "__main__":
    sys.exit(main())
