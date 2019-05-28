#import os
import re

from . import org_id, auth_token_pattern,  auth_token, auth_token_admin

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
