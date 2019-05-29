
from . import get_api, auth

class HookMessage():
    def __init__(self, msg):
        self.test_message = None
        self.__dict__.update(msg)
        #self.id = msg['id']
        #self.name = msg['name']
        fields = [ 'name', 'resource', 'event']
        self.message_text = ''
        self.creator_name = ''
        self.creator_email = ''
        self.author_name = ''
        self.author_email = ''

        self.api = get_api()
        me = self.api.people.me()
        #print("me: %s" % me.displayName )
        self.my_id = me.id

    def show(self, format='simple' ):
        print("%s  (%s - %s)" % (self.name, self.resource, self.event ) )
        #print("data: message ID: %s " % (self.data.id ) )
        #print("data: message ID: %s " % (self.data['id'] ) )
        #print("data: message ID: {} ".format( self.data) )
        print("hook created by: %s - %s / id=%s" % ( self.creator_name, self.creator_email, self.createdBy ))
        print("message author: %s (%s) " % ( self.author_name, self.author_email))
        print("Message: %s" % self.message_text)

    def get_creator(self):
        person = self.api.people.get( self.createdBy )
        self.creator_name = person.displayName
        self.creator_email = person.emails[0]

        person = self.api.people.get( self.data['personId'] )
        self.author_name = person.displayName
        self.author_email = self.data['personEmail']

    def get_text(self):
        try:
            if self.test_message:
                self.message_text = self.test_message
                return
        except Exception as err:
            pass

        msg = self.api.messages.get( self.data['id'] )
        self.message_text = msg.text

    def from_me(self):
        return self.data['personId'] == self.my_id
        #return self.createdBy == self.my_id

    def check_org(self):
        return auth.check_org_id(self.orgId)
