import requests
from tkinter import *
from bs4 import BeautifulSoup as bs
import os
import time
import concurrent.futures as cf


def timer(func):
    """ for personal use"""
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        value = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f'This is the time it took:{round(t2 - t1)} second(s)')
        return value
    return wrapper


def make_options(root, clicked, options, text):
    """
    building a label a menu
    """
    main_label = Label(root, text=text)
    drop = OptionMenu(root, clicked, *options)
    return main_label, drop


def read_subjects(url, the_filter):
    """
    get me the subjects and return
    a dict of option - href
    """
    hrefs = {}
    html = requests.get(url)
    soup = bs(html.text, features="lxml")

    tags = soup.findAll('a', class_='infoIcon')

    # filter
    for tag in tags:
        link = tag.get('href', None)
        if link is None:
            continue
        if the_filter in link:
            option = tag.figcaption.string
            # adding to my dict the links
            hrefs[option] = link

    return hrefs

class GetHeaders:
    def __init__(self, clicked, hrefs, url_main):
        self.clicked = clicked
        self.hrefs = hrefs
        self.url_main = url_main
        self.subs_links = {}
        self.subject_url = self.get_subject_url()

    def get_subject_url(self):
        url = requests.get(self.url_main, self.hrefs[self.clicked][1:-1])
        return requests.get(url.url.replace('?', ''))

    @timer
    def get_headers(self):
        """
        function will return a dict of headers-links
        """
        # get the soup
        soup = bs(self.subject_url.text, features="lxml")

        # get the relevant headers
        bigs = soup.findAll('div', class_='container-fluid col9')

        with cf.ProcessPoolExecutor() as executor:
            executor.map(self.parser_head_link, bigs)

        return self.subs_links

    def parser_head_link(self, big):
        try:
            raw_links = big.ul.findAll('li')
        except AttributeError:
            return
        # i want to create a dict with the subjects and links
        # and then add it to the big dict
        spec_links = {}
        for raw in raw_links:
            try:
                spec_links[raw.div.h2.text.replace('\n', '')] = raw.div.div.a.get('href', None)
            except AttributeError:
                print(raw.div.h2.text)
        self.subs_links[big.article.h2.text] = spec_links

def print_(dict):
    for k in dict:
        print(f"key:{k}")
        for k1 in dict[k]:
            print(f"keys:{k1}, values{dict[k][k1]}")



def get_real_file(url):
    """
    accepts a fliphtml link and returns a pdf link
    """
    req = requests.get(url)

    soup = bs(req.text, features="lxml")






def make_dir():
    """
    make a new dir and return the path to that dir
    """
    # get the current dir
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # make a new dir
    dir_name = "files"
    path = os.path.join(dir_path, dir_name)
    os.mkdir(path)

    return path
