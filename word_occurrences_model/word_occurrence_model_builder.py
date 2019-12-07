import re
import time
from word_occurrences_model.word_occurrence_node import Node
from text_helpers.text_tokenizer import contains_ascii_letter, contains_digit, contains_non_cyrillic_character, read_mk_dictionary
from configuration import settings


def build_word_occurrence_model(n_gram_level, list_of_sentences_as_words):

    start_time = time.time()
    print("SentencesCount={}, Message=\"Starting to build word occurrence model from sentences\"".format(len(list_of_sentences_as_words)))

    word_combination_occurrences = dict()

    mk_dictionary = read_mk_dictionary(settings["dictionary_file_path"])

    for words in list_of_sentences_as_words:

        sentence_word_count = len(words)

        for index, current_word in enumerate(words, start=0):
        # for i in range(0, sentence_word_count, 1):

            # current_word = words[i]

            # if contains_ascii_letter(current_word) or contains_digit(current_word):
            if current_word not in mk_dictionary:
                continue

            if current_word not in word_combination_occurrences:
                word_combination_occurrences[current_word] = Node(current_word)

            current_word_combination = word_combination_occurrences[current_word]
            current_word_combination.word_count += 1

            for n_gram_step in range(1, n_gram_level):
                if index + n_gram_step >= sentence_word_count:
                    # current_word_combination.mark_as_last
                    break

                next_word = words[index+n_gram_step]

                # if contains_digit(next_word) or contains_ascii_letter(next_word):
                #     # print("Skipping as ascii or number present: {}".format(next_word))
                #     break
                if next_word not in mk_dictionary:
                    break

                current_word_combination.add_occurrence(next_word)
                current_word_combination = current_word_combination.get_or_add_node(next_word)
                current_word_combination.word_count += 1

    print("ElapsedTime={}s, SentencesCount={}, Message=\"Finished building word occurrence model from sentences\"".format(format(time.time() - start_time, ".2f"), len(list_of_sentences_as_words)))

    return word_combination_occurrences


# def trim_word_occurrence_model_tree(word_combination_occurrences):
#
#     start_time = time.time()
#     print("FirstLevelNodesCount={}, Message=\"Starting to trim word occurrence model\"".format(len(word_combination_occurrences)))
#
#     for node in word_combination_occurrences.values():




