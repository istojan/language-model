import time
from word_occurrences_model.word_occurrence_node import Node


def build_word_occurrence_model(n_gram_level, list_of_sentences_as_words):

    start_time = time.time()
    print("SentencesCount={}, Message=\"Starting to build word occurrence model from sentences\"".format(len(list_of_sentences_as_words)))

    word_combination_occurrences = dict()

    for words in list_of_sentences_as_words:

        sentence_word_count = len(words)

        for i in range(0, sentence_word_count, 1):

            current_word = words[i]

            if current_word not in word_combination_occurrences:
                word_combination_occurrences[current_word] = Node(current_word)

            current_word_combination = word_combination_occurrences[current_word]
            current_word_combination.word_count += 1

            for n_gram_step in range(1, n_gram_level):
                if i + n_gram_step >= sentence_word_count:
                    # current_word_combination.mark_as_last
                    break

                next_word = words[i+n_gram_step]

                current_word_combination.add_occurrence(next_word)
                current_word_combination = current_word_combination.get_or_add_node(next_word)
                current_word_combination.word_count += 1

    print("ElapsedTime={}s, SentencesCount={}, Message=\"Finished building word occurrence model from sentences\"".format(format(time.time() - start_time, ".2f"), len(list_of_sentences_as_words)))

    return word_combination_occurrences
