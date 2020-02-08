import xml.etree.ElementTree as ET
import re
from stemming.porter2 import stem
from nltk.corpus import stopwords
import copy
import numpy as np


def xml_parser(file_path, attri_list):
    """
    parse xml file
    store the complete information about docs
    call function to do tokenisation, stopping and stemming to title and text
    :param file_path:
    :param attri_list:
    :return: complete_id_attris_dict = {id: {attri:val}}, id_text_dict = {id:[text]}
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    # complete_id_attris_dict = {ID: attri_val_dict}
    complete_id_attris_dict = dict()

    # {ID: text}
    id_text_dict = dict()

    for doc in root.findall('DOC'):

        id = doc.find('ID').text
        title = ''
        main_text = ''
        date = None
        # attri_val_dict = {attribution: value}
        attri_val_dict = dict()

        for attr in attri_list:
            val = doc.find(attr).text
            attri_val_dict[attr] = val

            if attr == 'TITLE':
                title = text_process(val)
            elif attr == 'TEXT':
                main_text = text_process(val)
            elif attr == 'DATE':
                date = val

        text = title + main_text
        id_text_dict[id] = text
        complete_id_attris_dict[id] = attri_val_dict
        id_time_dict[id] = date

    return complete_id_attris_dict, id_text_dict, id_time_dict


def text_process(text):
    """
    mainly do tokenisation, stopping and stemming to title and text
    :param text: <string>
    :return: processed_text: <list>
    """
    # remove symbols
    pure = re.sub(r'[^A-Za-z0-9]+', ' ', text)
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
    """
    do indexing
    :param id_text_dict: {ID: text}
    :return: indexed_dict = {term: {id:[pos]}}
    """

    # indexing step 1: term sequence -> {term:id} invalid since multiple terms as the same key
    # [(term,id,pos),(...),...]
    list_of_term_id_pos_pair = []
    for key, value in id_text_dict.items():
        for pos in range(0, len(value)):
            list_of_term_id_pos_pair.append((value[pos], key, pos + 1))

    # indexing step 2: sort by term, then id
    # [(term_sorted,id,pos),(...),...]
    list_of_term_id_pos_pair_sorted = sorted(list_of_term_id_pos_pair)

    # indexing step 3: posting
    # { term1: {id1:[pos], id2:[pos]}, term2: {id1:[pos]}, id2:[pos]} }
    prev_term = list_of_term_id_pos_pair_sorted[0][0]
    prev_id = list_of_term_id_pos_pair_sorted[0][1]
    initial_pos = list_of_term_id_pos_pair_sorted[0][2]
    indexed_dict = {prev_term: {prev_id: [initial_pos]}}
    for item in list_of_term_id_pos_pair_sorted[1:]:
        term = item[0]
        id = item[1]
        pos = item[2]
        if term == prev_term:
            if id == prev_id:
                indexed_dict[term][id].append(pos)
            elif id != prev_id:
                indexed_dict[term][id] = [pos]
                prev_id = id
        elif term != prev_term:
            indexed_dict[term] = {id: [pos]}
            prev_term = term
            prev_id = 0  # refresh prev_id to an impossible value
    return indexed_dict


def form_term_id_tfidf_bm25(id_text_dict, indexed_dict):
    '''

    :param id_text_dict: dictionary: {id:[text]}
    :param indexed_dict: dictionary: {term:{id:pos}}
    :return: dictionary: {term: {id: (tfidf, bm25) }}
    '''

    # parameters for bm25
    k1 = 1.2
    b = 0.75
    dl_dict, avg_dl = get_document_length(id_text_dict)

    N = len(id_text_dict)  #number of documents
    term_id_tfidf_bm25_dict = copy.deepcopy(indexed_dict)

    for term in term_id_tfidf_bm25_dict.keys():
        df = len(term_id_tfidf_bm25_dict[term])

        for key in term_id_tfidf_bm25_dict[term].keys():
            tf = len(term_id_tfidf_bm25_dict[term][key])
            tfidf = (1 + np.log10(tf) * np.log10(N / df))
            bm25 = (tf*(k1+1)) / (tf + k1*(1-b+b*(dl_dict[key]/avg_dl))) * np.log10(1+(N-df)+0.5/(df+0.5))
            term_id_tfidf_bm25_dict[term][key] = (round(tfidf,4), round(bm25,4))

    return term_id_tfidf_bm25_dict


def get_document_length(id_text_dict):
    """
    get document's length
    :param id_text_dict: {id: [text]}
    :return: dl_dict: {id: length}, avg_dl: average
    """

    dl_dict = dict()
    tot_length = 0
    for id, text in id_text_dict.items():
        dl = len(text)
        dl_dict[id] = dl
        tot_length += dl
    avg_dl = tot_length / len(dl_dict)
    return dl_dict, avg_dl