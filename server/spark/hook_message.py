
from . import get_api, auth

class HookMessage():
    def __init__(self, msg):
        self.__dict__.update(msg)
        #self.id = msg['id']
        #self.name = msg['name']
        fields = [ 'name', 'resource', 'event']
        self.message_text = ''
        self.creator_name = ''
        self.creator_email = ''

        self.api = get_api()
        me = self.api.people.me()
        #print("me: %s" % me.displayName )
        self.my_id = me.id

    def show(self, format='simple' ):
        print("%s  (%s - %s)" % (self.name, self.resource, self.event ) )
        #print("data: message ID: %s " % (self.data.id ) )
        #print("data: message ID: %s " % (self.data['id'] ) )
        #print("data: message ID: {} ".format( self.data) )
        print("created by: %s - %s / id=%s" % ( self.creator_name, self.creator_email, self.createdBy ))
        print("Message: %s" % self.message_text)

    def get_creator(self):
        person = self.api.people.get( self.createdBy )
        self.creator_name = person.displayName
        self.creator_email = person.emails[0]

    def get_text(self):
        if self.test_message:
            self.message_text = self.test_message
            return

        msg = self.api.messages.get( self.data['id'])
        self.message_text = msg.text

    def from_me(self):
        return self.createdBy == self.my_id
        
    def check_org(self):
        return auth.check_org_id(self.orgId)
