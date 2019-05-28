
import re
from deldevdb.staffdb import StaffDB
from . import api

last_err = None
staff_dbh = None
staff_dbh = StaffDB()
help_pattern = re.compile('.*help.*')
whois_pattern = re.compile('whois (\w+)\s*')
lookup_pattern = re.compile('lookup\s+(name|userid|email)\s+([\@\w\.\']+)')
lookup_name_pattern = re.compile('lookup\s+name\s+(\w+)\s+(\w+)')

show_pattern = re.compile('show\s+(user|managers|reports)\s*')
#show_for_pattern = re.compile('show\s+(user|managers|reports)(\s+for\s+(\w+))?')
show_for_pattern = re.compile('show\s+(user|managers|reports)\s+for\s+(\w+)')

default_message = "I don't understand this message"

def pez_handler( msg ):
    resp = response_message(msg)

    if msg.from_me():
        # don't respond
        return resp

    print("message from: %s " % msg.creator_name )
    post_response(msg, resp)

    return resp

def post_response(msg, resp):
    test_room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vYmFjMmZiYjAtODE3OC0xMWU5LWI3YjUtOWQ3OTkxODQwZTdj'  # PezTest

    # TODO: format as markdown
    api.messages.create( roomId=test_room_id, text=resp)

def response_message(msg):
    if help_pattern.search(msg.message_text):
        return help()

    result = whois_pattern.search(msg.message_text)
    if result:
        user_id = result.group(1)
        print("whois: %s" % user_id)
        return staff_dbh.whois(user_id)

    result = lookup_name_pattern.search(msg.message_text)
    if result:
        type = 'name'
        value = result.group(1) + ' ' + result.group(2)

        #print("n=%s n4=%s" % ( result.groups(3), result.groups(4)))
        #return staff_dbh.whois(user_id)
        return lookup(type, value)

    result = lookup_pattern.search(msg.message_text)
    if result:
        type = result.group(1)
        value = result.group(2)
        return lookup(type, value)

    result = show_for_pattern.search(msg.message_text)
    if result:
        type = result.group(1)
        user_id = None
        user_id = result.group(2)
        # user_id = cache.get(key=msg.createdBy, 'user_id')
        if not user_id:
            #return "No user selected"
            user_id = '2474'
            user_id = 'toddpet'
            user_id =  '2164'
            user_id = '2311'

        return user_details(user_id, type)

    return default_message + help()

def help():
    return '''
Staff Directory Bot

Supported ommands
   whois <userid>

   lookup name <name>

   lookup email <email>

   show managers for <userid>

   show reports for <userid>
   '''


def lookup(type, value):
    print("lookup (%s): '%s' " % (type, value))
    if type == 'userid':
        return staff_dbh.whois( value )

    if type == 'email':
        return staff_dbh.lookup_email(value)

    if type == 'name':
        value += '%'
        return staff_dbh.lookup_name(value)

def user_details(user_id, type):
    print("details (%s): '%s' " % (type, user_id))
    if type == 'managers':
        return staff_dbh.list_managers(user_id)

    if type == 'reports':
        return staff_dbh.list_reports(user_id)

    return default_message
