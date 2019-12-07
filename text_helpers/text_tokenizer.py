import re
import os
import time
from configuration import NAME_JOKER_SIGN, NUMBER_JOKER_SIGN

TEXT_TO_SENTENCES_REGEX = '([\w\s]{0,})[^\w\s]'
SENTENCE_TO_WORDS_REGEX = '([\w]{0,})'


def extract_all_sentences_from_files(dir_location):
    """
    Extract all sentences from files located in given directory.
    :param dir_location:
    :return: a list of sentences
    """
    start_time = time.time()

    sentences = list()
    files = os.listdir(dir_location)

    print("FilesCount={}, Message=\"Starting to extract sentences from files\"".format(len(files)))

    for file in files:
        if not file.endswith(".txt"):
            print("FileName={}, Message=\"Ignoring file with invalid structure.\"".format(file))
            continue
        file_path = os.path.join(dir_location, file)

        sentences_file = extract_sentences(file_path)
        sentences.extend(sentences_file)

        # print("File_Path={}, SentecesCount={}, Message=\"Extracted sentences from file.\"".format(file_path, len(sentences_file)))

    print("ElapsedTime={}s, FilesCount={}, TotalSentencesCount={}, Message=\"Finished extracting sentences from files\"".format(format(time.time() - start_time, ".2f"), len(files), len(sentences)))

    return sentences


def convert_sentences_to_list_of_words(sentences, names_set, keep_names = False):

    start_time = time.time()
    print("SentencesCount={}, Message=\"Begin converting sentences to list of words\"".format(len(sentences)))

    sentences_to_words = list()

    for sentence in sentences:
        words = token_to_words(sentence)

        if keep_names:
            sentences_to_words.append(words)
        else:
            sentences_to_words.append([check_word_type(word, names_set) for word in words])

    print("ElapsedTime={}s, SentencesCount={}, Message=\"Finished converting sentences to list of words\"".format(format(time.time() - start_time, ".2f"), len(sentences)))

    return sentences_to_words


def read_names(male_names_file_path, female_names_file_path):

    names = set()

    with open(male_names_file_path, "r") as f1:
        for name in f1:
            names.add(name.strip().lower())

    with open(female_names_file_path, "r") as f2:
        for name in f2:
            names.add(name.strip().lower())

    return names


def read_mk_dictionary(dictionary_path):

    dictionary_words = set()

    with open(dictionary_path, "r") as f:
        for line in f:
            dictionary_words.add(line.strip().lower())

    return dictionary_words


def extract_sentences(file_path):
    """
    A function that reads a file line by line, extracts sentences from each line and returns them back in a list.
    :param file_path: a file_path to a file we want to read
    :return: a list of sentences (a definition of sentence is described above
    """

    all_sentences = list()

    with open(file_path, "r") as file:

        for line in file:
            line_stripped = line.strip()

            if line_stripped == "":
                continue

            sentences = token_to_sentence(line_stripped)
            all_sentences.extend(sentences)

    return all_sentences


def token_to_sentence(text):
    """
    A function that from a given string (text) extracts sentences by using a Regex and returns a list of sentences.
    A sentence is defined as a continuous flow of words between 2 punctuation signs. Even though this is not a correct
    definition of a sentence, it's the best way if it is used in a language model.
    :param text: a string that we want to extract sentences from
    :return: a list of sentences
    """

    regex_of_sentence = re.findall(TEXT_TO_SENTENCES_REGEX, text)
    text_sentences = [x.strip() for x in regex_of_sentence if x is not '']

    return text_sentences


def token_to_words(sentence):
    """
    A function that from a given sentence extracts a list of words using a regex and returns the list
    :param sentence: a string that represents 1 sentence
    :return: a list of words from the sentence
    """

    regex_of_word = re.findall(SENTENCE_TO_WORDS_REGEX, sentence)

    words = [x.lower() for x in regex_of_word if x is not '']

    return words


def check_word_type(word, names_set):

    if word in names_set:
        return NAME_JOKER_SIGN
    elif word.isdigit():
        return NUMBER_JOKER_SIGN

    return word


contains_ascii_letter = re.compile('[a-zA-Z]').search


contains_digit = re.compile("\d").search


contains_non_cyrillic_character = re.compile('[^а-шА-Ш]').search