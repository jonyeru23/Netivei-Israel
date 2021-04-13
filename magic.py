"""
this file is for all the actions that will take place from the question on
"""
from helper import *
# import textract
import shutil
import concurrent.futures as cf
from string import punctuation
# import nltk
from math import log, e, inf
import numpy as np



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

class LoadText:
    """a class to load all the text to a dict"""
    """
    check for the files type
    load it to the dir
    get the text
    load to the dict
    """
    def __init__(self, subject_links):
        # a dict of the links and the headers
        self.__micro_subject_links = subject_links
        # path to new_dir and making a new dir
        self.__path = None
        # a dict for text_name[name] = text
        self.texts = {}

    def get_texts(self):
        """this is the interface!"""
        self.__path = self.__make_dir()
        # loads the files to the dict
        self.__load_files()
        for i, k in self.texts.items():
            print(i)
            print(k)
        # parsers the dict
        self.__destroy_dir()

        return self.texts

    def __make_dir(self):
        """
        make a new dir and return the path to that dir
        """
        if self.__path is not None:
            self.__destroy_dir()
        # get the current dir
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # make a new dir
        dir_name = "files"
        path = os.path.join(dir_path, dir_name)
        os.mkdir(path)

        return path

    def __load_files(self):
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self.__all_the_work, self.__micro_subject_links.items())

    def __all_the_work(self, item):
        """responsible for, checking the type, uploading it to the dict"""
        file_type = self.__check_for_type(item[1])
        if file_type == any(bad_types):
            return
        else:
            self.__load_the_file(file_type, item)

    @staticmethod
    def __check_for_type(link):
        """this function will check for a certain link type of file"""
        for file_type in types:
            if file_type in link:
                return file_type

    def __load_the_file(self, file_type, item):
        if file_type == flip:
            """we dont need to download the file to the dir if it's a flip"""
            r = requests.get(item[1])
            soup = bs(r.text, features="lxml")
            links = soup.findAll('script')
            page = requests.get(item[1] + links[5].get('src', None))

            self.texts[item[0]] = self.__get_text_from_(page)

        else:
            """download the file and then get the text"""
            full_path = self.__write_file(item)
            text = textract.process(full_path)
            text = text.decode("utf-8")

            self.texts[item[0]] = text

    @staticmethod
    def __get_text_from_(page):
        """getting the text and manipiulating it (because it's hebrew)"""
        text = page.text.encode("latin1").decode("utf-8")
        text = re.sub("\s\s+", " ", text)
        text_copy = re.sub('[^\W]', ' ', text)
        chars = re.split(' ', text_copy)
        # loop over all the characters
        for char in chars[:]:
            # find the chars of unicode Cf
            if char == '' or len(char) != 1 or char in punctuation:
                continue
            text = re.sub(char, ' ', text)
        return text

    def __write_file(self, item):
        """writing the file and returning a path to the file"""
        req = requests.get(item[1])
        full_path = os.path.join(self.__path, item[0])
        with open(full_path, "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)
        return full_path

    def __destroy_dir(self):
        try:
            shutil.rmtree(self.__path)
        except OSError as e:
            print("Error: %s : %s" % (self.__path, e.strerror))

class TFIDF():
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

    @timer
    def _compute_idfs(self, tokened_dict):
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



"""
muy importante
"""
# r = requests.get(file_url)
#     # print(r.encoding)
#     soup = bs(r.text, features="lxml")
#     text = soup.text.encode("latin1").decode("utf-8")
#     text = re.sub("\s\s+", " ", text)



#     def load(self):
#         for link in



"""
opening files
"""
