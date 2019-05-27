import sys

import argparse
from endpoint import api
#import endpoint

def set_config():
    logo = "Get IT"
    s = api.set_config_message( logo )

def set_ultrasound(v=10):
    r = api.set_ultrasound(v)
    print("got r=%s" % r)

def show_status():
    #s = api.get_status_standby()
    s = api.status1()
    #s = api.network_status()
    #s = api.http_feedback()

    #s = api.cameras()
    print("status=%s" % (s))

def test_dial(number='roomkit@sparkdemos.com'):
    api.dial(number)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="config file")

    parser.add_argument("-s", "--status", help="show status", action="store_true")
    parser.add_argument( "--config", help="show device configuration", action="store_true")
    parser.add_argument("-s", "--status", help="show status", action="store_true")
    parser.add_argument("-u", "--ultrasounce", "--ultrasounc", help="set ultrasounce max volume", action="store_true")

    parser.add_argument( "--dial", help="dial this number")
    parser.add_argument( "--logo", help="set logo on device")

    args = parser.parse_args()

    f = 've.cfg'
    if args.c:
        f = args.c
    api.init(f)

    if args.config:
        s = api.config1()
        print("config=%s" % (s)))

    if args.status:
        show_status()
    if args.ultrasound:
        set_ultrasound()
    if args.dial:
        api.dial(args.dial)
    if args.logo:
        #logo = "Get IT"
        s = api.set_config_message( args.logo )

if __name__ == '__main__':
    sys.exit(main())
