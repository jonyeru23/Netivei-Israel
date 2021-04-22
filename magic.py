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

class TFIDF:
    def __init__(self, pages, the_question, n=1, similarity_ratio=89):
        self._pages = pages
        self._tokened_dict = {}
        self._idfs = {}
        self._n = n
        self._similarity_ratio = similarity_ratio
        self._stop_words = self._get_stop_words_hebrew('hebrew.txt')
        self._the_question = self._tokenizer(the_question)

    def get_top_options(self):
        self._tokenize_dict()
        self._compute_idfs()
        return self._get_top_keys()

    @staticmethod
    def _get_stop_words_hebrew(filename):
        """takes the words in the .txt and makes it a list"""
        with open(filename, encoding="utf8") as f:
            text = f.read()
            stopwords = list(text.split('\n'))
        return stopwords

    def _tokenize_dict(self):
        for name, words in self._pages.items():
            self._tokened_dict[name] = self._tokenizer(words)

    def _tokenizer(self, text):
        words = nltk.word_tokenize(text)
        return [word for word in words if word not in punctuation
                and word not in self._stop_words
                and word != " "]

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
        for name, text in self._tokened_dict.items():
            seen = set()
            for word in text:
                if self._is_in_seen(word, seen):
                    continue
                else:
                    self._add_word_to_idfs(word)
                    seen.add(word)

        self._make_idfs_log()

    def _is_in_seen(self, seen, word):
        for seen_word in seen:
            if self._check_similarity(word, seen_word):
                return True
        return False

    def _make_idfs_log(self):
        for word in self._idfs:
            self._idfs[word] = log((len(self._tokened_dict) / self._idfs[word]), e)

    def _add_word_to_idfs(self, word):
        for key in self._idfs:
            if self._check_similarity(word, key):
                self._idfs[key] += 1
                return
        self._idfs[word] = 1

    def _get_top_keys(self):
        ranking = self.set_rankings()
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

    def _check_similarity(self, word1, word2):
        return True if fuzz.ratio(word1, word2) > self._similarity_ratio else False

    def _get_list_of_best_keys(self, ranking):
        the_keys = []
        for i in range(self._n):
            best_key = self._get_highest_key_by_value(ranking)
            if self._key_not_good_enough(best_key):
                return the_keys
            the_keys.append(best_key)
            ranking.pop(best_key)

        return the_keys

    @staticmethod
    def _key_not_good_enough(best_key):
        return True if best_key == 0 else False

    def _not_important(self, word):
        if word in self._stop_words or word not in self._idfs:
            return True
        return False

    def set_rankings(self):
        ranking = {}
        for key in self._tokened_dict:
            ranking[key] = 0
        return ranking

    @staticmethod
    def _get_highest_key_by_value(ranking):
        highest_value = -inf
        best_key = None
        for key, grade in ranking.items():
            if grade > highest_value:
                best_key = key
                highest_value = grade
        return best_key


class HeadersIDFS(TFIDF):
    """this is for experiments, the exact numbers will be decided"""
    def get_top_options(self):
        self._tokenize_dict()
        self._compute_idfs()
        return self._get_top_keys()

    def _get_list_of_best_keys(self, ranking):
        ranking_copy = ranking.copy()
        for key, value in ranking_copy.items():
            if value == 0:
                ranking.pop(key)
        if len(ranking) == 0:
            return ranking_copy.keys()
        else:
            return ranking.keys()

    def _get_idf_value(self, word, text):
        """dealing with hebrew polymorphisism and egnoring
        the number of times the word appears"""
        for word_of_text in text:
            if word in word_of_text:
                return self._idfs[word]
        return 0


class FilesIDFS(TFIDF):
    def _get_idf_value(self, word, text):
        """dealing with hebrew polymorphisism
        taking into account the number of times the word appears"""
        counter = 0
        for word_of_text in text:
            if word in word_of_text:
                counter += 1
        return counter * self._idfs[word]


