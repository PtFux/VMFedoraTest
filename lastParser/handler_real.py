"""
Handler [Complete]
Класс инициализируется с плагином. Может с помощью этого плагина доставать soup сайта и его каталогов,
может возвращать список элементов (ссылок) с этого сайта

Класс нужно будет использовать дважды. Один раз для получения всех ссылок с сайта,
второй раз для получения soup у конкретного продукта
"""

import bs4
import requests
from bs4 import BeautifulSoup as BS
import plug_in_link as plug


class Handler:
    def __init__(self, plugin):
        self.plugin = plugin

    def find_soup(self, url: str, start_p: int = 1, last_p: int = 1, page: bool = False):
        soups = []
        for i in range(start_p, last_p + 1):
            url_page = self.plugin.url_page(url, i) if page else url
            try:
                html_text = requests.get(url_page).text
                soup_site = BS(html_text, 'html.parser')
                soups.append(soup_site)
            except ConnectionError as ex:
                print(f"[Except] Handler {ex}")
                return None
        return soups

    def find_html(self, url: str, start_p: int = 1, last_p: int = 1, page: bool = False):
        htmls = []
        for i in range(start_p, last_p + 1):
            url_page = self.plugin.url_page(url, i) if page else url
            try:
                html_text = requests.get(url_page).text
                htmls.append(html_text)
            except ConnectionError:
                return None
            except Exception as ex:
                print("[Except] Handler", ex)
                return None

        return htmls

    def links_from_soup(self, soup: bs4.BeautifulSoup):     # find products from website's soup
        return self.plugin.links_from_soup(soup)


if __name__ == '__main__':
    plug = plug.LavkaPlugInLink(plug.LinkData(home_link="https://lavka.yandex.ru"))
    h = Handler(plug)
    my_url = "https://lavka.yandex.ru/213/category/e64b861bd9a34ebc9103dbf15e2d2932"

    soup = h.find_soup(my_url, page=False)
    links = h.links_from_soup(soup[0])
    # print(soup)
    print(*links, sep='\n')
