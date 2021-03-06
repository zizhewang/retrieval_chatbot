# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from retrieval_documents import Retrieval
from fuzzy_match import fuzzy_matching
from tf_idf import TfIdf
import config

# TODO: distribute message by threading or tornado

NUM_OF_IR = 10
MODEL_PATH = []

class Agent:
    def __init__(self):
        self.config = config
        self.init_all_states()

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=10, config=self.config)
        self.tf_idf = TfIdf(config)

    def get_utterance_type(self, utterance):    # TODO get correct file name by utterance
        return "AI"    # return file_name

    def start(self):
        while True:
            utterance = input(">>>")
            file_name = self.get_utterance_type(utterance)
            # index_path = self.config[file_name]
            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance)
            fuzzy_ratio_ls = fuzzy_matching(utterance, context_ls)

            # TODO tf-idf
            self.tf_idf.select_model(file_name)
            self.tf_idf.predict_tfidf(utterance, context_ls)
            tf_idf_score_ls = self.tf_idf.calculate_distances()
            final_score_ls = [(fuzzy_ratio*0.6 + tf_tdf_score*0.4) for fuzzy_ratio,tf_tdf_score in zip(fuzzy_ratio_ls, tf_idf_score_ls)]
            best_index = final_score_ls.index(max(final_score_ls))
            print("<<<{}".format(context_ls[best_index][1]))

if __name__ == '__main__':
    agent = Agent()
    agent.start()
