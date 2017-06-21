import re
import nltk
from bs4 import BeautifulSoup
from functools import reduce


def remove_images(text):
    text = BeautifulSoup(text, 'html.parser')
    [s.extract() for s in text.find_all('img')]
    return str(text)


def remove_code(text):
    text = BeautifulSoup(text, 'html.parser')
    [s.extract() for s in text.find_all('code')]
    return str(text)


def remove_duplicate_link(text):
    text = BeautifulSoup(text, 'html.parser')
    duplicate_links = text.find_all('blockquote')
    for dl in duplicate_links:
        if re.search("Possible\sDuplicate", dl.text):
            dl.extract()
    return str(text)


def remove_urls(text):
    text = BeautifulSoup(text, 'html.parser')
    [s.unwrap() for s in text.find_all('a')]
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', str(text))
    return str(text)


def remove_tags(text):
    text = BeautifulSoup(text, 'html.parser')
    text = text.get_text(" ")
    return str(text)


def nltk_tokenize(text):
    tokens = nltk.word_tokenize(text)
    return " ".join(tokens)


def words_only(text):
    tokens = text.split(" ")
    words = [t for t in tokens if re.match("\w", t)]
    return " ".join(words)


def lowercase(text):
    return text.lower()


def preprocess_text(text, operations=[remove_images,
                                      remove_code,
                                      remove_duplicate_link,
                                      remove_urls,
                                      remove_tags,
                                      nltk_tokenize,
                                      words_only,
                                      lowercase]):  # Mind the order!
    if operations:
        return reduce((lambda x, y: y(x)), operations, text)
    else:
        return text

