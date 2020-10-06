from bs4 import BeautifulSoup
import requests
import os

BOOKS_DIRECTORY = "books2"

BOOKS_FILE = "books.txt"

ALPHABET = "абвгдѓежзѕијклљмнњопрстќуфхцчџш"


def extract_book_names():

    books = dict()

    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            for line in f:
                tmp = line.strip().split("|")
                books[tmp[0]] = tmp[1]

        print("TotalBooksCount={}, Message=\"Returning already read books.\"".format(len(books)))
        return books

    start_page = "http://makedonika.mk/Knigoteka.aspx?order=&cats=&page="

    page_ctr = 1
    total_books = 0

    while page_ctr < 1000:
        current_page = start_page + str(page_ctr)

        r = requests.get(current_page)
        soup = BeautifulSoup(r.text, features="html.parser")

        title_p_tags = soup.findAll("p", {"class": "naslov_kn"})

        if title_p_tags is None or len(title_p_tags) == 0:
            print("PagesVisited={}, BooksTotal={}, Message=\"Finished extracting books\"".format(page_ctr-1, total_books))
            break

        ids_a_tags = soup.findAll("a", {"class": "kniga_pop"})

        for i in range(0, len(title_p_tags)):
            total_books += 1
            book_name = title_p_tags[i].text
            book_id = ids_a_tags[i]['href'].split("idBook=")[1]

            if book_name is not None and book_name != "":
                print("BookName={}, Id={}".format(book_name, book_id))
                books[book_name] = book_id

        page_ctr = page_ctr + 1

    with open(BOOKS_FILE, 'w') as f:
        for book_name, book_id in books.items():
            f.write(book_name + "|" + book_id + "\n")

    return books


def extract_books(books):

    if not os.path.exists(BOOKS_DIRECTORY):
        os.makedirs(BOOKS_DIRECTORY)

    for book_name, book_id in books.items():
        file_path = "{}/{}.txt".format(BOOKS_DIRECTORY, book_name)

        if "/" in book_name:
            print("BookName={}, BookId={}, Message=\"Skipping book...\"".format(book_name, book_id))
            continue

        if os.path.exists(file_path):
            continue

        with open(file_path, 'w') as f:
            section_number = 1
            consecutive_error_pages = 0

            while section_number < 10000:
                link = "http://www.makedonika.mk/Upload/EpubExtract/{}{}/OEBPS/Text/Section{:04d}.xhtml".format(book_name, book_id, section_number)

                r = requests.get(link)
                soup = BeautifulSoup(r.text, features="html.parser")
                if "404 - File or directory not found." in soup.text or "HTTP Error 400. The request URL is invalid." in soup.text:
                    consecutive_error_pages += 1
                    if consecutive_error_pages == 5:
                        print(link)
                        print("BookName={}, Message=\"Finished iterating over book.\"".format(book_name))
                        break
                else:
                    consecutive_error_pages = 0
                    f.write(soup.text)

                section_number = section_number + 1

            if section_number >= 10000:
                print("BookName={}, Message=\"WARNING: Reached 10k visits for book\"".format(book_name))


def extract_words_for_letter(letter):

    print("Character: {}, Starting to extract words for character.".format(letter))

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = {'User-Agent': user_agent}

    base_url = "http://www.makedonski.info"
    url = "{}/letter/{}".format(base_url, letter)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")

    sub_pages = list()

    for option in soup.find_all('option'):
        sub_pages.append(option['value'])

    words_urls = list()

    print("Character: {}, SubPages={}".format(letter, len(sub_pages)))

    for page in sub_pages:
        url = "{}{}".format(base_url, page)

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, features="html.parser")

        # print(r.text)
        # print(url)
        # print(soup.find(id="lexems").find_all('a'))

        for word_link in soup.find(id="lexems").find_all('a'):
            word_url = "{}{}".format(base_url, word_link["href"])

            words_urls.append(word_url)

    print("Character: {}, Words={}".format(letter, len(words_urls)))

    return words_urls

    # print(r)
    # print(url)
    # # print(soup)
    # print(r.text)
    #
    # # print(soup.findAll(id='ranges'))
    # # print(soup.select("select > option"))
    # print(soup.find_all('option'))
    # print(letter)
    # print(sub_pages)


if __name__ == '__main__':
    # books = extract_book_names()
    #
    # extract_books(books)

    word_urls = list()

    for c in ALPHABET:
        word_urls_for_character = extract_words_for_letter(c)
        word_urls.extend(word_urls_for_character)

    print("Total Word Urls={}".format(len(word_urls)))

    with open("urls_of_words.txt", 'w') as f:
        for url in word_urls:
            f.write(url + "\n")



# абонент
# < div
#
#
# class ="flexion" >
#
# < i > мн.абоненти < / i >
#
# < / div >