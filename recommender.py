import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def find_most_similar_doc(converted_vectors, id_list):
    distance_matrix = pairwise_distances(converted_vectors, metric="cosine")
    similar_doc = {}
    distance_matrix = np.argsort(distance_matrix)
    similar_doc_index = []

    for id,row in zip(id_list, distance_matrix):
        similar_doc_id = []
        similar_doc_index = row[1:6]
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




