
class Node:

    def __init__(self, word):
        self.word = word
        self.word_count = 0
        self.children_nodes = dict()
        self.word_occurrence_count = dict()

    def add_occurrence(self, next_word):
        """
        For a given next word in the tree, update the child node occurrence word count.
        If this is the first occurrence of the word in the subtree, we set the count to 1.
        """

        current_count = self.word_occurrence_count.get(next_word, 0)
        current_count += 1
        self.word_occurrence_count[next_word] = current_count

    def get_or_add_node(self, next_word):
        """
        For a given next word in the tree, return the child node for it.
        If no node exists since this is the first occurrence of the new word in this subtree, create a node for it.
        """

        if next_word not in self.children_nodes:
            self.children_nodes[next_word] = Node(next_word)

        return self.children_nodes[next_word]

    # def trim_node(self, leave_count=1000):
    #     sorted_nodes = sorted(self.children_nodes, key=operator.attrgetter('word_count'), reverse=True)
    #     for node in sorted_nodes[leave_count:]:
    #         del self.children_nodes[node.word]