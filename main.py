#/usr/bin/env python3
import re
from elsevier import *
from nature import *
import requests
from UTILS import UTILS


siteMap = {
    'sciencedirect':Elsevier,
    'elsevier':Elsevier,
    'cell':Cell,
    'nature':Nature
}

def _parse_doi(url):
    """If the input is a doi, return the redirected link. Else return the input link

    >>> _parse_doi('https://doi.org/10.1016/j.humimm.2019.07.298')
    'https://linkinghub.elsevier.com/retrieve/pii/S0198885919310274'
    >>> _parse_doi('10.1016/j.bpj.2019.09.006')
    'https://linkinghub.elsevier.com/retrieve/pii/S0006349519307805'
    >>> _parse_doi('doi.org/10.1038/nmeth.2812')
    'https://www.nature.com/articles/nmeth.2812'
    """
    if re.search(r'^10\.\d+/', url):
        return requests.get('https://doi.org/' + url).url
    elif  re.match(r'(http(s)*://)*(www\.)*(\w+)(\..+)', url).group(4) == 'doi':
        return requests.get('https://doi' + re.match(r'(http(s)*://)*(www\.)*(\w+)(\..+)', url).group(5)).url 
    else:
        return url


def _parse_site(url):
    """To gieve the site name

    >>> _parse_site('doi.org/10.1038/nmeth.2812')
    'nature'
    >>> _parse_site('https://www.cell.com/biophysj/fulltext/S0006-3495(09)00849-2')
    'cell'
    >>> _parse_site('10.1016/j.bpj.2019.09.006')
    'elsevier'
    """
    return re.match(r'(http(s)*://)*(www\.)*(.+\.)*(\w+)(\.\w+/)', _parse_doi(url)).group(5)
    

def main():
    urls = []
    while True:
        line = input()
        if line:
            urls.append(line)
        else:
            break
    for url in urls:
        siteMap[_parse_site(url)](url)
        time.sleep(1)
        UTILS()

if __name__ == "__main__":
    main()
