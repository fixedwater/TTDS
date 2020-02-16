import os

for tag in ['Business','entertainment','health','politics','Sci_Technology','sport']:
    os.chdir('F:\\Mytools\\workspace\\TTDS-master\\catagery-bbc\\'+tag)
    file_chdir = os.getcwd()
    root_list = []
    for root,dirs,files in os.walk(file_chdir,topdown=True):
        root_list.append(root)
        
    f=open('Articles.xml','w',encoding='UTF-8')
    f.writelines('<?xml version="1.0" ?>\n')
    f.writelines('<DATA>\n')
    for path in root_list[1:]:
        filepath = path+'\\Articles.xml'
        with open(filepath,'r',encoding='UTF-8') as fr:
            for line in fr:
                if line == '<?xml version="1.0" ?>\n':
                    continue
                if line == '<DATA>\n':
                    continue
                if line == '</DATA>\n':
                    continue
                f.writelines(line)
    f.writelines('</DATA>\n')
    f.close()


os.chdir('F:\\Mytools\\workspace\\TTDS-master\\catagery-bbc\\')
file_chdir = os.getcwd()

f=open('Articles.xml','w',encoding='UTF-8')
f.writelines('<?xml version="1.0" ?>\n')
f.writelines('<DATA>\n')
for tag in ['Business','entertainment','health','politics','Sci_Technology','sport']:
    filepath = file_chdir+'\\'+tag+'\\Articles.xml'
    with open(filepath,'r',encoding='UTF-8') as fr:
            for line in fr:
                if line == '<?xml version="1.0" ?>\n':
                    continue
                if line == '<DATA>\n':
                    continue
                if line == '</DATA>\n':
                    continue
                f.writelines(line)
f.writelines('</DATA>\n')
f.close()