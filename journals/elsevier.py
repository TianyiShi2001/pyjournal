#!/usr/bin/env python
import re
import time

import requests
from lxml import etree as le
from selenium import webdriver

import elsevier
from CONFIG import AUTHTYPE, LOGIN, OUTDIR, UNI

from .JOURNAL import JOURNAL, risAndPdfLogger


class Elsevier(JOURNAL):
    name = 'Elsevier'
    signInUrl = 'https://www.sciencedirect.com/customer/institutionchoice'

    def __init__(self, url, method='default'):
        self.__routine(url, method)
        self.get_ris_and_pdf()

    def __cookies_get_shibboleth(self):
        self.logger.debug('Opening webdriver...')
        sel = webdriver.Chrome()
        self.logger.debug(f'Connecting to the singInUrl: {self.signInUrl}')
        sel.get(self.signInUrl)
        time.sleep(0.5)
        sel.find_element_by_id('auto_inst_srch').send_keys(UNI)
        time.sleep(0.5)
        sel.find_element_by_class_name('inst-name').click()
        time.sleep(3)
        LOGIN(sel)
        cookies = sel.get_cookies()
        self._cookies_write(cookies, 'shibboleth')
        return cookies

    def __cookies_get_default(self):
        pass

    def _cookies_get(self):
        return {
            'shibboleth': self.__cookies_get_shibboleth,
            'default': self.__cookies_get_default
        }[self.method]

    def get_ris_and_pdf(self):
        sel = webdriver.Chrome()
        sel.get(self.url)
        time.sleep(1)
        try:
            sel.find_element_by_id('export-citation').click()
            sel.find_element_by_xpath(
                '//*[text()="Export citation to RIS"]').click()  # Download citations
        except:
            self.url = sel.find_element_by_link_text(
                'Access this article on ScienceDirect').get_attribute('href')
            self.get_ris_and_pdf()
        try:
            cookies = self._cookies_read()[self.name]
        except:
            cookies = self._cookies_get()
        for i in cookies:  # add cookies to get access
            sel.add_cookie({
                'domain': i['domain'],
                'name': i['name'],
                'value': i['value']
            })
        sel.refresh()
        sel.get(self.url)
        sel.find_element_by_class_name('pdf-download-label').click()
        # pdfUrl = 'https://www.sciencedirect.com/' + sel.find_element_by_xpath('//*[text()="Download this article"]/parent::a').get_attribute('href')
        try:
            sel.find_element_by_link_text('Download this article').click()
            time.sleep(1)
            sel.switch_to.window(sel.window_handles[1])
            sel.find_element_by_link_text('Save').click()
            time.sleep(5)
        except:
            cookies = self._cookies_get()
            input('Updated cookies. Press any key to continue.')
            self.get_ris_and_pdf()


class ElsevierImprint(Elsevier):

    def __init__(self, url, authMethod):
        if authMethod != 'default':
            self.url = le.HTML(requests.get(url).text).xpath(
                '//a[text()="Access this article on ScienceDirect"]/@href')[0]
        self.get_ris_and_pdf()

    def __cookies_get_default(self):
        pass


class Cell(ElsevierImprint):
    pass
