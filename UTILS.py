#!/usr/bin/env python
import regex
from CONFIG import *
from glob import glob
import os
import lxml.etree as le

class UTILS(object):
    '''Set of actions after downloading
    '''

    def __init__(self):
        self.risSrc = self.ris_latest()
        self.pdfSrc = self.pdf_latest()
        self.newKey = self.get_citeKey()
        if BIBPATH:
            self.ris_to_bib()
            self.group_update()
        self.pdf_update()
        self.ris_update()

    def ris_latest(self):
        ris_all = glob(OUTDIR+ '*.[rR][iI][sS]') # * means all if need specific format then *.csv
        return max(ris_all, key=os.path.getctime)
    def pdf_latest(self):
        pdf_all = glob(OUTDIR+ '*.[pP][dD][fF]')
        return max(pdf_all, key=os.path.getctime)

    def update_citeKey(self, citeKey):
        '''Lastname-2017a if Lastname-2017 exists
        '''
        with open(BIBPATH) as f:
            bib = f.read()
        usedCiteKeys = regex.findall(r'(?<=@\w+\{).+(?=,)', bib)
        updatedCiteKey = citeKey

        i = 1; l = 'abcdefghi'
        while updatedCiteKey in usedCiteKeys:
            updatedCiteKey = citeKey + l[i]
            i += 1
    
        return updatedCiteKey

    def get_citeKey(self):
        with open(self.risSrc) as f:
            ris = f.read()
        author = regex.search(r'(?<=(AU|A1)  - )\w+', ris).group(0)
        year = regex.search(r'(?<=PY  - )\d+', ris).group(0)
        return self.update_citeKey(author + '-' + year)


    def ris_to_bib(self):
        risToBib = {
            'A1': 'Author',
            'AU': 'Author',
            'TI': 'Title',
            'T1': 'Title',
            'PY': 'Year',
            'JF': 'Journal',
            'JO': 'Journal',
            'VL': 'Volume',
            'IS': 'Number',
            'SP': 'Pages',
            'EP': 'Pages',
            'DO': 'Doi',
            'UR': 'Url'
        }   
        
        if USEKEYWORDS:
            risToBib.update({'KW': 'Keywords'})

        ris = [] # list of raw ris entries, each entry is a list of k&v, e.g. [['AU', 'Shi, Tianyi'], ['T1', 'Foo bar'], ...
        for line in open(self.risSrc):
            entry = line.rstrip('\n').split('  - ') 
            if risToBib.get(entry[0]):
                ris.append(entry)

        bib = {} # dict ready to write bib format 
        ris_keys = set(list(zip(*ris))[0]) # ignore repetitions, e.g. AU
        for key in ris_keys: # construct {bibKey:[<empty list>]} for each bibKey
            bib.update({risToBib.get(key):[]})
        for entry in ris: # append values from ris entries to corresponding bibKeys
            bib[risToBib[entry[0]]].append(entry[1])

        # bibtex formatting 
        bib['Author'] = [' and '.join(bib['Author'])] 
        bib['Pages'] = ['--'.join(bib['Pages'])]

        # getting rid of the list (now all entries should have one list item)
        for key, value in bib.items():
            bib.update({key:value[0]})

        # formatting for output
        bibRecordMain = ',\n\t'.join([f'{key} = {{{value}}}' for key, value in bib.items()])
        bibRecord = f'@article{{{self.get_citeKey()},\n\t' + bibRecordMain + '\n}\n\n'

        # output
        with open(BIBPATH, 'r') as f:
            old = f.read()
        with open(BIBPATH, 'w') as f:
            f.write(bibRecord)
            f.write(old)

        if VERBOSE:
            print(bibRecord)

    def group_update(self):
        newKey = self.newKey
        for GROUP in BIBDESKGROUPS:
            with open(BIBPATH, 'r+') as f:
                while f.readline() != '<plist version="1.0">\n':
                    pass
                writeLoc = f.tell()

                plist = ''
                while (line:=f.readline()) != '</plist>\n':
                    plist += line

                groups = {}
                for group in le.XML(plist).xpath('//dict'):
                    k, v = group.xpath('./string/text()')
                    groups.update({k:v})

                if lst := groups.get(GROUP):
                    groups[GROUP] = ','.join([lst, newKey])
                else:
                    groups[GROUP] = newKey

                f.seek(writeLoc)
                f.write('<array>\n')
                for k, v in groups.items():
                    f.write(f'''\
                    \t<dict>
                    \t\t<key>group name</key>
                    \t\t<string>{k}</string>
                    \t\t<key>keys</key>
                    \t\t<string>{v}</string>
                    \t</dict>''')
                f.write('</array>\n</plist>\n}}')

    def pdf_update(self, dst = DESTDIR):
        os.rename(self.pdfSrc, dst + self.newKey + '.pdf')

    def ris_update(self, dst = DESTDIR):
        src = self.risSrc
        if KEEPRIS:
            os.rename(src, dst + self.newKey + '.ris')
        else:
            os.remove(src)