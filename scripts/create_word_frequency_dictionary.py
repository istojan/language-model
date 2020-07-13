import os
from configuration import settings
from helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words, read_names


def convert_dictionary_to_word_frequency_dictionary(dictionary_path, corpus_directory):

    sentences = extract_all_sentences_from_files(corpus_directory)
    names = read_names(settings["male_names_file_path"], settings["female_names_file_path"])

    sentences_as_words = convert_sentences_to_list_of_words(sentences, names, keep_names=False)

    for words in sentences_as_words:
        pass

if __name__ == "__main__":
    pass


