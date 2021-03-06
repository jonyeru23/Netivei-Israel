from urllib import request
from bs4 import BeautifulSoup as bs

def main():
    # building my front page
    # page = FrontPage()
    html = request.urlopen("https://www.iroads.co.il/").read()
    soup = bs(html, features="lxml")
    # print(soup)

    # filter
    filter = "מידע-לספקים"
    tags = soup('a')
    for tag in tags:
        link = tag.get('href', None)
        if link is None:
            continue
        if filter in link:
            print(tag.figcaption.string)
        # the_link = tag.get('href', None)
        # if the_link is not None and the_link.find(filter) != -1:
        #     print(tag.get('figcaption', None))
        # print(tag)
if __name__ == '__main__':
    main()

