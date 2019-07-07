
class ProbabilityNode:

    def __init__(self, word, word_count):
        self.word = word
        self.word_count = word_count
        self.probability = 0.0
        self.children_nodes = dict()
        self.sorted_probability_nodes = list()

    def calculate_probability(self, total_words_count):
        self.probability = self.word_count / total_words_count
