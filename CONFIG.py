#/usr/bin/env python

from pathlib import Path
import dill, yaml
from getpass import getpass
import functools
from os.path import expanduser


for k, v in yaml.full_load(open('_config.yaml')).items():
    if isinstance(v, str) and v[0] == '~':
        locals().update({k:expanduser(v)})
    else:
        locals().update({k:v})

for dir in [OUTDIR, CONFIGDIR, DESTDIR]:
    Path(dir).mkdir(parents=True, exist_ok=True)

KEYPATH = CONFIGDIR + 'KEY'
COOKIEPATH = CONFIGDIR + 'cookies'

if not Path.exists(Path(KEYPATH)): # First time configuration
    from AUTH import AUTH
    def loginMaker(UNAME, PASSWD, UNI):
        @functools.wraps
        def wrapper(*args, **kwargs):
            AUTH[UNI][1](UNAME = UNAME, PASSWD = PASSWD, *args, **kwargs)
        return wrapper
    CREDENTIALS = [
        input('Username: '),
        getpass('Password: '),
        input('Library service provider/uni/institution full name: ')
    ]
    KEY = [CREDENTIALS[2], AUTH[CREDENTIALS[2]][0], loginMaker(*CREDENTIALS)]
    with open(KEYPATH, 'wb') as f:
        dill.dump(KEY, f)

with open(KEYPATH, 'rb') as f:
    UNI, AUTHTYPE, LOGIN = dill.load(f)
