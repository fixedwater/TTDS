from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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

def build_classifier(corpuses, label_list):

    vectorizer = TfidfVectorizer(max_features=10000)
    X = vectorizer.fit_transform(corpuses)
    Y = np.array(label_list)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=12)
    model = RandomForestClassifier(n_estimators=300, max_depth=150, n_jobs=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("\nAccuracy: ", acc)

    return model, vectorizer.get_feature_names()

def vectorize(id_text_dict,feature_list,tf_idf_dict):
    Vectors = []
    id_list = []
    for id in id_text_dict.keys():
        l = []
        id_list.append(id)
        for term in feature_list:
            if tf_idf_dict.get(term,0):
                if tf_idf_dict[term].get(id,0):
                    l.append(tf_idf_dict[term][id][-1])
                else:
                    l.append(0)
            else:
                l.append(0)
        Vectors.append(l)

    return  Vectors