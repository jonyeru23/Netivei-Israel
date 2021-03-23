from page import *
from helper import *
from time import sleep
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
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
    # access the right link

    # parse the htmkl using bs
    # get to this link
    # file_url = "http://online.fliphtml5.com/kfky/pzdc/"
    # r = requests.get(file_url)
    # soup = bs(r.text, features="lxml")
    # links = soup.findAll('script')
    # page = requests.get(file_url + links[5].get('src', None))
    #
    # text = page.text.encode("latin1").decode("utf-8")
    # text = re.sub("\s\s+", " ", text)
    #
    # print(text)
    """checking pdfs"""
    # req = requests.get("https://www.iroads.co.il/media/11845/%D7%AA%D7%91%D7%97%D7%99%D7%A0%D7%99-%D7%92%D7%9E%D7%99%D7%A9%D7%95%D7%99%D7%95%D7%AA-%D7%9C%D7%94%D7%A0%D7%97%D7%99%D7%95%D7%AA-%D7%9E%D7%A9%D7%A8%D7%93-%D7%94%D7%AA%D7%97%D7%91%D7%95%D7%A8%D7%94.pdf")
    # # full_path = os.path.join(self.path, item[0])
    # with open('text.pdf', "wb") as f:
    #     for chunk in req.iter_content(chunk_size=8192):
    #         f.write(chunk)
    # return full_path
    output_string = StringIO()
    with open('text.pdf', 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    print(output_string.getvalue())



if __name__ == '__main__':
    main()

