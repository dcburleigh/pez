
import re
from deldevdb.staffdb import StaffDB
from . import api

last_err = None
staff_dbh = None
staff_dbh = StaffDB()
help_pattern = re.compile('.*help.*', re.I)
whois_pattern = re.compile('who\s*is \s+ (\w+)', re.I | re.X )
lookup_pattern = re.compile('lookup\s+(name|userid|email)\s+([\@\w\.\']+)', re.I)
lookup_name_pattern = re.compile('lookup\s+name\s+(\w+)\s+(\w+)', re.I)
lookup_last_name_pattern = re.compile('lookup\s+last( name)?\s+(\w+)\s+(\w+)', re.I)

lookup_qname_pattern = re.compile('lookup\s+name\s+[\"\'](\w+)\s+(\w+)[\"\']', re.I)

show_pattern = re.compile('show\s+(user|managers|reports)\s*', re.I)
#show_for_pattern = re.compile('show\s+(user|managers|reports)(\s+for\s+(\w+))?')
show_for_pattern = re.compile('show\s+(user|managers|reports)\s+for\s+(\w+)', re.I)

split_pattern = re.compile("\n")
default_message = "I don't understand this message"

format_pattern = re.compile('format\s+(plain|name|text|email|md)')
max_len = 7439
break_limit = max_len - 200 # allow line of 200 characters

def pez_handler( msg ):
    if msg.from_me():
        # don't respond
        return resp

    #staff_dbh.user_row_format = 'email'
    resp = response_message(msg)
    print("r=%s last query:%s" % (resp, staff_dbh.sql ))
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
    #
    # api
    #
    text = ''
    nb = 0
    for line in resp.splitlines():
        if len(text) > break_limit:
            print("next batch, len=%d f=%s" % (len(text), staff_dbh.user_row_format) )
            nb += 1
            if staff_dbh.user_row_format == 'md':
                api.messages.create( roomId=room_id,  markdown=text)
            else:
                api.messages.create( roomId=room_id, text=text)

            #print(text)
            text = ''
        text += line + "\n"

    if staff_dbh.user_row_format == 'md':
        api.messages.create( roomId=room_id,  markdown=text)
    else:
        api.messages.create( roomId=room_id, text=text)

def response_message(msg):
    #sstaff_dbh.user_row_format = 'email'
    staff_dbh.user_row_format = 'name'
    result = format_pattern.search(msg.message_text)
    if result:
        staff_dbh.user_row_format = result.group(1)
        #print("format=%s" % staff_dbh.user_row_format)

    if help_pattern.search(msg.message_text):
        return help()

    result = whois_pattern.search(msg.message_text)
    if result:
        user_id = result.group(1)
        print("whois: %s " % user_id )
        if user_id == '007':
            return "Bond, James Bond"
        if user_id == 'number 2' or user_id == 'number2' or user_id == '2':
            return "You are number 6"
        if user_id == '1337':
            return "H@x05"
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
