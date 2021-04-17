from page import *
from helper import *
import requests

# THE MAIN URL
url_main = "https://www.iroads.co.il/"
filter = 'מידע-לספקים'


def main():
    # building my front page -- class
    page = FrontPage()

    # making a dict of options-links -- function
    header_finder = GetHeaders(page.root, url_main, filter)
    main_subs_links = header_finder.get_hrefs()

    # making the dropdown, label and a button -- class
    main_menu = DisplayMenu1(page.root, ":מה הנושא המרכזי", main_subs_links.keys(), main_subs_links, url_main)
    main_menu.show()

    page.root.mainloop()

    """ checking things"""


def checking_gens(full_path):
    text = textract.process(full_path)
    yield text.decode("utf-8")


if __name__ == '__main__':
    main()

