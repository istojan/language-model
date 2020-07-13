import time
from word_occurrences_model.word_occurrence_node import Node
from helpers.text_tokenizer import get_dictionary_words
from helpers.utils import get_elapsed_time
from configuration import settings


def build_word_occurrence_model(list_of_sentences_as_words):
    """
    For a given list of sentences represented as a list of words, build a word occurrences model. The depth of the model
    should depend from the setting 'n_gram_level'.
    The building of the model has 2 phases:
    1. Create the model using all the sentences.
    2. Trim the model in order to reduce the size of the model and to cut down noisy data.
    The word occurrences model will be represented as a dictionary where keys are the first level words are values are
    Node objects.
    """

    n_gram_level = settings["n_gram_level"]

    start_time = time.time()
    print("SentencesCount={}, Message=\"Starting to build word occurrence model\"".format(len(list_of_sentences_as_words)))

    word_occurrences_model = create_word_occurrence_model(n_gram_level, list_of_sentences_as_words)

    word_occurrences_model = trim_word_occurrences_model(word_occurrences_model)

    print("ElapsedTime={}s, SentencesCount={}, Message=\"Finished building word occurrence model\""
          .format(get_elapsed_time(start_time), len(list_of_sentences_as_words)))

    return word_occurrences_model


def create_word_occurrence_model(n_gram_level, list_of_sentences_as_words):
    """
    Create an n-gram word occurrences model represented as a tree. We will only consider words that are valid by using
    the dictionary of words.
    """

    start_time = time.time()
    print("SentencesCount={}, Message=\"Starting to create base word occurrence model from sentences\"".format(len(list_of_sentences_as_words)))

    word_occurrences_model = dict()

    mk_dictionary = get_dictionary_words(settings["dictionary_file_path"])

    for words in list_of_sentences_as_words:

        sentence_word_count = len(words)

        for index, current_word in enumerate(words, start=0):
            if current_word not in mk_dictionary:
                continue

            if current_word not in word_occurrences_model:
                word_occurrences_model[current_word] = Node(current_word)

            current_word_combination = word_occurrences_model[current_word]
            current_word_combination.word_count += 1

            for n_gram_step in range(1, n_gram_level):
                if index + n_gram_step >= sentence_word_count:
                    break

                next_word = words[index+n_gram_step]

                if next_word not in mk_dictionary:
                    break

                current_word_combination.add_occurrence(next_word)
                current_word_combination = current_word_combination.get_or_add_node(next_word)
                current_word_combination.word_count += 1

    print("ElapsedTime={}, SentencesCount={}, Message=\"Finished creating base word occurrence model from sentences\""
          .format(get_elapsed_time(start_time), len(list_of_sentences_as_words)))

    return word_occurrences_model


def trim_word_occurrences_model(word_occurrences_model):
    """
    TODO:
    """

    start_time = time.time()
    print("BaseLevelNodes={}, Message=\"Starting to trim base word occurrence model\"".format(len(word_occurrences_model)))

    total_nodes, trimmed_nodes = trim_nodes(word_occurrences_model, 10)

    print("ElapsedTime={}, OriginalNodeCount={}, TrimmedNodes={}, UpdatedBaseLevelNodes={}, Message=\"Finished trimming word occurrence model\""
          .format(get_elapsed_time(start_time), total_nodes, trimmed_nodes, len(word_occurrences_model)))

    return word_occurrences_model


def trim_nodes(word_to_node_map, trim_level):

    total_nodes = 0
    trimmed_nodes = 0

    nodes_to_trim = list()

    for word_occurrence_node in word_to_node_map.values():
        total_nodes = total_nodes + 1

        if word_occurrence_node.word_count < trim_level:
            nodes_to_trim.append(word_occurrence_node.word)
            trimmed_nodes = trimmed_nodes + 1

        if word_occurrence_node.children_nodes:
            total_sub_nodes, trimmed_sub_nodes = trim_nodes(word_occurrence_node.children_nodes, 2)

            total_nodes = total_nodes + total_sub_nodes
            trimmed_nodes = trimmed_nodes + trimmed_sub_nodes

    for child_word_to_remove in nodes_to_trim:
        del word_to_node_map[child_word_to_remove]
        # TODO: check if word_count should be updated

    return total_nodes, trimmed_nodes
