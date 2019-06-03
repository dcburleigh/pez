
import re
from deldevdb.staffdb import StaffDB
from . import api

last_err = None
staff_dbh = None
staff_dbh = StaffDB()
help_pattern = re.compile('.*help.*', re.I)
whois_pattern = re.compile('whois (\w+)\s*', re.I)
lookup_pattern = re.compile('lookup\s+(name|userid|email)\s+([\@\w\.\']+)', re.I)
lookup_name_pattern = re.compile('lookup\s+name\s+(\w+)\s+(\w+)', re.I)
lookup_last_name_pattern = re.compile('lookup\s+last( name)?\s+(\w+)\s+(\w+)', re.I)

lookup_qname_pattern = re.compile('lookup\s+name\s+[\"\'](\w+)\s+(\w+)[\"\']', re.I)

show_pattern = re.compile('show\s+(user|managers|reports)\s*', re.I)
#show_for_pattern = re.compile('show\s+(user|managers|reports)(\s+for\s+(\w+))?')
show_for_pattern = re.compile('show\s+(user|managers|reports)\s+for\s+(\w+)', re.I)

split_pattern = re.compile("\n")
default_message = "I don't understand this message"

max_len = 7439
break_limit = max_len - 200 # allow line of 200 characters

def pez_handler( msg ):
    if msg.from_me():
        # don't respond
        return resp

    staff_dbh.user_row_format = 'email'
    resp = response_message(msg)
    print("last query:%s" % staff_dbh.sql )
    #print("message from: %s " % msg.creator_name )
    try:
        post_response(msg, resp)
    except Exception as err:
        pass
        return "error"
    return resp

def post_response(msg, resp):
    # ?
    # direct room:
    room_id = msg.data['roomId']
    #print("room=%s response length=%d" % ( room_id, len(resp) ))
    # Unable to post message to room:
    # Message length limited to 7439 characters before encryption
    # and 10000 characters after encryption.
    # TODO: format as markdown
    text = ''
    nb = 0
    for line in resp.splitlines():
        if len(text) > break_limit:
            print("next batch, len=%d" % len(text) )
            nb += 1
            api.messages.create( roomId=room_id, text=text)
            #print(text)
            text = ''
        text += line + "\n"

    api.messages.create( roomId=room_id, text=text)

def response_message(msg):
    staff_dbh.user_row_format = 'email'
    if help_pattern.search(msg.message_text):
        return help()

    result = whois_pattern.search(msg.message_text)
    if result:
        user_id = result.group(1)
        #print("whois: %s" % user_id)
        return staff_dbh.whois(user_id)

    result = lookup_qname_pattern.search(msg.message_text)
    if result:
        type = 'name'
        value = result.group(1) + ' ' + result.group(2)
        return lookup(type, value)

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
            return "No user selected"

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
        n = value.find('@')
        if n == -1:
            value += '@%'
        return staff_dbh.lookup_email(value)

    if type == 'name':
        value += '%'
        #print("lookup (%s): '%s' " % (type, value))
        return staff_dbh.lookup_name(value)

def user_details(user_id, type):
    #print("details (%s): '%s' " % (type, user_id))
    if type == 'managers':
        return staff_dbh.list_managers(user_id)

    if type == 'reports':
        return staff_dbh.list_reports(user_id)

    return default_message
