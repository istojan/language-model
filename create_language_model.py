from text_helpers.text_tokenizer import extract_all_sentences_from_files
from word_occurrences_model.word_occurrence_model_builder import build_word_occurrence_model
from language_model.language_model import LanguageModel

INPUT_DIR = "text_corpus"

N_GRAM_LEVEL = 3


def print_model(word_occurrence_model):
    print(word_occurrence_model)
    for word in word_occurrence_model.keys():
        # print(word + " - " + WORD_COMBINATION_OCCURENCES[word])
        #if WORD_COMBINATION_OCCURENCES[word].word_count < 1000:
        #    continue

        print("### {} {}".format(word_occurrence_model[word].word_count, word))
        print_level(word_occurrence_model[word], " ")


def print_level(word_occurrences, prefix):

    for child_node in word_occurrences.children_nodes.values():
        print(prefix + str(word_occurrences.word_occurrence_count[child_node.word]) + " " + child_node.word)
        print_level(child_node, prefix + " ")


if __name__ == '__main__':

    sentences = extract_all_sentences_from_files(INPUT_DIR)

    # sentences = ["утрово изгреа сонце на исток", "ова сонце утрово изгреа на исток сега", "ех сестро"]

    word_occurrence_model = build_word_occurrence_model(N_GRAM_LEVEL, sentences)

    # print_model(word_occurrence_model)

    language_model = LanguageModel()
    language_model.build_language_model(word_occurrence_model)

    language_model.save_language_model()






