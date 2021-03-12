from page import *
from helper import *
from urllib import request, parse
import requests


# THE MAIN URL
url_main = "https://www.iroads.co.il/"
filter = 'מידע-לספקים'



def main():
    # building my front page -- class
    page = FrontPage()

    # making a dict of options-links -- function
    main_subs_links = read_subjects(url_main, filter)

    # making the dropdown, label and a button -- class
    main_menu = DisplayMenu(page.root, ":מה הנושא המרכזי", main_subs_links.keys(), True,
                            main_subs_links, url_main)
    display_menus.append(main_menu)
    main_menu.pack()

    page.root.mainloop()

    """ checking things"""


if __name__ == '__main__':
    main()

