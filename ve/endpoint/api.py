
import requests
from requests.auth import HTTPBasicAuth

from configparser import ConfigParser

from . import cfg

auth = None

objects = [ 'Audio', 'Bookings', 'Call', 'CallHistory', 'Camera', 'Cameras', 'Conference'
, 'Diagnostics', 'Dial', 'GPIO', 'HttpFeedback', 'Macros', 'Message', 'Peripherals', 'Phonebook', 'Presentation']

def init(cfg_file):
    global cfg, auth
    #read_server_config( cfg_file )
    config = ConfigParser()
    config.read(cfg_file)
    #print("got cfg={}".format( config.sections() ))
    cfg  = config['server']
    #print("ip=%s" % ( cfg['ip']))
    auth=HTTPBasicAuth( cfg['username'], cfg['password'] )

def post(data):

    url = "http://%s/putxml" % (  cfg['ip'] )
    print("post url=%s data=%s" % (url, data ))
    r = requests.post(url, verify=False, auth=auth, data=data)

    if not r.status_code == 200:
        print("get failed (%d) - result=%s" % (r.status_code, r.text ))
        return
    return r.text

def command(path):
    post( '/Command' + path)

def dial(number):
    #path = '/Command/Dial/Number/%s' % number;
    xml = '<Command><Dial><Number>%s</Number></Dial></Command>' % number
    post(xml)

def get(path):
    ###print('cfg={}'.format(cfg))
    url = "http://%s/getxml?%s" % (  cfg['ip'], path  )
    print("get url=%s" % url )
    r = requests.get(url, verify=False, auth=auth)
    #print("got={}".format(r))
    if not r.status_code == 200:
        print("get failed")
        return
    return r.text

def set_ultrasound( vol ):
    xml = '''
<Configuration>
       <Audio>
         <Ultrasound><MaxVolume>%s</MaxVolume></Ultrasound>
     </Audio>
    </Configuration>''' % vol
    post(xml)

def set_config_message( message ):
    xml = '''
<Configuration>
       <UserInterface>
         <CustomMessage>%s</CustomMessage>
     </UserInterface>
    </Configuration>''' % message
    post(xml)

def config1(n=1):
    path = 'location=/Configuration'
    path = 'location=/Configuration/Audio'
    #path = 'location=/Configuration/Cameras'
    #path = 'location=/Configuration/Conference'
    #path = 'location=/Configuration/Macros'
    #path = 'location=/Configuration/Network'
    #path = 'location=/Configuration/NetworkPort'
    #path = 'location=/Configuration/NetworkServices'
    #path = 'location=/Configuration/UserInterface'
    #path = 'location=/Configuration/UserManagement'
    #path = 'location=/Configuration/Video'
    #path = 'location=/Configuration/Video/Input/Connector'
    #path = 'location=/Configuration/Video/Input/Connector' + '&item=1'

    return get(path)


def cameras(n=1):
    path = 'location=/Status/Cameras'
    path = 'location=/Status/Cameras/Camera/%d' % n

    path = 'location=/Status/Cameras/Camera'
    path = 'location=/Status/Cameras/Camera/1'

    return get(path)

def http_feedback():
    path = 'location=/Status/HttpFeedback'
    return get(path)

def network_status():
    path = 'location=/Status/Network'
    path = 'location=/Status/NetworkServices'
    return get(path)

def status1():
    path = 'location=/Status/Audio/Devices/HeadsetUSB/ConnectionStatus'
    path = 'location=/Status/Audio/Devices/HeadsetUSB/Description'

    path = 'location=/Status/Audio/Devices/HeadsetUSB/Manufacturer'
    path = 'location=/Status/Audio'
    path = 'location=/Status/Audio/Input'
    path = 'location=/Status/Audio/Output'
    path = 'location=/Status/Audio/SelectedDevice'

    path = 'location=/Status/Capabilities'
    path = 'location=/Status/Conference'
    path = 'location=/Status/Diagnostics'
    path = 'location=/Status/MediaChannels'
    path = 'location=/Status/Peripherals'
    path = 'location=/Status/Provisioning'
    path = 'location=/Status/Proximity'
    path = 'location=/Status/Security'
    path = 'location=/Status/SIP'
    path = 'location=/Status/SystemUnit'
    path = 'location=/Status/Time'
    path = 'location=/Status/UserInterface'
    path = 'location=/Status/Video'

    return get(path)


def get_status_standby():
    path = 'location=/Status/Standby'
    return get(path)
