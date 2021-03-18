from page import *
from helper import *
import requests
import codecs
import re


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
    # # access the right link
    #
    # # parse the htmkl using bs
    # # get to this link
    # file_url = "http://online.fliphtml5.com/kfky/pzdc/files/search/book_config.js?bfe6ba3d2a8d19569d672697cccad432"
    # r = requests.get(file_url)
    # # print(r.encoding)
    # soup = bs(r.text, features="lxml")
    # text = soup.text.encode("latin1").decode("utf-8")
    # text = re.sub("\s\s+", " ", text)
    #
    # print(text)

if __name__ == '__main__':
    main()

