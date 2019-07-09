from text_helpers.text_tokenizer import extract_all_sentences_from_files
from word_occurrences_model.word_occurrence_model_builder import build_word_occurrence_model
from language_model.language_model import LanguageModel
from os import path
import pickle

INPUT_DIR = "text_corpus"
OUTPUT_FILE_PATH = 'output/language_model.pickle'

N_GRAM_LEVEL = 3


def load_language_model(path):
    with open(path, "rb") as pickle_file:
        language_model = pickle.load(pickle_file)
        return language_model


def save_language_model(language_model, path):
    with open(path, "wb") as pickle_file:
        pickle.dump(language_model, pickle_file)


if __name__ == '__main__':

    if path.exists(OUTPUT_FILE_PATH):
        print("Message=\"Specified language model already exists, cancelling training and proceeding to load it.\"")
        language_model = load_language_model(OUTPUT_FILE_PATH)
    else:
        sentences = extract_all_sentences_from_files(INPUT_DIR)

        # sentences = ["утрово изгреа сонце на исток", "ова сонце утрово изгреа на исток сега", "ех сестро"]

        word_occurrence_model = build_word_occurrence_model(N_GRAM_LEVEL, sentences)

        language_model = LanguageModel()
        language_model.build_language_model(word_occurrence_model)

        language_model.save_language_model(OUTPUT_FILE_PATH)

    language_model.test_language_model()






