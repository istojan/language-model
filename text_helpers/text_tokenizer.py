import re
import os
import time


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
        file_path = os.path.join(dir_location, file)

        sentences_file = token_to_sentence(file_path)
        sentences.extend(sentences_file)

        # print("File_Path={}, SentecesCount={}, Message=\"Extracted sentences from file.\"".format(file_path, len(sentences_file)))

    print("ElapsedTime={}s, FilesCount={}, TotalSentencesCount={}, Message=\"Finished extracting sentences from files\"".format(format(time.time() - start_time, ".2f"), len(files), len(sentences)))

    return sentences


def convert_sentences_to_list_of_words(sentences):

    start_time = time.time()
    print("SentencesCount={}, Message=\"Begin converting sentences to list of words\"".format(len(sentences)))

    sentences_to_words = list()

    for sentence in sentences:
        sentences_to_words.append(token_to_words(sentence))

    print("ElapsedTime={}s, SentencesCount={}, Message=\"Finished converting sentences to list of words\"".format(format(time.time() - start_time, ".2f"), len(sentences)))

    return sentences_to_words


def token_to_sentence(file_path):
    """
    A function that reads a file, extracts all sentences from it and returns them back in a list.
    A sentence is defined as a continuous flow of words between 2 punctuation signs. Even though this is not a correct
    definition of a sentence, it's the best way if it is used in a language model.
    :param file_path: a file_path to a file we want to read
    :return: a list of sentences (a definition of sentence is described above
    """

    sentences = list()

    regex = '([\w\s]{0,})[^\w\s]'

    with open(file_path, "r") as file:

        for line in file:
            line_stripped = line.strip()

            if line_stripped == "":
                continue

            regex_of_sentence = re.findall(regex, line)
            line_sentences = [x.strip() for x in regex_of_sentence if x is not '']

            sentences.extend(line_sentences)

    return sentences


def token_to_words(sentence):
    """

    :param sentence:
    :return:
    """

    regex = '([\w]{0,})'
    regex_of_word = re.findall(regex, sentence)

    words = [x.lower() for x in regex_of_word if x is not '']

    return words
