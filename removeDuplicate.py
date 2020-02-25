import os
from lxml import etree

#YOur path
path = '/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/dataset'
files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))

f=open('Articles.xml','w',encoding='UTF-8')
f.writelines('<?xml version="1.0"?>\n')
f.writelines('<DATA>\n')
for path in files:
    with open(path,'r',encoding='UTF-8') as fr:
        for line in fr:
            if line == '<?xml version="1.0"?>\n':
                continue
            if line == '<DATA>\n':
                continue
            if line == '</DATA>\n':
                continue
            f.writelines(line)
f.writelines('</DATA>\n')
f.close()


f = '/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/Articles.xml'
dom = etree.parse(f)
xsl = etree.parse('/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/check.xsl')

# TRANSFORM XML
transform = etree.XSLT(xsl)
result = transform(dom)

# SAVE OUTPUT TO FILE
with open('/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/Articles.xml', 'wb') as fi:
    fi.write(result)


'''
#original verison
path = '/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/dataset/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))

for f in files:
    dom = etree.parse(f)
    xsl = etree.parse('/media/jsir/Windows/Users/jiang/Desktop/ed HPC/ttds/project/crawler/check.xsl')

# TRANSFORM XML
    transform = etree.XSLT(xsl)
    result = transform(dom)

# SAVE OUTPUT TO FILE
    with open(f, 'wb') as fi:
        fi.write(result)
'''