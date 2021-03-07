from page import *
from urllib import request, parse
import requests

url_main = "https://www.iroads.co.il/"


def main():
    # building my front page
    page = FrontPage()

    # getting the subjects from the web
    main_subs_links = ReadSubjects()
    # making the dropdown
    main_menu = Display_Subjects(main_subs_links.keys(), page.root, main_subs_links)


    # # making the dropdown
    # sub_menu = Display_Subjects(sub_subs.options, page.root)

    page.root.mainloop()

    """ checking things"""



if __name__ == '__main__':
    main()

