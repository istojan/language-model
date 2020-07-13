import time
from helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words, get_dictionary_words
from operator import itemgetter


INPUT_DIR = "../big_corpus"
MK_DICTIONARY_PATH = "../other/macedonian-dict"


def extract_difference_words():

    start_time = time.time()
    print("Message=\"Starting script to extract words present in text corpus, but not in macedonian dictionary\"")

    sentences = extract_all_sentences_from_files(INPUT_DIR)

    sentences_as_list_words = convert_sentences_to_list_of_words(sentences, set(), True)

    dictionary_words = get_dictionary_words(MK_DICTIONARY_PATH)

    difference_words = dict()

    for words in sentences_as_list_words:

        for word in words:
            if word in dictionary_words:
                continue

            word_count = difference_words.get(word, 0)
            word_count = word_count + 1

            difference_words[word] = word_count

    difference_words_as_list = [[word, word_count] for word, word_count in difference_words.items()]

    difference_words_as_list = sorted(difference_words_as_list, key=itemgetter(1), reverse=True)

    with open("difference_words.txt", "w") as f:
        for (word, count) in difference_words_as_list:
            f.write("{}: {}\n".format(word, count))

    print("ElapsedTime={}s, TotalDifferentWords={}, Message=\"Finished extracting difference words\"".format(format(time.time() - start_time, ".2f"), len(difference_words_as_list)))


if __name__ == "__main__":
    extract_difference_words()
