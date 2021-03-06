from tkinter import *
from urllib import request
import helper
from bs4 import BeautifulSoup as bs

# THE MAIN URL
url_main = "https://www.iroads.co.il/"


class FrontPage():
    """
    this class is for building the basic basic front
    """
    def __init__(self):
        self.root = Tk()
        self.subject = Label(self.root, text=":מה הנושא המרכזי").pack()
        self.subs_clicked = StringVar()
    # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("400x400")

    # get a text bar with options

class ReadSubjects():
    """
    this class is for reading the prime subjects
    """
    def __init__(self, the_filter, url):
        self.the_filter = the_filter
        self.url = url
        self.options = self.add_subs()


    def add_subs(self):
        """
        go to the
        """
        options = []
        html = request.urlopen(self.url).read()
        soup = bs(html, features="lxml")

        # filter
        tags = soup('a')
        for tag in tags:
            link = tag.get('href', None)
            if link is None:
                continue
            if self.the_filter in link:
                options.append(tag.figcaption.string)
        return options

class Display_Subjects():