class FFTFIDF():
    """Finding nemo!"""

    def __init__(self, texts, the_questions, n=1):
        self._n = n
        self._stop_words = self._get_stop_words_hebrew('hebrew.txt')
        self._documents = texts
        self._tokened_docs = {}
        self._sentences = {}
        self._the_questions = the_questions


    def get_answer(self):
        """all the work"""
        # tokenized the documents
        for name, text in self._documents.items():
            self._tokened_docs[name] = self._tokenizer(text)

        # compute the idfs
        docs_idfs = self._compute_idfs(self._tokened_docs)

        # get the top files
        top_files = self._top_keys(docs_idfs, self._tokened_docs, True)

        # get the top sentences
        for file in top_files:
            self._get_sentences(file)

        for name, text in self._sentences.copy().items():
            self._sentences[name] = self._tokenizer(text)

        sentences_idfs = self._compute_idfs(self._sentences)

        top_sentences = self._top_keys(sentences_idfs, self._sentences, False)

        return top_sentences


    def _get_sentences(self, name):
        """making a doc a dict of sentences"""
        text = self._documents[name]

        split_text = re.split(".", text)

        for sentence in split_text:
            self._sentences[sentence] = re.split(' ', sentence)
    #
    # # Extract sentences from top files
    # sentences = dict()
    # for filename in filenames:
    #     for passage in files[filename].split("\n"):
    #         for sentence in nltk.sent_tokenize(passage):
    #             tokens = tokenize(sentence)
    #             if tokens:
    #                 sentences[sentence] = tokens

    def _tokenizer(self, text):
        """make every string given a list of space or punctuation marks separated tokens"""
        words = nltk.word_tokenize(text)
        return [word for word in words if word not in punctuation
                and word not in self._stop_words
                and word != " "]

    @staticmethod
    def _get_stop_words_hebrew(filename):
        """takes the words in the .txt and makes it a list"""
        with open(filename, encoding="utf8") as f:
            text = f.read()
            stopwords = list(text.split('\n'))
        return stopwords

    @staticmethod
    def _compute_idfs(tokened_dict):
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
        # make thereturned dict
        idf = {}
        # get the number of the docs
        num_docs = len(tokened_dict)

        # loop over each doc
        for name, text in tokened_dict.items():
            seen = set()
            # loop over each word
            for word in text:
                # if the word was seen in the doc continue
                if word in seen:
                    continue
                # else, check if it exists in dict, if so i++ if not i = 0
                else:
                    if word in idf:
                        idf[word] += 1
                    else:
                        idf[word] = 1
                    seen.add(word)

        # make it logarithmic
        for word in idf:
            idf[word] = log((num_docs / idf[word]), e)

        return idf

    def _top_keys(self, idf, tokened_dict, is_file):
        """
        Given a `query` (a set of words), `files` (a dictionary mapping names of
        files to a list of their words), and `idfs` (a dictionary mapping words
        to their IDF values), return a list of the filenames of the the `n` top
        files that match the query, ranked according to tf-idf.
        the how:
        make a dict with ranking for each doc (doc as key and grade as value)
        iterate over all the words in the query,
        if a word is stopword, continue
        else, calculate her tf-idf and add it to the value of the dict
        the dict with the hiesght value wins
        """
        # make the dict
        ranking = {}
        for file in tokened_dict:
            ranking[file] = 0

        # iterate over the query
        for word in self._the_questions:
            if word in self._stop_words or word not in idf:
                continue

            # term frequency and idf
            for key, text in tokened_dict.items():
                if is_file:
                    ranking[key] += text.count(word) * idf[word]
                else:
                    # in other words, if the word is in a sentence rank it higher
                    if word in text:
                        ranking[key] += idf[word]

        the_keys = []
        for i in range(self._n):
            best_key = self._get_highest_key_by_value(ranking)
            the_keys.append(best_key)
            ranking.pop(best_key)

        return the_keys

    @staticmethod
    def _get_highest_key_by_value(ranking):
        highest_value = -inf
        best_key = None
        for key, grade in ranking.items():
            if grade > highest_value:
                best_key = key
                highest_value = grade
        return best_key


class TextDict:
    def __init__(self, subject_links):
        self._micro_subject_links = subject_links
        self._files = Dir()
        self._texts = {}

    def get_texts(self):
        self._make_texts()
        print(len(self._texts))
        return self._texts

    def _make_texts(self):
        """this is the interface!"""
        self._files.make_dir()
        # loads the files to the dict
        self._load_files()
        # parsers the dict
        self._files.destroy_dir()

    def _load_files(self):
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self._all_the_work, self._micro_subject_links.items())

    def _all_the_work(self, item):
        """responsible for, checking the type, uploading it to the dict"""
        text_object = Text(item[0], item[1])
        if self._is_text_valid(text_object.get_text()):
            self._texts[text_object.get_name()] = text_object.get_text()

    @staticmethod
    def _is_text_valid(text):
        return True if text is not None else False


class Text:
    def __init__(self, name, url):
        self._file = File(name, url)
        self._text = self._extract_text()

    def get_name(self):
        return self._file.get_name()

    def get_text(self):
        return self._text

    def _extract_text(self):
        if self._file.write_file():
            text = self._extract_text_by_pages()
            self._file.delete_file()
            return text
        return None

    def _extract_text_by_pages(self):
        text = {}
        image_path = "page.png"
        document = fitz.open(self._file.get_name())
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            page_text = page.get_text()
            length_of_page = len(page_text)
            if self._is_scanned_image(length_of_page):
                new_text = self._extract_text_from_image(document, page_num, image_path)
            else:
                new_text = self._reverse_string(length_of_page, page_text)
            text[page_num] = new_text
        return text

    def _extract_text_from_image(self, document, i, image_path):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
        return pytesseract.image_to_string(self._get_image(document, i, image_path), config='', lang='heb')

    @staticmethod
    def _get_image(document, i, image_path):
        image_list = document.get_page_images(i)
        xref = image_list[0][0]
        pix = fitz.Pixmap(document, xref)
        pix.writePNG(image_path)
        img = cv2.imread(image_path)
        height, width, _ = img.shape
        if width > height:
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
        os.remove(image_path)
        return img

    @staticmethod
    def _reverse_string(length_of_page, page_text):
        new_text = str()
        for j in range(length_of_page):
            new_text += page_text[length_of_page - j - 1]
        return new_text

    @staticmethod
    def _is_scanned_image(length_of_page):
        return True if length_of_page == 0 else False


class File:
    """a file you can write and delete"""
    def __init__(self, name, url):
        self._url = Url(url)
        self._download_url = self._url.get_download_link()
        self._name = name + "." + self._url.type
        self._path = self._get_path_to_file()

    def get_path(self):
        return self._path

    def get_name(self):
        return self._name

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
        with open(rf"{self._name}", "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)

    def _is_url_not_valid(self):
        return True if self._download_url is None else False



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


# class Text:
#     def __init__(self, name, url):
#         self._file = File(name, url)
#         self._text = {}
#         if self._file.write_file():
#             self._document = fitz.open(self._file.get_name())
#             self._extract_text()
#
#     def get_name(self):
#         return self._file.get_name()
#
#     def get_text(self):
#         return self._text
#
#     def _extract_text(self):
#         self._extract_text_by_pages()
#         self._file.delete_file()
#
#     def _extract_text_by_pages(self):
#         with cf.ThreadPoolExecutor() as executor:
#             executor.map(self._extract_from_page, range(self._document.page_count))
#
#     def _extract_from_page(self, page_num):
#         image_path = "page.png"
#         page_doc = self._document.load_page(page_num)
#         page_text = page_doc.get_text()
#         length_of_page = len(page_text)
#         if self._is_scanned_image(length_of_page):
#             new_text = self._extract_text_from_image(page_num, image_path)
#         else:
#             new_text = self._reverse_string(length_of_page, page_text)
#         self._text[page_num] = new_text
#
#     def _extract_text_from_image(self, i, image_path):
#         pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
#         return pytesseract.image_to_string(self._get_image(i, image_path), config='', lang='heb')
#
#     def _get_image(self, i, image_path):
#         image_list = self._document.get_page_images(i)
#         xref = image_list[0][0]
#         pix = fitz.Pixmap(self._document, xref)
#         pix.writePNG(image_path)
#         img = cv2.imread(image_path)
#         height, width, _ = img.shape
#         if width > height:
#             img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
#         os.remove(image_path)
#         return img
#
#     @staticmethod
#     def _reverse_string(length_of_page, page_text):
#         new_text = str()
#         for j in range(length_of_page):
#             new_text += page_text[length_of_page - j - 1]
#         return new_text
#
#     @staticmethod
#     def _is_scanned_image(length_of_page):
#         return True if length_of_page == 0 else False
