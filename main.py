import os
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from indexer import *
from recommender import *
from searcher import *


# file_path = 'D:\\ttds-cw3\Articles.xml'
file_path = './Articles.xml'


def package_install():
    """
    install necessary package
    """
    import nltk
    nltk.download('stopwords')


def load_glove():
    """
    load glove pre-trained word vectors
    :return: Glove model
    """
    glove_file = datapath('/Users/cyril_huang/Desktop/Stanford-NLP/GloVe/glove.6B.100d.txt')
    word2vec_glove_file = get_tmpfile("glove.6B.100d.word2vec.txt")
    glove2word2vec(glove_file, word2vec_glove_file)
    glove_model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
    return glove_model

def main():
    # step 1: parse xml
    # complete_id_attris_dict = {ID:{attri:val}}, id_text_dict = {ID: [title + text]}
    complete_id_attris_dict, id_text_dict, id_time_dict = xml_parser(file_path=file_path,
                                                       attri_list=['TITLE', 'AUTHER', 'DATE', 'TOPIC', 'TEXT', 'URL'])

    # todo: step2: store complete_id_attris_dict into database and release memory

    # step 3: indexing
    # indexed_dict = {term: {id:[pos]}}
    indexed_dict = indexing(id_text_dict)

    # step 4: form TFIDF, bm25 ranking results for each term in corresponding documents
    # term_id_tfidf_bm25_dict = {term: {id: (tfidf, bm25) }}
    term_id_tfidf_bm25_dict = form_term_id_tfidf_bm25(id_text_dict, indexed_dict)

    # step 5: recommend 5 top related news based on tfidf or bm25 score
    vectors, id_list = convert_news_to_vectors(id_text_dict, term_id_tfidf_bm25_dict,
                                               mode='bm25', top_n_terms=25)
    similar_doc = find_most_similar_doc(vectors, id_list)

    print(similar_doc)

    # step 6: search model

    search_query = 'Chinese food'
    search_instance = SearchModule(indexed_dict, term_id_tfidf_bm25_dict, id_time_dict)
    search_instance.get_search_query(search_query)

    # glove_model = load_glove()
    # search_instance.get_glove_model(glove_model)

    result = search_instance.conduct_search()


def test():
    res = find_synonyms_search_comb({'best', 'movie'})
    print(res)
    # glove_model = load_glove()
    # res = find_similar_search_comb({'chinese', 'food'}, glove_model)
    # print(res)


if __name__ == '__main__':
    # package_install()
    # main()
    test()


