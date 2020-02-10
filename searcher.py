from nltk.corpus import wordnet
from itertools import chain
from autocorrect import spell
from indexer import text_process
import re
from collections import defaultdict


class SearchModule(object):
    def __init__(self, indexed_dict=None, term_id_tfidf_bm25_dict=None, id_time_dict=None):
        self.indexed_dict = indexed_dict
        self.term_id_tfidf_bm25_dict = term_id_tfidf_bm25_dict
        self.id_time_dict = id_time_dict
        self.search_query = None
        self.glove_model = None

    def get_search_query(self, search_query):
        self.search_query = search_query

    def get_glove_model(self, glove_model):
        self.glove_model = glove_model

    def conduct_search(self):
        """
        conduct search and rank search results with distance, time, and tf-idf(bm25) factors
        :return: search_result_list: a list of ranked ids [id1, id2, ...]
        """
        corrected_query = spell(self.search_query)
        # todo: stem ???
        # ori_word_set = set(corrected_query.lower())

        word_set = set(text_process(corrected_query))

        if word_set:
            # a ranked search result list from most relevant to least
            search_result_list = list()

            # start to do exact search
            same_id_set = self.get_same_id_set(word_set)
            if same_id_set:
                # {id: final_score}
                id_final_score_dict = self.get_final_score(same_id_set, word_set)
                # [(id, final_score)]   sorted by final_score from high to low, append id to search result list
                sorted_id_list = sorted(id_final_score_dict.items(), key=lambda d: d[1], reverse=True)
                for id, score in sorted_id_list:
                    if id not in search_result_list:
                        search_result_list.append(id)

            #  then do synonym search
            comb_list = find_synonyms_search_comb(word_set)
            id_score_sum_dict = defaultdict(float)
            for comb in comb_list:
                comb = set(comb)
                same_id_set = self.get_same_id_set(comb)
                if same_id_set:
                    id_final_score_dict = self.get_final_score(same_id_set, comb)
                    for id, score in id_final_score_dict:
                        id_score_sum_dict[id] += score
            sorted_id_list = sorted(id_score_sum_dict.items(), key=lambda d: d[1], reverse=True)
            for id, score in sorted_id_list:
                if id not in search_result_list:
                    search_result_list.append(id)

            # if No. results is still less than 100, do single word search
            if len(search_result_list) < 100:
                id_shit_dict = defaultdict()
                for word in word_set:
                    same_id_set = self.get_same_id_set({word})
                    id_shit_dict += self.get_final_score(same_id_set, {word})
                sorted_id_list = sorted(id_shit_dict.items(), key=lambda d: d[1], reverse=True)
                for id, score in sorted_id_list:
                    if id not in search_result_list:
                        search_result_list.append(id)

            return search_result_list
        else:
            print('Search query is too simple!')
            return []

    def get_same_id_set(self, word_set):
        """
        search every word separately and return the same doc id set
        :param word_set: {word}
        :return: same_id_set: {doc_id}
        """
        same_id_set = set()
        word_list = list(word_set)

        i = 0

        # try to find a non-empty initial same_id_set
        while not same_id_set:
            try:
                same_id_set = set(self.indexed_dict[word_list[i]].keys())
            except Exception as error:
                if error == KeyError:
                    i += 1
                elif error == IndexError:
                    return set()
        # then to find intersection set
        for word in word_list[i + 1:]:
            try:
                doc_id = set(self.indexed_dict[word].keys())
                same_id_set = same_id_set & doc_id
            except KeyError:
                i += 1
        return same_id_set

    def get_final_score(self, same_id_set, word_set):
        """
        :param same_id_set: {id}
        :param word_set: {word}
        :return: {id: score}
        """
        # three dict:  1. {id: max length} 2. {id: '20200202'} 3. {id: rank score}
        id_lenfac_dict = self.get_length_factor(same_id_set, word_set)
        id_timefac_dict = self.get_time_factor(same_id_set)
        id_rankalgofac_dict = self.get_rankalgo_factor(same_id_set, word_set, mode='tfidf')

        id_final_score_dict = dict()
        for id in id_timefac_dict.keys():
            id_final_score_dict[id] = id_lenfac_dict[id] * id_timefac_dict[id] * id_rankalgofac_dict[id]
        return id_final_score_dict

    def get_length_factor(self, same_id_set, word_set):
        """
        :param same_id_set: {id}
        :param word_set: {word}
        :return: {id: length of continuous number}
        """
        pos_list = list()
        id_lenfac_dict = dict()
        for doc_id in same_id_set:
            for word in word_set:
                pos_list += self.indexed_dict[word][doc_id]
            length = get_longest_streak(pos_list)
            id_lenfac_dict[doc_id] = 1 + 0.1 * length
        return id_lenfac_dict

    def get_time_factor(self, same_id_set):
        """
        :param same_id_set: {id}
        :param word_set: {word}
        :return: {id: time_factor}
        """
        id_time_dict = dict()
        for doc_id in same_id_set:
            id_time_dict[doc_id] = int(re.sub('-', '', self.id_time_dict[doc_id]))  # 2020-02-02 -> 20200202

        time_list = sorted(id_time_dict.values(), reverse=True)
        date_rank = {}
        i = 1
        m = len(time_list)
        date_rank[time_list[0]] = 0
        cnt = 0
        id_timefac_dict = {}  # {id:rank}
        while i < m - 1:
            if time_list[i] < time_list[i - 1]:
                cnt += 1
                date_rank[time_list[i]] = cnt
            else:
                date_rank[time_list[i]] = cnt
            i += 1
        for id in id_time_dict.keys():
            # {id: 1/(0.2*rank+1)}
            id_timefac_dict[id] = 1 / (0.1 * date_rank[id_time_dict[id]] + 1)
        return id_timefac_dict

    def get_rankalgo_factor(self, same_id_set, word_set, mode):
        """
        :param mode: 'tfidf' or 'bm25'
        :param same_id_set: {id}
        :param word_set: {word}
        :return: {id: bm25}
        """
        id_rankalgofac_dict = defaultdict(int)
        for doc_id in same_id_set:
            for term in word_set:
                # term_id_tfidf_bm25_dict = {term: {id: (tfidf, bm25) }}
                if mode == 'tfidf':
                    id_rankalgofac_dict[doc_id] += self.term_id_tfidf_bm25_dict[term][doc_id][0]
                elif mode == 'bm25':
                    id_rankalgofac_dict[doc_id] += self.term_id_tfidf_bm25_dict[term][doc_id][1]
        return id_rankalgofac_dict


