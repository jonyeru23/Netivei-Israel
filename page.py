from tkinter import *
from helper import *
from urllib import request
import helper
from bs4 import BeautifulSoup as bs
import requests

"""
this is a global list of all the display menus
"""
display_menus = []

class FrontPage():
    """
    this class is for building the basic basic front
    """

    def __init__(self):
        self.root = Tk()
        self.subject = Label(self.root, text="?מה תרצו לדעת").pack()
        # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("800x800")


class DisplayMenu():
    """
    this class is for creating the label and the option menu. that's it!
    """
    def __init__(self, root, text, options, first, sub_links, url):
        self.root = root
        self.clicked = StringVar()
        self.clicked.set("לא נחבר")
        self.first = first

        self.label = Label(self.root, text=text)
        self.drop = OptionMenu(self.root, self.clicked, *options)
        self.button = MyButton(self, sub_links, url)

    def pack(self):
        self.label.pack()
        self.drop.pack()
        self.button.button.pack()

    def remove(self):
        self.label.pack_forget()
        self.drop.pack_forget()
        self.button.button.pack_forget()


class MyButton():
    def __init__(self, menu, sub_links, url):
        self.sub_links = sub_links
        self.url = url
        self.menu = menu
        self.button = Button(self.menu.root, text="!בחרתי", command=self.get)

    def get(self):

        if self.menu.first:
            if len(display_menus) > 1:
                display_menus[-1].remove()
            # find the subs -- function
            sub_subs_links, subject_url = get_headers(str(self.menu.clicked.get()), self.sub_links, self.url)

            # create another display menu
            sub_menu = DisplayMenu(self.menu.root, ":מה הנושא המשני", sub_subs_links.keys(), False,
                                   sub_subs_links, subject_url)
            display_menus.append(sub_menu)
            sub_menu.pack()

        else:
            """
            ask the fucking question
            """
            print("fuck")

# class Display():
#     def __init__(self, root):
#         self.root = root
#         self.clicked = StringVar()
#
#
# class Display_Subjects(Display):
#     """
#     this class is for displaying options menus
#     """
#
#     def __init__(self, options, root, hrefs):
#         super().__init__(root)
#         self.options = options
#         self.hrefs = hrefs
#
#         # building a options menu
#         self.clicked.set('לא נבחר')
#         self.make_options()
#
#     def make_options(self):
#         """
#         building a label a menu and a button
#         """
#         main_label = Label(self.root, text=":מה הנושא המרכזי")
#         main_label.pack()
#         drop = OptionMenu(self.root, self.clicked, *self.options).pack()
#         mybutton = Button(self.root, text='!בחרתי', command=self.change).pack()
#
#
#     def change(self):
#         """
#         this is where i'm going to set the new options
#         """
#         sub_subs = ReadSubSubjects(self.hrefs, self.clicked.get())
#         sub_subs.get_headers()
#
#         sub_menu = DisplaySubSubjects(sub_subs.options, self.root)
#
#
# class ReadSubSubjects():
#     """
#     this class is for getting the headers of the page we have chosen to enter
#     """
#     def __init__(self, hrefs, clicked):
#         self.hrefs = hrefs
#         self.options = ['תבחר נושא']
#         self.clicked = str(clicked)
#
#
#
# class DisplaySubSubjects(Display):
#     def __init__(self, options, root):
#         super().__init__(root)
#         self.options = options
#
#         # build the interface
#         self.drop = OptionMenu(self.root, self.clicked, *self.options).pack()
#         mybutton = Button(self.root, text='submit', command=self.ask).pack()
#
#     def ask(self):
#         """
#         asking the user what he/she would like to know
#         """



