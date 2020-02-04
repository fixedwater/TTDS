import xml.etree.ElementTree as ET
import re
import nltk
from stemming.porter2 import stem
from nltk.corpus import stopwords
import copy
import numpy as np
nltk.download('stopwords')



def text_process(text):
    # remove symbols
    pure = re.sub(r'[^A-Za-z0-9\-]+', ' ', text)
    # case-folding
    case_folded_text = pure.lower()
    # tokenisation
    word_tokens = case_folded_text.split()
    # stopping
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in word_tokens if word not in stop_words]
    # stemming
    processed_text = [stem(word) for word in filtered_text]

    return processed_text


def indexing(id_text_dict):
    # indexing step 1: term sequence -> {term:id} invalid since multiple terms as the same key
    # [(term,id,pos),(...),...]
    list_of_term_id_pos_pair = []
    for key, value in id_text_dict.items():
        for pos in range(0, len(value)):
            list_of_term_id_pos_pair.append((value[pos], key, pos + 1))
    # print(list_of_term_id_pos_pair[0])

    # indexing step 2: sort by term, then id
    # [(term_sorted,id,pos),(...),...]
    list_of_term_id_pos_pair_sorted = sorted(list_of_term_id_pos_pair)

    # indexing step 3: posting
    # data structure:
    # { term1: {id1:[pos], id2:[pos]}, term2: {id1:[pos]}, id2:[pos]} }
    prev_term = list_of_term_id_pos_pair_sorted[0][0]
    prev_id = list_of_term_id_pos_pair_sorted[0][1]
    initial_pos = list_of_term_id_pos_pair_sorted[0][2]
    dict = {prev_term: {prev_id: [initial_pos]}}
    for item in list_of_term_id_pos_pair_sorted[1:]:
        term = item[0]
        id = item[1]
        pos = item[2]
        if term == prev_term:
            if id == prev_id:
                dict[term][id].append(pos)
            elif id != prev_id:
                dict[term][id] = [pos]
                prev_id = id
        elif term != prev_term:
            dict[term] = {id: [pos]}
            prev_term = term
            prev_id = 0  # refresh prev_id to an impossible value
    return dict

def Dcit_Term_ID_Tfidf(id_text_dict, dict):
    '''

    :param id_text_dict: dictionary: id : text
    :param dict: dictionary: term:id:pos
    :return: dictionary: term:id:(tf,df,tfidf)
    '''

    N = len(id_text_dict)  #number of documents
    term_id_tfidf = copy.deepcopy(dict)
    for term in term_id_tfidf.keys():
        df = len(term_id_tfidf[term])

        for key in term_id_tfidf[term].keys():
            tf = len(term_id_tfidf[term][key])
            score = (1 + np.log10(tf) * np.log10(N / df))
            term_id_tfidf[term][key] = (tf, df, round(score,4))
    return term_id_tfidf

class PreprocessModule(object):
    def __init__(self, file_path=None):
        if file_path is None:
            raise ValueError
        self.file_path = file_path
        self.attri_list = ['TITLE', 'AUTHER', 'DATE', 'TOPIC', 'TEXT', 'URL']

    def xml_parser(self):
        """
        parse xml file and do tokenisation, stopping and stemming to title and text
        :return: {ID: {attribution:val}}
        """

        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # {ID: {attribution:val}}
        complete_id_attris_dict = dict()
        attri_val_dict = dict()

        # {ID: text}
        id_text_dict = dict()

        for doc in root.findall('DOC'):
            ID = doc.find('ID').text
            title = ''
            main_text = ''
            for attr in self.attri_list:
                val = doc.find(attr).text
                attri_val_dict[attr] = val

                if attr == 'TITLE':
                    title = text_process(val)
                elif attr == 'TEXT':
                    main_text = text_process(val)

            text = title + main_text
            id_text_dict[ID] = text
            complete_id_attris_dict[ID] = attri_val_dict

        return complete_id_attris_dict, id_text_dict
