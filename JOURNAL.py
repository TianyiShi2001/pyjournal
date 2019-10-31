import pickle, os, time
from CONFIG import OUTDIR, COOKIEPATH
import functools


def _for_requests(seleniumCookies):
    return {item["name"]:item["value"] for item in seleniumCookies}

def mkPrinter(ss, es):
    @functools.wraps
    def printer(func, ss = ss, es = es):
        @functools.wraps
        def wrapper():
            print(ss)
            func()
            print(es)
        return wrapper
    return printer

def mkPrinter_download(type):
    ss = f'Downloading {type} to{OUTDIR}...'
    es = f'{type} downloaded.'
    return mkPrinter(ss, es)

risPrinter = mkPrinter_download('ris')
pdfPrinter = mkPrinter_download('pdf')
risAndPdfPrinter = mkPrinter_download('ris and pdf')

class JOURNAL(object):
    
    name = None

    def __init__(self, url):
        self.url = url

    def _cookies_get(self):
        pass # Defined in subclasses

    def _cookies_read(self):
        return pickle.load(open(COOKIEPATH, 'rb'))

    def _cookies_write(self, newCookies):
        if os.path.exists(COOKIEPATH):
            cookies = self._cookies_read()
        else:
            cookies = {}
        cookies[self.name] = newCookies
        with open(COOKIEPATH, 'wb') as f:
            pickle.dump(cookies, f)

    def _cookies_retrieve(self):
        try:
            print('Trying to read cookies from' + COOKIEPATH)
            return self._cookies_read()[self.name]
        except KeyError:
            return self._cookies_get()

    def _pdf_write(self, content):
        with open(OUTDIR + self.name + '.pdf', 'wb') as f:
            print('Downloading PDF...')
            f.write(content)
            print('Done.')