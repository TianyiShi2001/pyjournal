#!/usr/bin/env python

from selenium import webdriver
import time
import requests
from .JOURNAL import *
from CONFIG import LOGIN, OUTDIR, UNI, AUTHTYPE


class Nature(JOURNAL):
    name = 'Nature'
    baseUrl = 'https://www.nature.com/'

    def __init__(self, url):
        self.url = url
        self.get_ris()
        self.get_pdf()

    def _name(self):
        return self.name

    def _cookies_get(self):
        sel = webdriver.Chrome()
        sel.get(self.url)
        if AUTHTYPE == 'shibboleth':
            sel.find_element_by_link_text('Access through your institution').click()
            time.sleep(1)
            sel.find_element_by_id('keywords-institutions').send_keys(UNI)
            sel.find_element_by_id('search-button').click()
            sel.find_element_by_class_name('search-result').click()
            time.sleep(3)
            LOGIN(sel)
            cookies = self._for_requests(sel.get_cookies())
            self._cookies_write(cookies)
            return cookies

    @risLogger
    def get_ris(self):
        with open(OUTDIR + self.name + '.ris', 'wb') as f:
            f.write(requests.get(self.url + '.ris').content)

    @pdfLogger
    def get_pdf(self):
        try:
            self._pdf_write(requests.get(self.url + '.pdf', cookies=self._cookies_retrieve()).content)
        except:
            input('Update cookies and try again?')
            self._cookies_get()
            Nature(self.url)


if __name__ == "__main__":
    Nature(input())
