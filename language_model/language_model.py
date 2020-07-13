import time
from operator import attrgetter
from language_model.probability_node import ProbabilityNode
from helpers.utils import get_elapsed_time


class LanguageModel:

    def __init__(self):
        self.total_words_count = 0
        self.probability_nodes = dict()
        self.sorted_probability_nodes = list()

    def build_language_model(self, word_occurrences_model):
        """
        From a given word occurrences model, build a probability language model.
        """

        start_time = time.time()
        print("Message=\"Starting to train a language model from a word occurrences model\"")

        for word, word_occurrence_node in word_occurrences_model.items():
            word_count = word_occurrence_node.word_count
            self.total_words_count += word_count

            probability_node = self.build_word_occurrence_probability_node(word, word_count, word_occurrence_node.children_nodes)
            self.probability_nodes[word] = probability_node

        self.calculate_nodes_probability(self.probability_nodes, self.total_words_count)
        self.sorted_probability_nodes = sort_probability_list(self.probability_nodes.values())

        print("ElapsedTime={}, TotalWordsCount={}, TotalDistinctWordsCount={}, Message=\"Finished training language model from word occurrences model\""
              .format(get_elapsed_time(start_time), self.total_words_count, len(self.probability_nodes)))

    def build_word_occurrence_probability_node(self, base_word, base_word_count, children_word_occurrences):

        probability_node = ProbabilityNode(base_word, base_word_count)

        if len(children_word_occurrences) == 0:
            return probability_node

        for child_word, word_occurrences_node in children_word_occurrences.items():
            child_word_count = word_occurrences_node.word_count
            probability_node.word_count += child_word_count

            child_probability_node = self.build_word_occurrence_probability_node(child_word, child_word_count, word_occurrences_node.children_nodes)
            probability_node.children_nodes[child_word] = child_probability_node

        self.calculate_nodes_probability(probability_node.children_nodes, probability_node.word_count)

        probability_node.sorted_probability_nodes = sort_probability_list(probability_node.children_nodes.values())
        # keep only top 1000 sorted probability nodes
        # probability_node.sorted_probability_nodes = probability_node.sorted_probability_nodes[:1000]

        return probability_node

    def calculate_nodes_probability(self, children_probability_nodes, total_words_count):

        for word, probability_node in children_probability_nodes.items():
            probability_node.calculate_probability(total_words_count)

    def prepare_model_data_for_saving(self):
        return [self.total_words_count, self.probability_nodes, self.sorted_probability_nodes]


def sort_probability_list(probability_nodes):
    sorted_probability_nodes = sorted(probability_nodes, key=attrgetter("probability"), reverse=True)
    return sorted_probability_nodes
