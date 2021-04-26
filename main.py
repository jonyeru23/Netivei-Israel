from page import *
from helper import *


def main():
    # building my front page -- class
    page = FrontPage()

    # making a dict of options-links -- function
    header_finder = GetHeaders(page.root, url_main, filter)
    main_subs_links = header_finder.get_hrefs()

    # making the dropdown, label and a button -- class
    main_menu = DisplayMenu1(page.root, ":מה הנושא המרכזי", main_subs_links, url_main)
    main_menu.show()

    page.root.mainloop()

    """ checking things"""

if __name__ == '__main__':
    main()

