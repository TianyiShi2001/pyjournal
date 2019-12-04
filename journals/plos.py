#!/usr/bin/env python
from selenium import webdriver
import time
import re
import requests
from .JOURNAL import JOURNAL, risAndPdfLogger
from lxml import etree as le
from CONFIG import LOGIN, OUTDIR, UNI, AUTHTYPE

# * info: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0028766
# * pdf:  https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0028766&type=printable
# * bib:  https://journals.plos.org/plosone/article/citation/bibtex?id=10.1371/journal.pone.0028766


class Plos(JOURNAL):

    baseUrl = 'https://journals.plos.org/plosone/article'

    def __init__(self, url):
        self.url = url
        self.id = self.url.split('?')[1]  # 'id=10.1371/journal.pone.0028766'
        self.get_pdf()
        self.get_bib()

    def get_bib(self):
        bibUrl = self.baseUrl + '/citation/bibtex?' + self.id

    def get_pdf(self):
        pdfUrl = self.baseUrl + '/file?' + self.id + '&type=printable'
        with open(OUTDIR + 'a.pdf') as f:
            f.write(requests.get(pdfUrl).content)
