from helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words, read_names
from helpers.utils import get_elapsed_time
from word_occurrences_model.word_occurrence_model_builder import build_word_occurrence_model
from language_model.language_model import LanguageModel
from os import path
from configuration import settings
import pickle
import time
import sys


def save_language_model(language_model_data, path):
    """
    Saves the language model in a pickle file to be later used by the language model service.
    """

    start_time = time.time()
    print("Message=\"Starting to save language model\"")

    with open(path, "wb") as pickle_file:
        pickle.dump(language_model_data, pickle_file)

    print("ElapsedTime={}, Message=\"Finished saving language model.\"".format(get_elapsed_time(start_time)))


if __name__ == '__main__':

    model_name = settings["output_file_path"]

    if path.exists(model_name):
        print("ModelName=\"{}\", Message=\"A language model with specified name already exists. Use a different name or delete the old model\"".format(model_name))
        sys.exit(0)

    start_time = time.time()
    print("ModelName=\"{}\", Message=\"Starting language model training\"".format(model_name))

    sentences = extract_all_sentences_from_files(settings["text_corpus_directory"])

    # TODO: Delete
    print(sentences[:20])

    names_set = read_names(settings["male_names_file_path"], settings["female_names_file_path"])

    list_of_sentences_as_words = convert_sentences_to_list_of_words(sentences, names_set)

    word_occurrence_model = build_word_occurrence_model(list_of_sentences_as_words)

    language_model = LanguageModel()
    language_model.build_language_model(word_occurrence_model)

    model_data = language_model.prepare_model_data_for_saving()
    save_language_model(model_data, model_name)

    print("TotalElapsedTime={}, ModelName=\"{}\", Message=\"Finished language model training\"".format(get_elapsed_time(start_time), model_name))
