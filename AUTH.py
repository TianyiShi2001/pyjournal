#!/usr/bin/env python

import time

def oxford(sel, UNAME, PASSWD):        
    sel.find_element_by_id('username').send_keys(UNAME)
    sel.find_element_by_id('password').send_keys(PASSWD)
    sel.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(1)
    sel.find_element_by_class_name('go_button').click()
    time.sleep(1)

def jerusalem():
    pass

AUTH = {
    'University of Oxford': ['shibboleth', oxford],
    'Hebrew University of Jerusalem': ['openathens', jerusalem]
}
