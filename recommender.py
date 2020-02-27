import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
def get_features(corpuses):

    vectorizer = TfidfVectorizer(max_features=25000)
    X = vectorizer.fit_transform(corpuses)

    return vectorizer.get_feature_name

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

    return  Vectors, id_list

def find_most_similar_doc(converted_vectors, id_list):
    distance_matrix = pairwise_distances(converted_vectors, metric="cosine")
    similar_doc = {}
    distance_matrix = np.argsort(distance_matrix)
    similar_doc_index = []

    for id,row in zip(id_list, distance_matrix):
        similar_doc_id = []
        similar_doc_index = row[1:10]
        for i in similar_doc_index:
            similar_doc_id.append(id_list[i])
        similar_doc[id] = similar_doc_id

    return similar_doc


def recommend(pie,Vectors, id_list):
    left = 0
    right = 10000
    Similar_doc = {}
    for i in range(pie - 1):
        similar_doc = find_most_similar_doc(Vectors[left:right], id_list[left:right])
        left += 10000
        right += 10000
        Similar_doc.update(similar_doc)
        print("update pie{} done".format(i))
    similar_doc = find_most_similar_doc(Vectors[left:], id_list[left:])
    Similar_doc.update(similar_doc)
    print("update pie Final done")

    return  Similar_doc