def find_synonyms_search_comb(word_set):
    """
    :param word_set: target
    :return: comb_list: <list>
    """
    synonym_comb_list = list()
    for word in word_set:
        synonyms_list = []
        wsets = wordnet.synsets(word)
        synonyms_list += chain.from_iterable([i.lemma_names() for i in wsets])
        sub = set(word_set) - {word}
        for synonym in synonyms_list:
            synonym_comb_list.append(list(sub) + [synonym])

    # todo: remove repeated and redundant combs like XXX_oriWord_XXX, add max number limitation
    # todo: text_process the combs

    return synonym_comb_list


def find_similar_search_comb(word_set, glove_model):
    """
    :param glove_model: needed
    :param word_set: {'chinese', 'food'}
    :return: [[combination of word]] such as [['chinese', 'products'], ['taiwanese', 'food']]
    """
    block_list = list()
    try:
        for word in word_set:
            res = glove_model.most_similar(positive=word)
    except KeyError:
        block_list.append(word)

    filtered_word_set = word_set - set(block_list)
    similar_comb_list = list()
    for word in filtered_word_set:
        similar_word_list = [i[0] for i in glove_model.most_similar(positive=word) if i[1] > 0.7]
        sub = set(filtered_word_set) - {word}
        for similar_word in similar_word_list:
            similar_comb_list.append(list(sub) + [similar_word])

    # todo: adjust positions and remove repeated combinations, and reserve only 10

    return similar_comb_list


def get_longest_streak(pos_list):
    longest_streak = 0
    num_set = set(pos_list)

    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak
