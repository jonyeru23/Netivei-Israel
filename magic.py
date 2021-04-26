"""
this file is for all the actions that will take place from the question on
"""
from helper import *
import shutil
import concurrent.futures as cf
from string import punctuation
import nltk
from math import log, e, inf
from selenium import webdriver
import fitz
import pytesseract
import cv2
from fuzzywuzzy import fuzz
import textract
import requests
import os
import regex as re


# types for numbers
flip = 'fliphtml5'
pdf = 'pdf'
docx = 'docx'
xsl = 'xsl'
zip = 'zip'
wmv = 'wmv'
jpg = 'jpg'
types = [jpg, flip, pdf, docx, xsl, zip, wmv]
bad_types = [wmv, jpg, zip]


class NLPAnalasys:
    """a class holding functions for all nlp analysis"""
    def __init__(self, similarity_ratio=89):
        self._similarity_ratio = similarity_ratio

    def _check_similarity(self, word1, word2):
        return True if fuzz.ratio(word1, word2) > self._similarity_ratio else False


class TFIDF(NLPAnalasys):
    def __init__(self, pages, the_question, n=1):
        super().__init__()
        self._pages = pages
        self._tokened_dict = {}
        self._idfs = {}
        self._n = n
        self._stop_words = self._get_stop_words_hebrew('hebrew.txt')
        self._the_question = self._tokenizer(the_question)

    def get_tokened_dict(self):
        return self._tokened_dict

    @timer
    def get_top_options(self):
        self._tokenize_dict()
        self._compute_idfs()
        return self._get_top_keys()

    @staticmethod
    def _get_stop_words_hebrew(filename):
        """takes the words in the .txt and makes it a list"""
        with open(filename, encoding="utf8") as f:
            text = f.read()
            stopwords = set(text.split('\n'))
        return stopwords

    def _tokenize_dict(self):
        for name, text in self._pages.items():
            self._tokened_dict[name] = self._tokenizer(text)

    def _tokenizer(self, text):
        words = nltk.word_tokenize(text)
        bag_of_words = list()
        for word in words:
            if word not in punctuation and word not in self._stop_words and word != " ":
                bag_of_words.append(word)
        return bag_of_words

    def _compute_idfs(self):
        """
        Given a dictionary of `documents` that maps names of documents to a list
        of words, return a dictionary that maps words to their IDF values.
        Any word that appears in at least one of the documents should be in the
        resulting dictionary.
        how to do:
        loop over each doc, when i see a new word i add it to the dict and i++ to it's value,
        i will keep track of words i saw in each doc to make sure i dont dubble increment
        after i loopes over all the docs, i will make all the words and give them the log value
        """
        """compute the idf value for the words in the question alone"""
        self._idfs = dict.fromkeys(set(self._the_question), 0)
        for name, text in self._tokened_dict.items():
            for q_word in set(self._the_question):
                if self._is_in_data(text, q_word):
                    self._idfs[q_word] += 1
        self._make_idfs_log()

    def _is_in_data(self, data, word):
        for data_word in data:
            if self._check_similarity(word, data_word):
                return True
        return False

    def _make_idfs_log(self):
        for word, value in self._idfs.items():
            if value == 0:
                continue
            self._idfs[word] = log((len(self._tokened_dict) / value), e)

    def _add_word_to_idfs(self, word):
        for key in self._idfs:
            if self._check_similarity(word, key):
                self._idfs[key] += 1
                return
        self._idfs[word] = 1

    def _get_top_keys(self):
        ranking = dict.fromkeys(self._tokened_dict.keys(), 0)
        for word in self._the_question:
            if self._not_important(word):
                continue

            for key, text in self._tokened_dict.items():
                ranking[key] = self._get_idf_value(word, text)

        return self._get_list_of_best_keys(ranking)

    def _get_idf_value(self, word, text):
        """dealing with hebrew polymorphisism and mistakes of the program"""
        word_counter = 0
        for word_of_text in text:
            if self._check_similarity(word, word_of_text):
                word_counter += 1
        return word_counter * self._idfs[word]

    def _get_list_of_best_keys(self, ranking):
        the_keys = []
        for i in range(self._n):
            best_key = self._get_highest_key_by_value(ranking)
            if self._key_not_good_enough(best_key):
                return the_keys
            the_keys.append(best_key)
            try:
                ranking.pop(best_key)
            except KeyError:
                pass

        return the_keys

    @staticmethod
    def _key_not_good_enough(best_key):
        return True if best_key == 0 else False

    def _not_important(self, word):
        if word in self._stop_words or word not in self._idfs:
            return True
        return False

    @staticmethod
    def _get_highest_key_by_value(ranking):
        highest_value = -inf
        best_key = None
        for key, grade in ranking.items():
            if grade > highest_value:
                best_key = key
                highest_value = grade
        return best_key


class AnswerTensity(NLPAnalasys):
    def __init__(self, tokened_dict, best_keys, the_question):
        super().__init__()
        self._tokened_dict = tokened_dict
        self._best_keys = best_keys
        self._the_question = the_question

    def get_the_best_page(self):
        dict_q_positioning = self._get_positions()


    def _get_positions(self):
        dict_q_positioning = {}
        for key in self._best_keys:
            q_word_positioning = {}
            for q_word in self._the_question:
                postions = list()
                for position, word in enumerate(self._tokened_dict[key]):
                    if self._check_similarity(q_word, word):
                        postions.append(postions)
                q_word_positioning[q_word] = postions
            dict_q_positioning[key] = q_word_positioning
        return dict_q_positioning


class TexT:
    def __init__(self, name, url):
        self._file = File(name, url)
        self._text = {}
        if self._file.write_file():
            self._document = self.open_file()
            self._extract_text()
            self._document.close()
            self._file.delete_file()

    def get_download_url(self):
        return self._file.get_download_url()

    def get_name(self):
        return self._file.get_name()

    def get_text(self):
        return self._text

    @timer
    def open_file(self):
        return fitz.open(self._file.get_name(), filetype="pdf")

    @timer
    def _extract_text(self):
        self._extract_text_by_pages()

    def _extract_text_by_pages(self):
        pages = self._page_maker()
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self._getting_the_txts, pages.items())
            executor.shutdown(wait=True)

    def _getting_the_txts(self, page_numbers):
        page_num = page_numbers[0]
        page = page_numbers[1]
        length_of_page = len(page.get_text())
        if self._is_scanned_image(length_of_page):
            new_text = self._extract_text_from_image(self._document, page_num)
        else:
            file_path = f"{page_num}.pdf"
            pdf = fitz.open()
            pdf.insert_pdf(self._document, from_page=page_num, to_page=page_num)
            pdf.save(file_path)
            new_text = textract.process(file_path)
            new_text = new_text.decode("utf-8")
            os.remove(file_path)
        self._text[page_num] = new_text

    def _extract_text_from_image(self, document, page_num):
        pytesseract.pytesseract.tesseract_cmd = r"tesseract"
        return pytesseract.image_to_string(self._get_image(document, page_num), config='', lang='heb')

    def _page_maker(self):
        pages = {}
        for page_num in range(self._document.page_count):
            pages[page_num] = self._document.load_page(page_num)
        return pages

    @staticmethod
    def _get_image(document, page_num):
        image_list = document.get_page_images(page_num)
        xref = image_list[0][0]
        pix = fitz.Pixmap(document, xref)

        image_path = f"{page_num}.png"
        pix.writePNG(image_path)
        img = cv2.imread(image_path)

        height, width, _ = img.shape
        if width > height:
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

        os.remove(image_path)
        return img

    @staticmethod
    def _reverse_string(page_text):
        new_text = str()
        split_text = page_text.split("\n")
        for line in split_text:
            new_line = str()
            for j in range(len(line)):
                new_line += page_text[len(line) - j - 1]
            new_text += new_line
        return new_text

    @staticmethod
    def _is_scanned_image(length_of_page):
        return True if length_of_page == 0 else False


class File:
    """a file you can write and delete"""
    def __init__(self, name, url):
        self._url = Url(url)
        self._download_url = self._url.get_download_link()
        self._name = f"{name}'.'{self._url.type}"
        self._path = self._get_path_to_file()

    def get_download_url(self):
        return self._download_url

    def get_path(self):
        return self._path

    def get_name(self):
        return self._name

    @timer
    def write_file(self):
        if self._is_url_not_valid():
            return False
        req = requests.get(self._download_url, stream=True)
        self._open_write(req)
        return True

    def delete_file(self):
        os.remove(self._name)

    def _get_path_to_file(self):
        return os.path.join(self._get_current_path(), self._name + '.' + self._url.type)

    @staticmethod
    def _get_current_path():
        return os.path.dirname(os.path.realpath(__file__))

    def _open_write(self, req):
        with open(self._make_name_valid(), "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)

    def _is_url_not_valid(self):
        return True if self._download_url is None else False

    def _make_name_valid(self):
        return re.sub('\r', '', self._name)


class Url:
    """a class for URL"""
    def __init__(self, url):
        self.url = url
        self.type = self._get_type()

    def get_download_link(self):
        if self.type == any(bad_types):
            return
        elif self.type is flip:
            self.type = pdf
            return self._get_pdf_url()
        else:
            return self.url

    def _get_pdf_url(self):
        driver = self._get_driver()
        driver.get(self.url)
        return driver.execute_script('return bookConfig.DownloadURL')

    @staticmethod
    def _get_driver(chrome_path='chromedriver.exe'):
        """opening the chrome driver once"""
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(chrome_path,
                                  options=option)
        return driver

    def _get_type(self):
        for file_type in types:
            if file_type in self.url:
                return file_type


class Dir:
    def __init__(self):
        self.path = None
        self.name = "files"

    def make_dir(self):
        """
        check if dir exist and make a new one
        """
        self._is_path_exist()
        self._mkdir(self._get_cur_path())

    def destroy_dir(self):
        try:
            shutil.rmtree(self.path)
        except OSError as e:
            print("Error: %s : %s" % (self.path, e.strerror))

    def _is_path_exist(self):
        if self.path is not None:
            self.destroy_dir()

    def _mkdir(self, dir_path):
        self.path = os.path.join(dir_path, self.name)
        os.mkdir(self.path)

    @staticmethod
    def _get_cur_path():
        return os.path.dirname(os.path.realpath(__file__))
