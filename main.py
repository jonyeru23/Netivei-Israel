from page import *
from helper import *

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
    # listing()
    # req = requests.get('http://online.fliphtml5.com/kfky/pzdc/#p=1')
    # full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test")
    # with open(full_path, "wb") as f:
    #     for chunk in req.iter_content(chunk_size=8192):
    #         f.write(chunk.e)


# @timer
# def listing():
#     with open('hebrew.txt', encoding="utf8") as f:
#         text = f.read()
#         stopwords = list(text.split('\n'))
#     print(stopwords)

# b = "הפקעות‪/‬מלווים סטאטוטוריים‪/‬מתכנן גיאומטריה‪/‬מתכנן‬ ‫מוביל‪/‬מנה\"פ"
#
# c = לפרויקט \"אופני‪-‬דן\" (סימוכין ‬‫‪ )1‬ ולפי  פרק


if __name__ == '__main__':
    main()

