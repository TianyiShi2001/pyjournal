import pickle
import os
import sys
import time
from CONFIG import OUTDIR, COOKIEPATH
from functools import wraps
import logging


LOGGING_LEVEL = 'INFO'
LOGGING_FORMAT = '%(name)s: % (levelname)s: % (message)s'


def mkLogger(ss, es):
    def logger(func, ss=ss, es=es):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(ss)
            func(*args, **kwargs)
            print(es)
        return wrapper
    return logger


def mkLogger_download(type):
    ss = f'Downloading {type} to{OUTDIR}...'
    es = f'{type} downloaded.'
    return mkLogger(ss, es)


risLogger = mkLogger_download('ris')
pdfLogger = mkLogger_download('pdf')
risAndPdfLogger = mkLogger_download('ris and pdf')


class JOURNAL(object):

    name = 'null'

    def __init__(self, url, self.authMethod):
        self.__routine(url, self.authMethod)

    def __routine(self, url, self.authMethod):
        self.logger = self.__initLogger()
        self.url = url
        self.authMethod = self.authMethod

    def __initLogger(self):
        logger = logging.getLogger(self.name)
        try:
            logger.setLevel(int(LOGGING_LEVEL))
        except ValueError:
            logger.setLevel(getattr(logging, LOGGING_LEVEL.upper()))
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setFormatter(logging.Formatter(LOGGING_FORMAT))
        logger.addHandler(stdoutHandler)
        return logger

    def _for_requests(self, seleniumCookies):
        return {item["name"]: item["value"] for item in seleniumCookies}

    def _cookies_get(self):
        pass  # Defined in subclasses

    def _cookies_read(self):
        return pickle.load(open(COOKIEPATH, 'rb'))

    def _cookies_write(self, newCookies):
        self.logger.info(f'Writing cookies to cookies[{self.name}][{self.authMethod}]...')
        self.logger.debug(repr(newCookies))
        if os.path.exists(COOKIEPATH):
            cookies = self._cookies_read()
        else:
            cookies = {}
        if not cookies.get(self.name):
            cookies[self.name] = {}
        cookies[self.name]self.authMethod]= newCookies
        with open(COOKIEPATH, 'wb') as f:
            pickle.dump(cookies, f)

    def _cookies_retrieve(self):
        try:
            print('Trying to read cookies from' + COOKIEPATH)
            return self._cookies_read()[self.name]self.authMethod]
        except KeyError:
            return self._cookies_get()

    def _pdf_write(self, content):
        with open(OUTDIR + self.name + '.pdf', 'wb') as f:
            f.write(content)
