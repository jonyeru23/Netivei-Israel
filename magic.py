"""
this file is for all the actions that will take place from the question on
"""
from helper import *
import textract
import shutil
import concurrent.futures as cf
from string import punctuation
import nltk
from math import log, e



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
        """getting the text and manipiulating it (because it's hebrew"""
        text = page.text.encode("latin1").decode("utf-8")
        text = re.sub("\s\s+", " ", text)
        text_copy = re.sub('[^\W]', ' ', text)
        chars = re.split(' ', text_copy)
        # loop over all the characters
        for char in chars[:]:
            # find the chars of unicode Cf
            if char == '' or len(char) != 1 or char in punctuation:
                continue
            text = re.sub(char, '', text)
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
    """The father class"""

    def __init__(self, texts, the_questions):
        """the data for both classes"""
        self._idf = {}
        self._stop_words = self._get_stop_words_hebrew('hebrew.txt')
        self.documents = texts
        self.the_questions = the_questions

    def _tokenize(self, document):
        """make every string given a list of space or punctuation marks separated tokens"""
        stopwords = self._get_stop_words_hebrew('hebrew.txt')
        words = nltk.word_tokenize(document)
        return [word for word in words if word not in punctuation and
                word not in stopwords]

    @staticmethod
    def _get_stop_words_hebrew(filename):
        """takes the words in the .txt and makes it a list"""
        with open(filename, encoding="utf8") as f:
            text = f.read()
            stopwords = list(text.split('\n'))
        return stopwords

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
        # get the number of the docs
        num_docs = len(self.documents)

        # loop over each doc
        for doc in self.documents:
            seen = set()
            # loop over each word
            for word in self.documents[doc]:
                # if the word was seen in the doc continue
                if word in seen:
                    continue
                # else, check if it exists in dict, if so i++ if not i = 0
                else:
                    if word in self._idf:
                        self._idf[word] += 1
                    else:
                        self._idf[word] = 1
                    seen.add(word)

        # make it logarithmic
        for word in self._idf:
            self._idf[word] = log((num_docs / self._idf[word]), e)

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

