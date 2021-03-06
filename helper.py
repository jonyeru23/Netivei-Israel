from urllib import request

Format = "utf-8"

def get_html_page(url):
    """
    returns a string based html page
    """
    url = request.urlopen(url)
    return url.read().decode(Format)
