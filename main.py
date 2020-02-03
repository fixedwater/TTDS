import os
from indexer import *
from recommendation import *
file_path = 'D:\\ttds-cw3\sample.xml'


def main():
    preprocess_module = PreprocessModule(file_path=file_path)
    complete_id_attris_dict, id_text_dict = preprocess_module.xml_parser()

    for key, val in complete_id_attris_dict.items():
        print(key, val)

    for key, val in id_text_dict.items():
        print(key, val)

    # store complete_id_attris_dict into database and release memory

    results = indexing(id_text_dict)
    term_id_tfidf = Dcit_Term_ID_Tfidf(id_text_dict, results)  # construct inverted matrix. term:id:tfidf
    vectors = Convert_news_to_vectors(id_text_dict, term_id_tfidf)
    for term in term_id_tfidf.keys():
        print("term: {}, ID: (TF, DF, TFIDF): {}\n".format(term,term_id_tfidf[term]))
    for key, val in results.items():
        print(key, val)
    print(id_text_dict)

    # store id_text_dict into database and release memory


if __name__ == '__main__':
    main()
