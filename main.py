from page import *
from helper import *

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
    main_menu = DisplayMenu1(page.root, ":מה הנושא המרכזי", main_subs_links, url_main)
    main_menu.show()

    page.root.mainloop()

    """ checking things"""
    # i = 5
    # url = "http://online.fliphtml5.com/kfky/pzdc/" + f"#p={i}"
    # req = requests.get(url)
    # print(req.url)
#     # make_set_of_word
#     checker()
#
# @timer
# def checker():
#     word = "עצירה"
#     word1 = "עקיפה"
#     ratio = fuzz.ratio(word, word1)
#     print(ratio)


if __name__ == '__main__':
    main()

