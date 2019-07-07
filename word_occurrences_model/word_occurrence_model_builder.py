from text_helpers.text_tokenizer import token_to_words
from word_occurrences_model.word_occurrence_node import Node


def build_word_occurrence_model(n_gram_level, sentences):

    word_combination_occurrences = dict()

    for sentence in sentences:
        words = token_to_words(sentence)

        for i in range(0, len(words), 1):

            current_word = words[i]

            if current_word not in word_combination_occurrences:
                word_combination_occurrences[current_word] = Node(current_word)

            current_word_combination = word_combination_occurrences[current_word]
            current_word_combination.word_count += 1

            for n_gram_step in range(1, n_gram_level):
                if i + n_gram_step >= len(words):
                    break

                next_word = words[i+n_gram_step]

                current_word_combination.add_occurrence(next_word)
                current_word_combination = current_word_combination.get_or_add_node(next_word)
                current_word_combination.word_count += 1

    return word_combination_occurrences
