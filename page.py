from tkinter import *
from urllib import request
import helper

class FrontPage():
    """
    this class is for building the GUI
    """
    def __init__(self):
        self.root = Tk()
        self.subject = Label(self.root, text=":מה הנושא המרכזי").pack()
        self.subs = None
    # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("400x400")
        self.root.mainloop()
    # get a text bar with options
    def show_subs(self):
        raise NotImplementedError

class ReadSubjects():
    """
    this class is for reading the prime subjects
    """
    def __init__(self):
        self.options = []
        self.url = "https://www.iroads.co.il/"

    def read_url(self):
        main_page = helper.get_html_page(self.url)


