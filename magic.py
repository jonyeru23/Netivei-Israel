"""
this file is for all the actions that will take place from the question on
"""
import requests
from bs4 import BeautifulSoup as bs
from helper import *

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
        self.micro_subject_links = subject_links
        # a dict for text_name[name] = text
        self.texts = {}
        # path to new_dir and making a new dir
        self.path = make_dir()
        self.load_files()

    def load_files(self):
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self.all_the_work, self.micro_subject_links.items())

    def all_the_work(self, item):
        # print(item[1])
        """responsible for, checking the type, uploading it to the dict"""
        file_type = self.check_for_type(item[1])
        if file_type == any(bad_types):
            return
        else:
            self.load_the_file(file_type, item)

    def check_for_type(self, link):
        """this function will check for a certain link type of file"""
        for file_type in types:
            if file_type in link:
                return file_type

    def load_the_file(self, file_type, item):
        if file_type == flip:
            """we dont need to download the file to the dir if it's a flip"""
            r = requests.get(item[1])
            soup = bs(r.text, features="lxml")
            links = soup.findAll('script')
            page = requests.get(item[1] + links[5].get('src', None))

            text = page.text.encode("latin1").decode("utf-8")
            text = re.sub("\s\s+", " ", text)

            self.texts[item[0]] = text

        elif file_type == pdf:
            """download the file and then get the text"""
            full_path = self.write_file(item)



    def write_file(self, item):
        """writing the file and returning a path to the file"""
        req = requests.get(item[1])
        full_path = os.path.join(self.path, item[0])
        with open(full_path, "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)
        return full_path

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

