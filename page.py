from magic import *
from tkhtmlview import HTMLLabel
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import *
import webbrowser
from bs4 import BeautifulSoup as bs
import requests


class ListOfObjects:
    """job: handle adding and removing objects from the list of objects"""

    def __init__(self):
        self._objects = []

    def append(self, widjet):
        self._objects.append(widjet)

    def removing_items(self, which_menu):
        if self._is_click_not_valid(which_menu):
            self._looping_through_items(which_menu)

    def _is_click_not_valid(self, which_menu):
        if len(self._objects) > which_menu:
            return True
        else:
            return False

    def _looping_through_items(self, which_menu):
        for index, item in enumerate(self._objects[:]):
            if self._is_bigger(index, which_menu):
                continue
            self._remove_item(item)

    def _remove_item(self, widjet):
        widjet.remove()
        self._objects.remove(widjet)

    @staticmethod
    def _is_bigger(index, which_menu):
        return True if index < which_menu else False


display_menus = ListOfObjects()


class FrontPage:
    """
    this class is for building the basic basic front
    """
    def __init__(self):
        self.root = ThemedTk(themebg=True)
        self.root.set_theme('adapta')
        # self.subject = ttk.Label(self.root, text="?מה תרצו לדעת").pack()
        # build the screen
        self.root.title("למצוא את התקן")
        self.root.geometry("400x420")


class GetHeaders:
    def __init__(self, root, url_main, the_filter):
        self._root = root
        self._url_main = url_main
        self._the_filter = the_filter
        self.hrefs = {}

    def get_hrefs(self):
        """
        get me the subjects and return
        a dict of option - href
        """
        html = self._get_request()
        if html is None:
            return
        return self._loop_over_tags(html)

    def _get_request(self):
        try:
            return requests.get(self._url_main).text
        except (ConnectionError, TimeoutError):
            self._show_state_to_user()
            return

    def _show_state_to_user(self):
        no_internet = UserCheck(self._root, "אין חיובר אינטרנט, נא לבדוק את החיבור")
        no_internet.show()

    @staticmethod
    def _get_html_elements(html, tag, class_):
        soup = bs(html, features="lxml")
        tags = soup.findAll(tag, class_=class_)
        return tags

    def _loop_over_tags(self, html):
        for tag in self._get_html_elements(html, 'a', 'infoIcon'):
            link = tag.get('href', None)
            if link is None:
                continue
            if self._the_filter in link:
                self._add_option(tag, link)
        return self.hrefs

    def _add_option(self, tag, link):
        option = tag.figcaption.string
        self.hrefs[option] = link


class GetSubHeaders(GetHeaders):
    """
    A class to get the dict with the names of the
    options and links (using threading)
    """
    def __init__(self, root, clicked, hrefs, url_main):
        super().__init__(root, url_main, the_filter="מידע לספקים")
        self._clicked = clicked
        self._sub_hrefs = hrefs
        self._subject_url = self._get_url_request()
        self._spec_links = {}
        self.subs_links = {}

    def get_headers(self):
        """
        function will return a dict of headers-links
        """
        bigs = self._get_html_elements(self._subject_url.text, 'div', 'container-fluid col9')
        # with cf.ThreadPoolExecutor() as executor:
        #     executor.map(self._parser_head_link, bigs)
        #     executor.shutdown(wait=True)
        for big in bigs:
            self._parser_head_link(big)
        return self.subs_links

    def _get_url_request(self):
        try:
            url = requests.get(self._url_main, self._sub_hrefs[self._clicked][1:-1])
            return requests.get(url.url.replace('?', ''))
        except (ConnectionError, TimeoutError):
            self._show_state_to_user()

    def _parser_head_link(self, big):
        raw_links = self._get_raw_links(big)
        if raw_links is None:
            return
        self._spec_links = {}
        for raw in raw_links:
            self._build_dict(raw)
        self.subs_links[big.article.h2.text] = self._spec_links

    def _build_dict(self, raw):
        try:
            self._spec_links[self._get_name(raw)] = self._get_href(raw)
        except AttributeError:
            self._show_error(raw)

    @staticmethod
    def _get_href(raw):
        return raw.div.div.a.get('href', None)

    @staticmethod
    def _get_name(raw):
        return raw.div.h2.text.replace('\n', '')

    def _show_error(self, raw):
        bad = UserCheck(self._root, f"לא הצלחנו להגיע ל{raw.div.h2.text}")
        bad.show()

    @staticmethod
    def _get_raw_links(big):
        try:
            return big.ul.findAll('li')
        except AttributeError:
            return


class DisplayMenu:
    """
    the father class to create the two display menus
    """
    def __init__(self, root, text, sub_links):
        self.root = root
        self.clicked = StringVar()
        self.sub_links = sub_links

        self._make_l_d_b(text, sub_links.keys())

    def _make_l_d_b(self, text, options):
        self.label = ttk.Label(self.root, text=text)
        self.drop = ttk.OptionMenu(self.root, self.clicked, "בחר אפשרות", *options)
        self.button = ttk.Button(self.root, text="!בחרתי", command=self._get)

    def show(self):
        self.label.pack()
        self.drop.pack()
        self.button.pack()
        display_menus.append(self)

    def remove(self):
        self.label.destroy()
        self.drop.destroy()
        self.button.destroy()

    def _get(self):
        pass

    def _show_bad_user(self):
        bad = UserCheck(self.root, "נא לבחור אופציה")
        bad.show()

    def _catch_display_menu(self, sub_subs_links):
        try:
            self._make_menu(sub_subs_links)
        except (TypeError, AttributeError):
            self._catch_error()

    def _make_menu(self, sub_subs_links):
        sub_menu = DisplayMenu2(self.root, ":מה הנושא המשני", sub_subs_links)
        sub_menu.show()

    def _catch_error(self):
        self._show_bad_user()


