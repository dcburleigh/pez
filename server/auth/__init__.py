import os
import re
from webexteamssdk import WebexTeamsAPI

# NOT USED

auth_token = None
auth_token_admin = None
webex_teams_access_token = None  # bot
org_id = None

t = os.environ.get('ORG_ID')
if t:
    org_id = t

t = os.environ.get('PEZ_AUTH_TOKEN')
if t:
    auth_token = t
    auth_token_admin = t

t = os.environ.get('PEZ_ADMIN_AUTH_TOKEN')
if t:
    ###print "got token", t
    auth_token_admin = t

auth_token_pattern = re.compile('^Bearer (\w+)$')

api = None
t = os.environ.get('WXT_ACCESS_TOKEN')
if t:
    webex_teams_access_token = t
    api = WebexTeamsAPI(access_token=webex_teams_access_token )

def check_org_id(org_id_in):
    if not org_id:
        print("no ORG ")
        return False

    if org_id == org_id_in:
        return True
    else:
        print("%s <> %s" % ( org_id, org_id_in))
        return False

def check_auth(h=None, token=None):

    if not token:
        token = auth_token

    b = h.get('Authorization','')
    if b == '':
        return 'no auth'
    m = auth_token_pattern.match(b)
    if not m:
        return 'no match on ' + b

    t = m.group(1)
    if not t:
        return 'no match; ' + b
    #print "check", token
    if t == token:
        return

    #return "invalid token " + m.group(1) + " t=" + token
    return "invalid token " + m.group(1)

def admin_auth():
    return check_auth(auth_token_admin)
