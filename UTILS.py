#!/usr/bin/env python
import regex
from CONFIG import *
from glob import glob
import os

def ris_latest():
    ris_all = glob(OUTDIR+ '*.[rR][iI][sS]') # * means all if need specific format then *.csv
    return max(ris_all, key=os.path.getctime)
def pdf_latest():
    pdf_all = glob(OUTDIR+ '*.[pP][dD][fF]')
    return max(pdf_all, key=os.path.getctime)

def update_citeKey(citeKey):
    with open(BIBPATH) as f:
        bib = f.read()
    usedCiteKeys = regex.findall(r'(?<=@\w+\{).+(?=,)', bib)
    updatedCiteKey = citeKey

    i = 1; l = 'abcdefghi'
    while updatedCiteKey in usedCiteKeys:
        updatedCiteKey = citeKey + l[i]
        i += 1
    
    return updatedCiteKey

def get_citeKey():
    risPath = ris_latest()
    ris = open(risPath).read()
    author = regex.search(r'(?<=AU  - )\w+', ris).group(0)
    year = regex.search(r'(?<=PY  - )\d+', ris).group(0)
    return update_citeKey(author + '-' + year)


def ris_to_bib():
    risPath = ris_latest()

    risToBib = {
        'AU': 'Author',
        'TI': 'Title',
        'PY': 'Year',
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

    ris = []

    for line in open(risPath):
        entry = line.rstrip('\n').split('  - ')
        if risToBib.get(entry[0]):
            ris.append(entry)

    bib = {}

    ris_keys = set(list(zip(*ris))[0])
    for key in ris_keys:
        bib.update({risToBib.get(key):[]})

    for entry in ris:
        bib[risToBib[entry[0]]].append(entry[1])

    citeKey = bib['Author'][0].split(',')[0] + '-' + bib['Year'][0]
    citeKey = update_citeKey(citeKey)

    bib['Author'] = [' and '.join(bib['Author'])]
    bib['Pages'] = ['--'.join(bib['Pages'])]

    for key, value in bib.items():
        bib.update({key:value[0]})

    bibRecordMain = ',\n\t'.join([f'{key} = {{{value}}}' for key, value in bib.items()])
    bibRecord = f'@article{{{citeKey},\n\t' + bibRecordMain + '\n}\n\n'

    print(bibRecord)

    with open(BIBPATH, 'a') as f:
        f.seek(0)
        f.write(bibRecord)
    
    return citeKey

def pdf_modify(dst = DESTDIR):
    src = pdf_latest()
    newName = ris_to_bib() if BIBPATH else get_citeKey()
    os.rename(src, dst + newName + '.pdf')

def ris_modify(dst = DESTDIR):
    src = ris_latest()
    if KEEPRIS:
        newName = ris_to_bib() if BIBPATH else get_citeKey()
        os.rename(src, dst + newName + '.ris')
    else:
        os.remove(src)

if __name__ == "__main__":
    ris_to_bib()
