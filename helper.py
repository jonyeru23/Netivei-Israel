import requests
from tkinter import *
from bs4 import BeautifulSoup as bs
import os

def make_options(root, clicked, options, text):
    """
    building a label a menu
    """
    main_label = Label(root, text=text)
    drop = OptionMenu(root, clicked, *options)
    return main_label, drop


def read_subjects(url, the_filter):
    """
    get me the subjects and return two datasets
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


def get_headers(clicked, hrefs, url_main):
    """
    function will return a dict of headers-links
    """
    # make the dict
    subs_links = {}

    # making out way for the page
    url = requests.get(url_main, hrefs[clicked][1:-1])
    subject_url = requests.get(url.url.replace('?', ''))
    # get the soup
    soup = bs(subject_url.text, features="lxml")

    # get the relevant headers
    bigs = soup.findAll('div', class_='container-fluid col9')

    for big in bigs:
        raw_links = big.ul.findAll('li')
        # i want to create a dict with the subjects and links
        # and then add it to the big dict
        spec_links = {}
        for raw in raw_links:
            try:
                spec_links[raw.div.h2.text.replace('\n', '')] = raw.div.div.a.get('href', None)
            except AttributeError:
                print(raw.div.h2.text)
        subs_links[big.article.h2.text] = spec_links

    # print_(subs_links)

    return subs_links, subject_url

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
