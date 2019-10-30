#!/usr/bin/env python
from selenium import webdriver
import time, re
import requests
from JOURNAL import JOURNAL
from lxml import etree as le
from CONFIG import LOGIN, OUTDIR


class Elsevier(JOURNAL):
    name = 'Elsevier'
    signInUrl = 'https://www.sciencedirect.com/customer/institutionchoice'

    def __init__(self, url):
        self.url = url
        self.get_bib_and_pdf()

    def _cookies_get(self):
        sel = webdriver.Chrome()
        sel.get(self.signInUrl)
        time.sleep(0.5)
        sel.find_element_by_id('auto_inst_srch').send_keys('University of Oxford')
        time.sleep(0.5)
        sel.find_element_by_class_name('inst-name').click()
        time.sleep(1)
        LOGIN(sel)
        cookies = sel.get_cookies()
        self._cookies_write(cookies)
        return cookies

    def get_bib_and_pdf(self):
        try:
            cookies = self._cookies_read()[self.name]
        except:
            cookies = self._cookies_get()
        sel = webdriver.Chrome()
        sel.get(self.url)
        time.sleep(1)
        try:
            sel.find_element_by_id('export-citation').click()
            sel.find_element_by_xpath('//*[text()="Export citation to RIS"]').click() # Download citations
        except:
            self.url = sel.find_element_by_link_text('Access this article on ScienceDirect').get_attribute('href')
            self.get_bib_and_pdf()
        for i in cookies: # add cookies to get access
            sel.add_cookie({
                'domain':i['domain'],
                'name':i['name'],
                'value':i['value']
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
            self.get_bib_and_pdf()
        
class ElsevierImprint(Elsevier):

    def __init__(self, url):
        self.url = le.HTML(requests.get(url).text).xpath('//a[text()="Access this article on ScienceDirect"]/@href')[0]
        self.get_bib_and_pdf()

class Cell(ElsevierImprint):
    pass
