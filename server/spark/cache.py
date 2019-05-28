
from pathlib import Path
from datetime import datetime, timedelta

exp_days = 2
exp_hours = 5
cache_file = 'cache.json'
CF = Path(cache_file)

data = {}

def read():
    global data
    if not CF.exists():
        data = {}

    text = ''
    with open(CF) as fh:
        text = fh.read()
    data = json.loads( text )
    delete_expired() 

def delete_expired():
    now = datetime.now()
    d_str = str( now )
    for key in data.keys():
        if  now > data[key]['exp_date']:
            del data[ key ]


def write():

    text = json.dumps( data )
    with open(CF,'w') as fh:
        fh.write( text )

def add(key, info):
    global data

    exp =
