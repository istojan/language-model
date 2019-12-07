from text_helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words, read_names
from word_occurrences_model.word_occurrence_model_builder import build_word_occurrence_model
from language_model.language_model import LanguageModel
from os import path
from configuration import settings
import pickle
import time
import sys


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

    total_start_time = time.time()
    print("Message=\"Starting program for language model training.\"")

    if path.exists(settings["output_file_path"]):
        print("Message=\"Specified language model already exists, cancelling training and proceeding to load it.\"")
        language_model_data = load_language_model(settings["output_file_path"])
        language_model = LanguageModel()
        language_model.load_model_data(language_model_data)
    else:
        sentences = extract_all_sentences_from_files(settings["text_corpus_directory"])

        names_set = read_names(settings["male_names_file_path"], settings["female_names_file_path"])

        list_of_sentences_as_words = convert_sentences_to_list_of_words(sentences, names_set)

        sys.exit(0)
        # sentences = ["утрово изгреа сонце на исток", "ова сонце утрово изгреа на исток сега", "ех сестро"]

        word_occurrence_model = build_word_occurrence_model(settings["n_gram_level"], list_of_sentences_as_words)

        language_model = LanguageModel()
        language_model.build_language_model(word_occurrence_model)

        model_data = language_model.prepare_model_data_for_saving()
        save_language_model(model_data, settings["output_file_path"])

    language_model.test_language_model()

    print("TotalElapsedTime={}, Message=\"Program has finished.\"".format(format(time.time() - total_start_time, ".2f")))






