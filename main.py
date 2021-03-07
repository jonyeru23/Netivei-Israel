from page import *

url_main = "https://www.iroads.co.il/"


def main():
    # building my front page
    page = FrontPage()
    # build a option menu
    filter = 'מידע-לספקים'
    main_subs = ReadSubjects(filter, url_main)
    main_menu = Display_Subjects(main_subs.options, page.root)
    page.root.mainloop()


if __name__ == '__main__':
    main()

