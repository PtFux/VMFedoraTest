from dataclasses import dataclass

import bs4
import requests
from bs4 import BeautifulSoup as BS

"""
Плагин для получения ссылок с сайта
"""
# коммент


class AbsPlugInLink:
    def __init__(self):
        pass

    def url_page(self, url: str, page: int):
        return f"{url}$p={page}"

    def links_from_soup(self, soup: bs4.BeautifulSoup):
        return list(soup.find_all('a'))


@dataclass
class LinkData:
    home_link: str = None
    regular_link_p = None
    param: str = 'a'
    class_a: str = "l1nk0t22"


@dataclass
class InfoData:
    weight_class: str = "s1l37y20 t18stym3 b1clo64h r88klks r1b0wfc3 lc0zwt5 l14lhr1r"
    price_class: str = "t18stym3 b1clo64h r88klks r1b0wfc3 tnicrlv l14lhr1r"
    name_class: str = "ttu50to t18stym3 hbhlhv b1ba12f6 b1wwsurb n1wpn6v7 l14lhr1r"


class LavkaPlugInLink(AbsPlugInLink):
    def __init__(self,
                 get_link: LinkData = LinkData(),
                 get_info: InfoData = InfoData()):  # Надо бы добавить регулярочку для url_page

        self.get_link = get_link

        self.get_info = get_info

        super().__init__()

    def url_page(self, url: str, page: int):
        if self.get_link.regular_link_p: return self.get_link.regular_link_p(url, page)
        return f"{url}$p={page}"

    def links_from_soup(self, soup: bs4.BeautifulSoup):
        def f(path_soup):
            return self.get_link.home_link + path_soup.get("href")

        return list(map(f, soup.find_all(self.get_link.param, class_=self.get_link.class_a)))

    def change_param_soup(self, param: int, class_a: str):
        self.get_link.param = param
        self.get_link.class_a = class_a

    def find_info(self, html):
        soup = BS(html, 'html.parser')
        # data = json.loads(soup.find('script', type='application/ld+json').text)
        crash_flag = False
        params = ["calories", "proteins", "fats", "carbohydrates"]

        ans = dict()
        params_soup = soup.find_all("dd")
        for i in range(len(params_soup)):
            ans.update({params[i]: params_soup[i].text})

        try:
            weight = soup.find('span', class_=self.get_info.weight_class).text.split()[0]
            ans.update({'weight': weight})
        except:
            crash_flag = True
            print("WEIGHT IS NONE", html)

        try:
            price = soup.find('span', class_=self.get_info.price_class).text.split()[0]
            ans.update({'price': price})
        except:
            crash_flag = True
            print("PRICE IS NONE", html)

        name = soup.find('span', class_=self.get_info.name_class).text
        ans.update({'name': name.replace("\xad", "").replace("\xa0", " ")})
        return ans, crash_flag