import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np

'''
Business ------ 1
Entertainment-- 2 
Health--------- 3
Politics------- 4
Sci_Tech------- 5
Sport---------- 6
World---------- 7
'''

def get_data(id_text_dict,i):
    label = []
    corpus = []
    for id, value in id_text_dict.items():
        label.append(i)
        corpus.append(" ".join(value))

    return corpus, label

def adjust_formatofDataset(path, data_path, file_list):
    complete_id_attris_dict = {}
    id_text_dict = {}
    id_flag = 0
    corpuses = []
    label_LIST = []
    for i,part in enumerate(files_list):
        path = data_path + '\\' + part + '.xml'
        complete_id_attris_dict_step, id_text_dict_step, id_time_dict_step, id_flag = xml_parser(file_path=path,
                                                                                                 attri_list=['TITLE',
                                                                                                             'AUTHER',
                                                                                                             'DATE',
                                                                                                             'TOPIC',
                                                                                                             'IMAGE',
                                                                                                             'TEXT',
                                                                                                             'URL'],
                                                                                                 id_start=id_flag)

        corpuse, lable = get_data(id_text_dict_step, i+1)

        corpuses += corpuse
        label_LIST += lable

        complete_id_attris_dict.update(complete_id_attris_dict_step)
        id_text_dict.update(id_text_dict_step)
    with open(path, 'w', encoding='utf-8') as f:
        for key, label in zip(complete_id_attris_dict.keys(), label_LIST):
            Text = complete_id_attris_dict[key]['TITLE'] + ' ' + complete_id_attris_dict[key]['TEXT']
            Text = Text.split(' ')
            Text = " ".join(Text)
            Text = re.sub('\n\n', ' ', Text)
            Text = re.sub('\n', ' ', Text)

            f.write('{}\t{}\t{}\n'.format(key, Text, str(label)))

def split_dataset():
    L = []
    with open('D:\\ttds-cw3\\data.train', 'r', encoding='utf-8') as f:
        l = f.readlines()
        for line in l:
            L.append(line)
    X = np.array(L)
    Y = np.array(L)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    with open('D:\\ttds-cw3\\data1.train', 'w', encoding='utf-8') as f:
        for i in X_train:
            f.write(i)

    with open('D:\\ttds-cw3\\data1.test', 'w', encoding='utf-8') as f:
        for i in X_test:
            f.write(i)

def BOW(path_train):
    with open(path_train, 'r+', encoding='utf-8', errors='ignore') as f:
        ff_train = f.readlines()
    ff = []
    for line in ff_train:
        line = line.lower()
        line = line.split()
        line.pop(0)
        line.pop(-1)
        ff += line
    BOW = []
    for word in ff:
        if word not in stopwords:
            word = stem(word)
            if word not in BOW:
                BOW.append(word)
    cnt = 1
    BOW_dict = {}
    for i in BOW:

        BOW_dict[i] = cnt
        cnt += 1

    return BOW_dict


def Convert_data(path,BOW,dic):
    with open(path, 'r+', encoding='utf-8', errors='ignore') as f:
        f1 = f.readlines()
    Feature = []
    cnt = 0
    for line in f1:

        f2 = f1.split()
        f2.pop(0)
        label = f2.pop(-1)
        f5 = []
        f4 = []
        temp = []
        for i in range(len(f2)):
            if f3[i] not in stopwords:
                f5.append(stem(f3[i]))

                if BOW.get(f3[i],0):
                    tf = len(dic[word][order + 1])
                    df = len(dic[word])
                    score = (1 + np.log10(tf)) * np.log10(N / df)
                    score = np.round(score, 4)

                    temp.append("{}:{}".format(BOW[f3[i]], score))

        temp = sorted(temp)

        temp.append(label)
        Feature.append(temp)

    return Feature

converted_train = Convert_feature(path_train,BOW,dic_train)
converted_test = Convert_feature(path_test,BOW,dic_test)

with open('./feats.train', 'w+') as f:
    for doc in converted_train:
        f.write("{}	{}\n".format(doc[-1]," ".join(doc[:-1])))

with open('./feats.test', 'w+') as f:
    for doc in converted_test:
        f.write("{}	{}\n".format(doc[-1]," ".join(doc[:-1])))

X_train,y_train = load_svmlight_file("./feats.train",dtype=np.float64,multilabel=True)
X_test,y_test = load_svmlight_file("./feats.test",dtype = np.float64,multilabel=True)
y_train = np.array([int(yy[0]) for yy in y_train])
y_test = np.array([int(yy[0]) for yy in y_test])

clf=OneVsRestClassifier(SVC(C=1000, kernel="sigmoid", gamma="auto"))
clf.fit(X_train[:,:], y_train)
y_predict = clf.predict(X_test)
print(np.mean(y_predict == y_test))
print(y_predict)

with open('./sklearn_predict.txt', 'w') as new_file:
    for item in y_predict:
        new_file.write(str(item)+' ')

