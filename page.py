from magic import *
from tkhtmlview import HTMLLabel


"""
this is a global list of all the display menus
"""
display_menus = []

class FrontPage:
    """
    this class is for building the basic basic front
    """
    def __init__(self):
        self.root = Tk()
        self.subject = Label(self.root, text="?מה תרצו לדעת").pack()
        # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("800x800")


class GetHeaders:
    """
    A class to get the dict with the names of the
    options and links (using threading)
    """
    def __init__(self, clicked, hrefs, url_main):
        self.clicked = clicked
        self.hrefs = hrefs
        self.url_main = url_main
        self.subs_links = {}
        self.subject_url = self.get_subject_url()

    def get_subject_url(self):
        url = requests.get(self.url_main, self.hrefs[self.clicked][1:-1])
        return requests.get(url.url.replace('?', ''))

    @timer
    def get_headers(self):
        """
        function will return a dict of headers-links
        """
        # get the soup
        soup = bs(self.subject_url.text, features="lxml")

        # get the relevant headers
        bigs = soup.findAll('div', class_='container-fluid col9')

        with cf.ThreadPoolExecutor() as executor:
            executor.map(self.parser_head_link, bigs)
        return self.subs_links

    def parser_head_link(self, big):
        try:
            raw_links = big.ul.findAll('li')
        except AttributeError:
            return
        # i want to create a dict with the subjects and links
        # and then add it to the big dict
        spec_links = {}
        for raw in raw_links:
            try:
                spec_links[raw.div.h2.text.replace('\n', '')] = raw.div.div.a.get('href', None)
            except AttributeError:
                print(raw.div.h2.text)
        self.subs_links[big.article.h2.text] = spec_links



class DisplayMenu:
    """
    this class is for creating the label and the option menu. that's it!
    """
    def __init__(self, root, text, options, first, sub_links, url):
        self.root = root
        self.clicked = StringVar()
        self.clicked.set("לא נחבר")
        self.first = first

        self.label = Label(self.root, text=text)
        self.drop = OptionMenu(self.root, self.clicked, *options)
        self.button = MyButton(self, sub_links, url)

    def pack(self):
        self.label.pack()
        self.drop.pack()
        self.button.button.pack()

    def remove(self):
        self.label.destroy()
        self.drop.destroy()
        self.button.button.destroy()


class MyButton:
    """
    the class for the buttons of the program
    """
    def __init__(self, menu, sub_links, url):
        self.sub_links = sub_links
        self.url = url
        self.menu = menu
        self.button = Button(self.menu.root, text="!בחרתי", command=self.get)

    def get(self):
        """
        if it is the first option menu create the second one
        if it's the second, ask the question and make the magic happen
        """
        if self.menu.first:
            self.__cleaning_menus(1)
            # find the subs -- function
            try:
                header = GetHeaders(str(self.menu.clicked.get()), self.sub_links, self.url)
                subject_url = header.subject_url
                sub_subs_links = header.get_headers()

                # create another display menu
                try:
                    sub_menu = DisplayMenu(self.menu.root, ":מה הנושא המשני", sub_subs_links.keys(), False,
                                           sub_subs_links, subject_url)
                    display_menus.append(sub_menu)
                    sub_menu.pack()

                except (TypeError, AttributeError):
                    bad = NoHeads(self.menu.root, ":אין כותרות זמינות, לגישה לדף לחץ על הקישור", subject_url.url)
                    display_menus.append(bad)
                    bad.pack()

            except KeyError:
                bad = UserCheck(self.menu.root, "נא לבחור אופציה")
                display_menus.append(bad)
                bad.pack()

        else:
            """
            ask the fucking question
            """
            self.__cleaning_menus(2)
            # it's recursive
            try:
                question = TheQuestion(self.menu.root, self.sub_links[self.menu.clicked.get()])
                question.show()
                display_menus.append(question)
            except KeyError:
                bad = UserCheck(self.menu.root, "נא לבחור אופציה")
                display_menus.append(bad)
                bad.pack()

    @staticmethod
    def __cleaning_menus(which_menu):
        start_length = len(display_menus)
        if start_length > which_menu:
            print(f"wich: {which_menu}")
            print(start_length)
            for i, item in enumerate(display_menus[:]):
                if i < which_menu:
                    continue
                item.remove()
                display_menus.remove(item)


class UserCheck:
    """ this is for checking the user """
    def __init__(self, root, label_text):
        self.bad_label = Label(root, text=f"{label_text}")

    def remove(self):
        self.bad_label.destroy()

    def pack(self):
        self.bad_label.pack()


class NoHeads(UserCheck):
    def __init__(self, root, label_text, link):
        super().__init__(root, label_text)
        self.link_label = HTMLLabel(root, html=f'<a href="{link}"> Link to page </a>')

    def remove(self):
        self.bad_label.destroy()
        self.link_label.destroy()

    def pack(self):
        self.bad_label.pack()
        self.link_label.pack()


class TheQuestion:
    def __init__(self, root, subject_links):
        self.subject_links = subject_links
        self.input = Entry(root)
        self.dif_button = Button(root, text="?מה השאלה", command=self.go)

    def show(self):
        self.input.pack()
        self.dif_button.pack()

    def remove(self):
        self.input.destroy()
        self.dif_button.destroy()

    def go(self):
        # initialize the class
        loading = LoadText(self.subject_links)
        # get the dict
        texts = loading.get_texts()


        print("fuck")
