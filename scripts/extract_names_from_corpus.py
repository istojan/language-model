import re
import time
from helpers.text_tokenizer import extract_all_sentences_from_files, convert_sentences_to_list_of_words
from operator import itemgetter

INPUT_DIR = "../big_corpus"


def extract_and_save_names():

    start_time = time.time()
    print("Message=\"Starting script to extract capital letter words from corpus\"")

    sentences = extract_all_sentences_from_files(INPUT_DIR)

    sentences_as_list_words = convert_sentences_to_list_of_words(sentences)

    # regex to remove the first word of the sentence
    remove_first_word_regex = r'^\W*\w+\W*'

    # regex to identify capital letter words
    capital_letter_words_regex = r'(?<!\.\s)\b[А-Ш][а-ш]*\b'

    extracted_capital_words = dict()

    # sentences = sentences[:100]
    for sentence in sentences:
        updated_sentence = re.sub(remove_first_word_regex, "", sentence)

        names = re.findall(capital_letter_words_regex, updated_sentence)

        for name in names:
            ctr = extracted_capital_words.get(name, 0)
            ctr = ctr + 1
            extracted_capital_words[name] = ctr

        # print("I: {}        - II: {}                - Names: {}".format(sentence, updated_sentence, names))

    extracted_capital_words_list = [[word, count] for (word, count) in extracted_capital_words.items()]
    extracted_capital_words_list_sorted = sorted(extracted_capital_words_list, key=itemgetter(1), reverse=True)


    with open("capital_letter_words_big_corpus.txt", "w") as f:
        for (word, count) in extracted_capital_words_list_sorted:
            f.write("{}: {}\n".format(word, count))
            # print()

    print("ElapsedTime={}s, TotalCapitalWords={}, Message=\"Finished extracting capital words from corpus\"".format(format(time.time() - start_time, ".2f"), len(extracted_capital_words_list)))


if __name__ == "__main__":
    extract_and_save_names()
