import numpy as np
from sklearn.metrics.pairwise import pairwise_distances


def convert_news_to_vectors(id_text_dict, term_id_tfidf_bm25_dict, mode, top_n_terms):
    """
    :param id_text_dict: Dictionary, {id:[text]}
    :param term_id_tfidf_bm25_dict: Dictionary, {term: {id: (tfidf, bm25) }}
    :param mode = 'tfidf' or 'bm25'
    :param top_n_terms:  use how many top terms in every news in terms of TFIDF as Bag of Words
    :return: Dictionary, id:[text(tfidf)]
    id:[term:tfidf, term:tfidf, term:tfidf, term:tfidf, term:tfidf, term:tfidf]
    """

    vectors = {}
    vectors1 = {}
    id_list = []
    for key, value in id_text_dict.items():
        id_list.append(key)
        value = set(value)
        temp_dict = {}
        for term in value:
            if mode == 'tfidf':
                temp_dict[term] = term_id_tfidf_bm25_dict[term][key][0]
            elif mode == 'bm25':
                temp_dict[term] = term_id_tfidf_bm25_dict[term][key][1]
        temp_dict_1 = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
        vectors[key] = temp_dict
        vectors1[key] = temp_dict_1

    bag_of_words = {}
    position = 0
    for value in vectors1.values():
        if len(value) >= top_n_terms:
            for term in value[:top_n_terms]:
                if term[0] not in bag_of_words.keys():
                    bag_of_words[term[0]] = position
                    position += 1

        else:
            for term in value:
                if term[0] not in bag_of_words.keys():
                    bag_of_words[term[0]] = position
                    position += 1

    dimension = len(bag_of_words)
    converted_vectors = []
    for key, value in vectors.items():
        vector = [0] * dimension
        for key1, value1 in value.items():
            d = bag_of_words.get(key1, 0)
            if d:
                vector[d] = value1
        converted_vectors.append(vector)

    return converted_vectors, id_list


def find_most_similar_doc(converted_vectors, id_list):
    distance_matrix = pairwise_distances(converted_vectors, metric="cosine")
    similar_doc = {}
    distance_matrix = np.argsort(distance_matrix)
    for id, row in zip(id_list, distance_matrix):
        similar_doc[id] = np.array(row[1:6]) + 1

    return similar_doc
