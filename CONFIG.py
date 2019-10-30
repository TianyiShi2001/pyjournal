#/usr/bin/env python

from pathlib import Path
import dill
from AUTH import AUTHMETHODS
from getpass import getpass
import functools

#################### CUSTOMISABLE #####################
OUTDIR = str(Path.home()) + '/Downloads/'
CONFIGDIR = str(Path.home()) + '/Library/pyjournal/'
CREDENTIALSPATH = CONFIGDIR + 'CREDENTIALS'
COOKIEPATH = CONFIGDIR + 'cookies'
####################################################### 

def loginMaker(UNAME, PASSWD, UNI):
    @functools.wraps
    def wrapper(sel):
        AUTHMETHODS[UNI](sel, UNAME = UNAME, PASSWD = PASSWD)
    return wrapper

Path(OUTDIR).mkdir(parents=True, exist_ok=True)
Path(CONFIGDIR).mkdir(parents=True, exist_ok=True)

if not Path.exists(Path(CREDENTIALSPATH)): # First time configuration
    CREDENTIALS = [
        input('Username: '),
        getpass('Password: '),
        input('Library service provider/uni/institution full name: ')
    ]
    LOGIN = loginMaker(*CREDENTIALS)
    with open(CREDENTIALSPATH, 'wb') as f:
        dill.dump(LOGIN, f)

with open(CREDENTIALSPATH, 'rb') as f:
    LOGIN = dill.load(f)
