import requests
from tkinter import *
from bs4 import BeautifulSoup as bs
import os
import time



def timer(func):
    """ for personal use"""
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        value = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f'This is the time it took:{t2 - t1} second(s)')
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


def print_(dict):
    for k in dict:
        print(f"key:{k}")
        for k1 in dict[k]:
            print(f"keys:{k1}, values{dict[k][k1]}")


