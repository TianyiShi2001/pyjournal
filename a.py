import lxml.etree as le

BIBPATH = 'main.bib'

GROUP = 'test'



def group_update(newKey):
    global BIBPATH, GROUP

    with open(BIBPATH, 'r+') as f:
        while f.readline() != '<plist version="1.0">\n':
          pass
        writeLoc = f.tell()

        xml = ''
        while (line:=f.readline()) != '</plist>\n':
            xml += line

        groups = {}
        for group in le.XML(xml).xpath('//dict'):
            k, v = group.xpath('./string/text()')
            groups.update({k:v})

        if lst := groups.get(GROUP):
            groups[GROUP] = ','.join([lst, newKey])
        else:
            groups[GROUP] = newKey

        f.seek(writeLoc)
        f.write('<array>\n')
        for k, v in groups.items():
            f.write('\t<dict>\n')
            f.write('\t\t<key>group name</key>\n')
            f.write(f'\t\t<string>{k}</string>\n')
            f.write('\t\t<key>keys</key>\n')
            f.write(f'\t\t<string>{v}</string>\n')
            f.write('\t</dict>\n')
        f.write('</array>\n</plist>\n}}')

if __name__ == '__main__':
    group_update('Hirai-2019')
