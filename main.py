import os
#from gensim.test.utils import datapath, get_tmpfile
#from gensim.models import KeyedVectors
#from gensim.scripts.glove2word2vec import glove2word2vec
from indexer import *
from recommender import *
#from searcher import *
from classification import *
from pickle import *
import numpy as np
import pickle

def save_obj(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def write_in_txt(file, result, id_list):
    with open(file,'w') as f:
        for i, j in zip(result,id_list):
            f.write("{}:{}\n ".format(j,i))



# file_path = 'D:\\ttds-cw3\Articles.xml'
from recommender import Convert_news_to_vectors, find_most_similar_doc

file_path = 'D:\\ttds-cw3\\dataset_classifier\\health_390.xml'



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


def get_classifier():
    '''

    :return: classifier, features: features extracted from the sample
    '''
    corpuses = []
    label_LIST = []
    for i, j in zip(["business_200", "entertainment_200", "health_200", "politics_200", "sci-tech_200", "sport_200", "world_200"],
                    [1, 2, 3, 4, 5, 6, 7]):
        file_path = 'D:\\ttds-cw3\\dataset_classifier\\AAA.xml'
        file_path = re.sub("AAA", i, file_path)
        complete_id_attris_dict, id_text_dict, id_time_dict = xml_parser1(file_path=file_path,
                                                                         attri_list=['TITLE',
                                                                                      'TEXT'])
        corpuse, lable = get_data(id_text_dict, j)
        corpuses += corpuse
        label_LIST += lable

    classifier, features = build_classifier(corpuses, label_LIST)


    return classifier, features



def main():
    # step 1: parse xml
    # complete_id_attris_dict = {ID:{attri:val}}, id_text_dict = {ID: [title + text]}

    complete_id_attris_dict, id_text_dict, id_time_dict, id_flag = read_dataset('F:\\Mytools\\workspace\\ttds-cw3\\dataset')

    print("step 1 done")


    # step 2: indexing
    # indexed_dict = {term: {id:[pos]}}
    id_text_dict = np.load('D:\\ttds-cw3\\id_text.npy', allow_pickle=True).item()
    print('id_text load done')
    indexed_dict = indexing(id_text_dict)
    np.save('D:\\ttds-cw3\\indexed.npy', indexed_dict)
    indexed_dict = np.load('D:\\ttds-cw3\\indexed.npy', allow_pickle=True).item()
    print('step2 done')
    # step 3: form TFIDF, bm25 ranking results for each term in corresponding documents
    # term_id_tfidf_bm25_dict = {term: {id: (tfidf, bm25) }}


    term_id_tfidf_bm25_dict = form_term_id_tfidf_bm25(id_text_dict, indexed_dict)
    save_obj(term_id_tfidf_bm25_dict)
    np.save('D:\\ttds-cw3\\iterm_id.npy', term_id_tfidf_bm25_dict)
    print('step3 done')
    # step 4: Construct a Classifier and Classify the News. Write to complete_id_attris_dict before storing

    #classifier, features = get_classifier()
    #print("got classifier")
    #term_id_tfidf_bm25_dict = load_obj('D:\\ttds-cw3\\term_i.pkl')
    #print('term_i load done')
    #Vectors, id_list = vectorize(id_text_dict, features, term_id_tfidf_bm25_dict)
    #y_pred = classifier.predict(Vectors)
    #write_in_txt("D:\\ttds-cw3\\categoty.txt",y_pred,id_list)
    #print("prediction done")

    #for i, value in enumerate(complete_id_attris_dict.values()):
        #value['Category'] = y_pred[i]

    # step 5: recommend 5 top related news based on tfidf or bm25 score
    #length = len(Vectors)
    #pie = int(length / 10000)
    #Similar_doc = recommend(pie, Vectors, id_list)
    #np.save("D:\\ttds-cw3\\pieLast.npy", Similar_doc)
    #print("save pieLast done")

    # step 6: search model
    # todo: interface of getting search query here
    search_query = 'National Committee'

    search_instance = SearchModule(indexed_dict, term_id_tfidf_bm25_dict, id_time_dict)
    search_instance.get_search_query(search_query)

    # glove_model = load_glove()
    search_instance.get_glove_model(glove_model)

    result, len = search_instance.conduct_search()
    print('search result: ' + str(result) + '    number of news found: ' + str(len))

    # todo: get similar combs and show


def test():
    res = find_synonyms_search_comb({'museums', 'library'})
    #print(res)
    # glove_model = load_glove()
    # res = find_similar_search_comb({'chinese', 'food'}, glove_model)
    # print(res)


if __name__ == '__main__':
    # package_install()
    main()
    # test()