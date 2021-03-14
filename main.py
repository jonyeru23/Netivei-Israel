from page import *
from helper import *
import requests
import PyPDF2
import textract


# THE MAIN URL
url_main = "https://www.iroads.co.il/"
filter = 'מידע-לספקים'



def main():
    # # building my front page -- class
    # page = FrontPage()
    #
    # # making a dict of options-links -- function
    # main_subs_links = read_subjects(url_main, filter)
    #
    # # making the dropdown, label and a button -- class
    # main_menu = DisplayMenu(page.root, ":מה הנושא המרכזי", main_subs_links.keys(), True,
    #                         main_subs_links, url_main)
    # display_menus.append(main_menu)
    # main_menu.pack()
    #
    # page.root.mainloop()

    """ checking things"""
    # file_url = "https://www.iroads.co.il/media/9771/%D7%A8%D7%99%D7%9B%D7%95%D7%96-%D7%93%D7%A4%D7%99-%D7%A2%D7%93%D7%9B%D7%95%D7%9F-%D7%9E%D7%A1-1-%D7%9C%D7%A4%D7%A8%D7%A7-0002.pdf"
    #
    # r = requests.get(file_url, stream=True)
    #
    # with open("python.pdf", "wb") as pdf:
    #     for chunk in r.iter_content(chunk_size=1024):
    #
    #         # writing one chunk at a time to pdf file
    #         if chunk:
    #             pdf.write(chunk)

    text = textract.process("C:\Users\User\Desktop\progrmaing\personal projects\finding nemo\python.pdf")
    print(text)


if __name__ == '__main__':
    main()

