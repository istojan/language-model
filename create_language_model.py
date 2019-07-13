from text_helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words
from word_occurrences_model.word_occurrence_model_builder import build_word_occurrence_model
from language_model.language_model import LanguageModel
from os import path
import pickle
import time

INPUT_DIR = "big_corpus"
OUTPUT_FILE_PATH = 'output/language_model_2M_rows.pickle'

N_GRAM_LEVEL = 3


def load_language_model(path):
    with open(path, "rb") as pickle_file:
        language_model = pickle.load(pickle_file)
        return language_model


def save_language_model(language_model_data, path):

    start_time = time.time()
    print("Message=\"Starting to save language model.\"")

    with open(path, "wb") as pickle_file:
        pickle.dump(language_model_data, pickle_file)

    print("ElapsedTime={}, Message=\"Finished saving language model.\"".format(format(time.time() - start_time, ".2f")))

if __name__ == '__main__':

    start_time = time.time()
    print("Message=\"Starting program for language model training.\"")

    if path.exists(OUTPUT_FILE_PATH):
        print("Message=\"Specified language model already exists, cancelling training and proceeding to load it.\"")
        language_model_data = load_language_model(OUTPUT_FILE_PATH)
        language_model = LanguageModel()
        language_model.load_model_data(language_model_data)
    else:
        sentences = extract_all_sentences_from_files(INPUT_DIR)

        list_of_sentences_as_words = convert_sentences_to_list_of_words(sentences)

        # sentences = ["утрово изгреа сонце на исток", "ова сонце утрово изгреа на исток сега", "ех сестро"]

        word_occurrence_model = build_word_occurrence_model(N_GRAM_LEVEL, list_of_sentences_as_words)

        language_model = LanguageModel()
        language_model.build_language_model(word_occurrence_model)

        model_data = language_model.prepare_model_data_for_saving()
        save_language_model(model_data, OUTPUT_FILE_PATH)

    language_model.test_language_model()

    print("TotalElapsedTime={}, Message=\"Program has finished.\"".format(format(time.time() - start_time, ".2f")))






