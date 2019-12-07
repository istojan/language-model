
class Node:

    def __init__(self, word):
        self.word = word
        self.word_count = 0
        self.children_nodes = dict()
        self.word_occurrence_count = dict()
        # self.words_occurrence_sorted_list = list()

    def add_occurrence(self, next_word):
        # print("Prev word: {}, Next word: {}, Adding occurence ".format(self.word, next_word))
        current_count = self.word_occurrence_count.get(next_word, 0)
        current_count += 1
        self.word_occurrence_count[next_word] = current_count

    def get_or_add_node(self, next_word):
        if next_word not in self.children_nodes:
            self.children_nodes[next_word] = Node(next_word)

        return self.children_nodes[next_word]

    # def trim_node(self, leave_count=1000):
    #     sorted_nodes = sorted(self.children_nodes, key=operator.attrgetter('word_count'), reverse=True)
    #     for node in sorted_nodes[leave_count:]:
    #         del self.children_nodes[node.word]