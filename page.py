from tkinter import *
from urllib import request
import helper
from bs4 import BeautifulSoup as bs
import requests


# THE MAIN URL
url_main = "https://www.iroads.co.il/"
filter = 'מידע-לספקים'


class FrontPage():
    """
    this class is for building the basic basic front
    """

    def __init__(self):
        self.root = Tk()
        self.subject = Label(self.root, text="מה תרצו לדעת?").pack()
        # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("800x800")


def ReadSubjects():
    """
    get me the subjects and return two datasets:
    1. a list of options
    2. a dict of option - href
    """
    hrefs = {}
    html = requests.get(url_main)
    soup = bs(html.text, features="lxml")

    tags = soup.findAll('a', class_='infoIcon')

    # filter
    for tag in tags:
        link = tag.get('href', None)
        if link is None:
            continue
        if filter in link:
            option = tag.figcaption.string
            # adding to my dict the links
            hrefs[option] = link

    return hrefs

class Display():
    def __init__(self, root):
        self.root = root
        self.clicked = StringVar()


class Display_Subjects(Display):
    """
    this class is for displaying options menus
    """

    def __init__(self, options, root, hrefs):
        super().__init__(root)
        self.options = options
        self.hrefs = hrefs

        # building a options menu
        self.clicked.set('לא נבחר')
        self.make_options()

    def make_options(self):
        """
        building a label a menu and a button
        """
        main_label = Label(self.root, text=":מה הנושא המרכזי")
        main_label.place(relx=0.9, rely=0.1)
        drop = OptionMenu(self.root, self.clicked, *self.options).place(relx=0.5, rely=0.1)
        mybutton = Button(self.root, text='בחרתי!', command=self.change).place(relx=0.4, rely=0.105)


    def change(self):
        """
        this is where i'm going to set the new options
        """
        sub_subs = ReadSubSubjects(self.hrefs, self.clicked.get())
        sub_subs.get_headers()

        sub_menu = DisplaySubSubjects(sub_subs.options, self.root)


class ReadSubSubjects():
    """
    this class is for getting the headers of the page we have chosen to enter
    """
    def __init__(self, hrefs, clicked):
        self.hrefs = hrefs
        self.options = ['תבחר נושא']
        self.clicked = str(clicked)

    def get_headers(self):
        # print(self.clicked)
        if self.clicked not in self.hrefs.keys():
            return
        self.options.clear()
        # making out way for the page
        url = requests.get(url_main, self.hrefs[self.clicked][1:-1])
        subject_url = requests.get(url.url.replace('?', ''))
        # get the soup
        soup = bs(subject_url.text, features="lxml")

        # get the relevant headers
        bigs = soup.findAll('div', class_='container-fluid col9')

        for big in bigs:
            self.options.append(big.article.h2.text)


class DisplaySubSubjects(Display):
    def __init__(self, options, root):
        super().__init__(root)
        self.options = options

        # build the interface
        self.drop = OptionMenu(self.root, self.clicked, *self.options).place(relx=0.5, rely=0.2)
        mybutton = Button(self.root, text='submit', command=self.ask).place(relx=0.4, rely=0.21)

    def ask(self):
        """
        asking the user what he/she would like to know
        """



