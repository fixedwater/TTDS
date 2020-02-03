import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
def Convert_news_to_vectors(id_text_dict, term_id_tfidf):
    '''

    :param id_text_dict: Dictionary, id:[text]
    :param term_id_tfidf: Dictionary, term:id:[text]
    :return: Dictionary, id:[text(tfidf)]
    id:[term:tfidf, term:tfidf, term:tfidf, term:tfidf, term:tfidf, term:tfidf]
    '''


    vectors = {}
    vectors1 = {}

    for key, value in id_text_dict.items():

        value = set(value)
        temp_dict = {}
        for term in value:
            temp_dict[term] = term_id_tfidf[term][key][-1]
        temp_dict_1 = sorted(temp_dict.items(), key=lambda x:x[1], reverse=True)
        vectors[key] = temp_dict
        vectors1[key] = temp_dict_1

    top_n_terms = 25  # use top 25 terms in every new in terms of TFIDF as Bag of Words
    Bag_of_words = {}
    position = 0
    for value in vectors1.values():
        if len(value) >= top_n_terms:
            for term in value[:25]:
                if term[0] not in Bag_of_words.keys():
                    Bag_of_words[term[0]] = position
                    position += 1

        else:
            for term in value:
                if term[0] not in Bag_of_words.keys():
                    Bag_of_words[term[0]] = position
                    position += 1


    Dimension = len(Bag_of_words)
    converted_vectors = []
    for key,value in vectors.items():
        vector = [0] * Dimension
        for key1,value1 in value.items():
            d = Bag_of_words.get(key1,0)
            if d:
                vector[d] = value1
        converted_vectors.append(vector)

    return converted_vectors

def find_most_similar_doc(converted_vectors):
    distance_matrix = pairwise_distances(converted_vectors, metric="cosine")
    similar_doc = {}
    distance_matrix = np.argsort(distance_matrix)
    simililar_doc = {}
    for id,row in enumerate(distance_matrix):
        similar_doc[id+1] = row

    return similar_doc







