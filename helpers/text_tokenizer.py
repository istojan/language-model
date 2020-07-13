import re
import os
import time
from configuration import NAME_JOKER_SIGN, NUMBER_JOKER_SIGN
from helpers.utils import get_elapsed_time

TEXT_TO_SENTENCES_REGEX = '([\w\s]{0,})[^\w\s]'
SENTENCE_TO_WORDS_REGEX = '([\w]{0,})'


def extract_all_sentences_from_files(source_directory):
    """
    Extract all sentences from all files located in a source directory.
    """

    start_time = time.time()

    sentences = list()
    files = os.listdir(source_directory)

    print("FilesCount={}, Message=\"Starting to extract sentences from files\"".format(len(files)))

    for file in files:
        if not file.endswith(".txt"):
            print("FileName={}, Message=\"Ignoring file with invalid structure. File extension needs to be .txt for sentences to be loaded\"".format(file))
            continue

        file_path = os.path.join(source_directory, file)

        sentences_file = extract_sentences(file_path)
        sentences.extend(sentences_file)

    print("ElapsedTime={}, FilesCount={}, TotalSentencesCount={}, "
          "Message=\"Finished extracting sentences from files\"".format(get_elapsed_time(start_time), len(files), len(sentences)))

    return sentences


def convert_sentences_to_list_of_words(sentences, names_set, keep_names = False):
    """
    For a given list of sentences, convert all sentences to a list of words. Optional is if we want to replace all
    names and digits with special joker characters so that they don't have a different meaning.
    We return a list of list of words where each word is in lower case.
    """

    start_time = time.time()
    print("SentencesCount={}, Message=\"Starting to convert sentences to lists of words\"".format(len(sentences)))

    sentences_to_words = list()

    for sentence in sentences:
        words = token_to_words(sentence)

        if keep_names:
            sentences_to_words.append(words)
        else:
            sentences_to_words.append([check_word_type(word, names_set) for word in words])

    print("ElapsedTime={}, SentencesCount={}, Message=\"Finished converting sentences to list of words\""
          .format(get_elapsed_time(start_time), len(sentences)))

    return sentences_to_words


def read_names(male_names_file_path, female_names_file_path):
    """
    Read both male and female names and return a set of names.
    The name files should follow the format of 1 name per line.
    """

    names = set()

    with open(male_names_file_path, "r") as f1:
        for name in f1:
            names.add(name.strip().lower())

    with open(female_names_file_path, "r") as f2:
        for name in f2:
            names.add(name.strip().lower())

    return names


def get_dictionary_words(dictionary_path):
    """
    Read a language dictionary of words and add all the words to a set for fast checking.
    """

    dictionary_words = set()

    with open(dictionary_path, "r") as f:
        for line in f:
            dictionary_words.add(line.strip().lower())

    return dictionary_words


def extract_sentences(file_path):
    """
    From a given file, extract all the sentences from it and return a list of sentences.
    """

    with open(file_path, "r") as file:

        lines = list()

        for line in file:
            line_stripped = line.strip()

            if line_stripped == "":
                continue

            lines.append(line_stripped)

        text = " ".join(lines)
        sentences = token_to_sentence(text)

        return sentences


def token_to_sentence(text):
    """
    From a given string (text), extract sentences by using a Regex and return a list of sentences.
    A sentence is defined as a continuous flow of words between 2 punctuation signs.
    Logically, this is not a correct definition of a sentence. It was done like this because in a lot of cases where
    punctuation signs are present, the meaning of the sentence can have a different meaning after the sign.
    """

    regex_of_sentence = re.findall(TEXT_TO_SENTENCES_REGEX, text)
    text_sentences = [x.strip() for x in regex_of_sentence if x is not '']

    return text_sentences


def token_to_words(sentence):
    """
    From a given sentence, extract a list of words using a regex and returns the list
    """

    regex_of_word = re.findall(SENTENCE_TO_WORDS_REGEX, sentence)

    words = [x.lower() for x in regex_of_word if x is not '']

    return words


def check_word_type(word, names_set):
    """
    From a given word and a set of names, check the word type and return a replacement word if necessary. Rules are:
    1. If word is a name, return joker sign for name. This is to be used for all names so they have the same meaning.
    2. If word is a digit, return joker sign for digit. Note: This can be extended to also check if the number is written with alphabetical characters.
    3. If the word doesn't match any of the above conditions, we return the word itself.
    """

    if word in names_set:
        return NAME_JOKER_SIGN
    elif word.isdigit():
        return NUMBER_JOKER_SIGN

    return word
