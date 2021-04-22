from magic import *
from tkhtmlview import HTMLLabel
# from tk_html_widgets import HTMLLabel
from ttkthemes import ThemedTk
from tkinter import ttk


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
        with cf.ThreadPoolExecutor() as executor:
            executor.map(self._parser_head_link, bigs)
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
            return None, None


class DisplayMenu2(DisplayMenu):
    def _get(self):
        display_menus.removing_items(2)

        self._catch_display_menu2()

    def _catch_display_menu2(self):
        try:
            self._make_menu2()
        except (TypeError, AttributeError):
            self._catch_error()

    def _make_menu2(self):
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
        self._subject_link = subject_link
        self._root = root
        self._input = ttk.Entry(root, width=30)
        self.dif_button = ttk.Button(self._root, text="?מה השאלה", command=self.go)
        self._name = name

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
            wait = UserCheck(self._root, "...אל תסגור את התוכנה עכשיו")
            wait.show()
            wait.bad_label.update()

            text_extracter = Text(self._name, self._subject_link)
            wait.remove()
            wait.bad_label.update()

            hold_on = UserCheck(self._root, "...רק עוד רגע")
            hold_on.show()
            hold_on.bad_label.update()

            super_ai = TFIDF(text_extracter.get_text(), input)
            hold_on.remove()

            top_pages = super_ai.get_top_options()
            answer_the_man = TheAnswer(self._root, top_pages, self._subject_link)
            answer_the_man.show()
        else:
            bad_user = UserCheck(self._root, "נא לבחור אופציה")
            bad_user.show()
        print("fuck")


class TheAnswer:
    def __init__(self, root, top_options, file_link):
        self._root = root
        self._file_link = file_link
        self._top_options_links = self._make_links(top_options)
        print(f"this is the second list: {self._top_options_links}")
        self._show_answer()

    def _show_answer(self):
        display_menus.removing_items(5)
        if self._no_answer():
            self._show_no_answer()
        else:
            self._first = NoHeads(self._root, "!התשובה שלך", self._top_options_links[0])
            self._list_of_widgets = self._add_widjets()

    def _no_answer(self):
        return True if len(self._top_options_links) == 0 else False

    def _show_no_answer(self):
        bad = UserCheck(self._root, "לא נמצאה תשובה, בבקשה לנסח את השאלה טוב יותר")
        bad.show()

    def _add_widjets(self):
        my_list = list()
        my_list.append(self._first)
        return my_list

    def _make_links(self, top_options):
        links = []
        for option in top_options:
            link = self._file_link + f"#p={option+1}"
            links.append(link)
        return links

    def show(self):
        for widjet in self._list_of_widgets:
            widjet.show()

    def remove(self):
        for widjet in self._list_of_widgets:
            widjet.remove()


