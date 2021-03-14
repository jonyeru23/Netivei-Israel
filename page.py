from tkinter import *
from helper import *

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
    """
    the class for the buttons of the program
    """
    def __init__(self, menu, sub_links, url):
        self.sub_links = sub_links
        self.url = url
        self.menu = menu
        self.button = Button(self.menu.root, text="!בחרתי", command=self.get)

    def get(self):
        """
        if it is the first option menu create the second one
        if it's the second, ask the question and make the magic happen
        """

        if self.menu.first:
            if len(display_menus) > 1:
                for i in range(1, len(display_menus)):
                    display_menus[i].remove()
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
            question = TheQuestion(self.menu.root)
            question.show()
            display_menus.append(question)


class TheQuestion():
    def __init__(self, root):
        self.input = Entry(root)
        self.dif_button = Button(root, text="?מה השאלה", command=self.go)

    def show(self):
        self.input.pack()
        self.dif_button.pack()

    def remove(self):
        self.input.pack_forget()
        self.dif_button.pack_forget()

    def go(self):
        print("fuck")
