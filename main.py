import os
from indexer import *
from recommender import *


# file_path = 'D:\\ttds-cw3\Articles.xml'
file_path = './Articles.xml'


def package_install():
    import nltk
    nltk.download('stopwords')


def main():
    # step 1: parse xml
    # complete_id_attris_dict = {ID:{attri:val}}, id_text_dict = {ID: [title + text]}
    complete_id_attris_dict, id_text_dict = xml_parser(file_path=file_path,
                                                       attri_list=['TITLE', 'AUTHER', 'DATE', 'TOPIC', 'TEXT', 'URL'])

    # todo: step2: store complete_id_attris_dict into database and release memory

    # step 3: indexing
    # indexed_dict = {term: {id:[pos]}}
    indexed_dict = indexing(id_text_dict)

    # step 4: form TFIDF, bm25 ranking results for each term in corresponding documents
    # term_id_tfidf_bm25_dict = {term: {id: (tfidf, bm25) }}
    term_id_tfidf_bm25_dict = form_term_id_tfidf_bm25(id_text_dict, indexed_dict)


    vectors, id_list = convert_news_to_vectors(id_text_dict, term_id_tfidf_bm25_dict, mode='tfidf')
    similar_doc = find_most_similar_doc(vectors, id_list)

  #  for term in term_id_tfidf.keys():
  #      print("term: {}, ID: (TF, DF, TFIDF): {}\n".format(term,term_id_tfidf[term]))
  #  for key, val in results.items():
  #      print(key, val)
  #  print(id_text_dict)

    print(similar_doc)


if __name__ == '__main__':
    # package_install()
    main()
