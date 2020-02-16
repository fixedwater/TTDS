import os

for tag in ['Business','entertainment','health','politics','Sci_Technology','sport']:
    os.chdir('F:\\Mytools\\workspace\\TTDS-master\\catagery-bbc\\'+tag)
    file_chdir = os.getcwd()
    root_list = []
    for root,dirs,files in os.walk(file_chdir,topdown=True):
        root_list.append(root)
        
    f=open('Articles.xml','w',encoding='UTF-8')
    for path in root_list[1:]:
        filepath = path+'\\Articles.xml'
        with open(filepath,'r',encoding='UTF-8') as fr:
            for line in fr:
                f.writelines(line)
    f.close()


os.chdir('F:\\Mytools\\workspace\\TTDS-master\\catagery-bbc\\')
file_chdir = os.getcwd()

f=open('Articles.xml','w',encoding='UTF-8')
for tag in ['Business','entertainment','health','politics','Sci_Technology','sport']:
    filepath = file_chdir+'\\'+tag+'\\Articles.xml'
    with open(filepath,'r',encoding='UTF-8') as fr:
            for line in fr:
                f.writelines(line)
f.close()