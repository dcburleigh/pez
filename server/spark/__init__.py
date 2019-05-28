""" Usage:
  from spark import get_api, auth_token, webex_teams_access_token, org_id

"""
import os
import re
from webexteamssdk import WebexTeamsAPI

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

def get_api():
    #global api
    return WebexTeamsAPI(access_token=webex_teams_access_token )