class DisplayMenu1(DisplayMenu):
    def __init__(self, root, text, sub_links, url):
        super().__init__(root, text, sub_links)
        self.url = url
    """the first one """
    def _get(self):
        display_menus.removing_items(1)
        # find the subs -- function
        sub_subs_links = self._get_url_links()
        if sub_subs_links is None:
            return
        # create another display menu
        self._catch_display_menu(sub_subs_links)

    def _get_url_links(self):
        try:
            header = GetSubHeaders(self.root, str(self.clicked.get()), self.sub_links, self.url)
            return header.get_headers()
        except KeyError:
            self._show_bad_user()
            return None


class DisplayMenu2(DisplayMenu):
    def _get(self):
        display_menus.removing_items(2)

        self._catch_display_menu2()

    def _catch_display_menu2(self):
        try:
            self._make_menu3()
        except (TypeError, AttributeError, KeyError):
            self._catch_error()

    def _make_menu3(self):
        third = DisplayMenu3(self.root, "?מה המסמך שתרצה לחפש בו", self.sub_links[self.clicked.get()])
        third.show()


class DisplayMenu3(DisplayMenu):
    """the second one"""
    def _get(self):
        """
        ask the fucking question
        """
        display_menus.removing_items(3)
        self._try_2_ask()

    def _try_2_ask(self):
        try:
            self._ask_the_question()
        except KeyError:
            self._show_bad_user()

    def _ask_the_question(self):
        question = TheQuestion(self.root, self.clicked.get(), self.sub_links[self.clicked.get()])
        question.show()


class UserCheck:
    """ this is for checking the user """
    def __init__(self, root, label_text):
        self.bad_label = ttk.Label(root, text=f"{label_text}")

    def remove(self):
        self.bad_label.destroy()

    def show(self):
        self.bad_label.pack()
        display_menus.append(self)


class NoHeads(UserCheck):
    def __init__(self, root, label_text, link):
        super().__init__(root, label_text)
        self.link_label = HTMLLabel(root,
                                    html=f'<a href="{link}">Link to page</a>')

    def remove(self):
        self.bad_label.destroy()
        self.link_label.destroy()

    def show(self):
        self.bad_label.pack()
        self.link_label.pack()
        display_menus.append(self)


class TheQuestion:
    def __init__(self, root, name, subject_link):
        self._subject_link = self._is_link_valid(subject_link)
        self._root = root
        self._input = ttk.Entry(root, width=30)
        self.dif_button = ttk.Button(self._root, text="?מה השאלה", command=self.go)
        self._name = name

    @staticmethod
    def _is_link_valid(subject_link):
        if subject_link[0] != 'h':
            subject_link = url_main + subject_link
        req = requests.get(subject_link)
        return req.url

    def show(self):
        self._input.pack()
        self.dif_button.pack()
        display_menus.append(self)

    def remove(self):
        self._input.destroy()
        self.dif_button.destroy()

    @timer
    def go(self):
        display_menus.removing_items(4)
        input = self._input.get()
        if len(input) != 0:
            wait = self._add_funny_sentence("...אל תסגור את התוכנה עכשיו")

            text_extracter = TexT(self._name, self._subject_link)
            wait.remove()
            wait.bad_label.update()

            hold_on = self._add_funny_sentence("...רק עוד רגע")

            super_ai = TFIDF(text_extracter.get_text(), input)
            hold_on.remove()

            top_pages = super_ai.get_top_options()
            answer_the_man = TheAnswer(self._root, top_pages, self._subject_link)
            answer_the_man.show_answer()
        else:
            bad_user = UserCheck(self._root, "נא לבחור אופציה")
            bad_user.show()
        print("fuck")

    @timer
    def _add_funny_sentence(self, text):
        wait = UserCheck(self._root, text)
        wait.show()
        wait.bad_label.update()
        return wait


class TheAnswer:
    def __init__(self, root, top_options, file_link):
        self._root = root
        self._file_link = file_link
        self._top_option = top_options
        print(top_options)

    def show_answer(self):
        display_menus.removing_items(5)
        if self._no_answer():
            self._show_no_answer()

        self._show_web_page()

    def _show_web_page(self):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        webpage = self._get_link()
        webbrowser.register('chrome',
                            None,
                            webbrowser.BackgroundBrowser(
                                chrome_path))
        webbrowser.get('chrome').open(webpage)

    def _get_link(self):
        top = self._top_option[0] + 1
        if pdf in self._file_link:
            return f"{self._file_link}#page={top}"

        elif flip in self._file_link:
            return f"{self._file_link}#p={top}"

        else:
            print("i'm fucked")

    def _no_answer(self):
        return True if len(self._top_option) == 0 else False

    def _show_no_answer(self):
        bad = UserCheck(self._root, "לא נמצאה תשובה, בבקשה לנסח את השאלה טוב יותר")
        bad.show()

