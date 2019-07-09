from operator import attrgetter
import pickle
from language_model.probability_node import ProbabilityNode


class LanguageModel:

    def __init__(self):
        self.total_words_count = 0
        self.probability_nodes = dict()
        self.sorted_probabiliy_nodes = list()

    def build_language_model(self, word_occurrences_model):

        print("Starting language model training")

        for word, word_occurrence_node in word_occurrences_model.items():
            word_count = word_occurrence_node.word_count
            self.total_words_count += word_count

            probability_node = self.build_word_occurrence_probability_node(word, word_count, word_occurrence_node.children_nodes)
            self.probability_nodes[word] = probability_node

        print("Total words count: {}".format(self.total_words_count))
        print("Total distinct words count: {}".format(len(self.probability_nodes)))

        self.calculate_nodes_probability(self.probability_nodes, self.total_words_count)
        self.sorted_probability_nodes = sort_probability_list(self.probability_nodes.values())

        print("Language model training has finished")

    def build_word_occurrence_probability_node(self, word, word_count, word_occurrences):

        probability_node = ProbabilityNode(word, word_count)

        if len(word_occurrences) == 0:
            return probability_node

        for word, word_occurrences_node in word_occurrences.items():
            word_count = word_occurrences_node.word_count
            probability_node.word_count += word_count

            child_probability_node = self.build_word_occurrence_probability_node(word, word_count, word_occurrences_node.children_nodes)
            probability_node.children_nodes[word] = child_probability_node

        self.calculate_nodes_probability(probability_node.children_nodes, probability_node.word_count)

        probability_node.sorted_probability_nodes = sort_probability_list(probability_node.children_nodes.values())

        return probability_node

    def calculate_nodes_probability(self, probability_nodes, total_words_count):
        for word, probability_node in probability_nodes.items():
            probability_node.calculate_probability(total_words_count)

    def test_language_model(self):
        print([ [node.word, node.probability] for node in self.sorted_probability_nodes[:5]])
        for node2 in self.sorted_probability_nodes[:5]:
            print("Word: {}, Count: {}, Prob: {}, Children: {}, ProbChildren: {}".format(node2.word, node2.word_count, node2.probability, len(node2.children_nodes), len(node2.sorted_probability_nodes)))
            print([[node.word, node.probability] for node in node2.sorted_probability_nodes[:5]])

    def save_language_model(self, path):
        pickle_file = open(path, 'wb')
        pickle.dump(self, pickle_file)

def sort_probability_list(probability_nodes):
    sorted_probability_nodes = sorted(probability_nodes, key=attrgetter("probability"), reverse=True)
    return sorted_probability_nodes