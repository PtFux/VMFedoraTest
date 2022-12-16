from dataclasses import dataclass

import bs4
import requests
from bs4 import BeautifulSoup as BS

"""
Плагин для получения ссылок с сайта
"""


@dataclass
class LinkData:
    home_link: str = ""
    regular_link_p = None   # Надо бы добавить регулярочку для url_page
    param: str = 'a'
    class_a_1: str = "l1nk0t22"
    class_a: str = "l1inc8zk"


@dataclass
class InfoData:
    weight_class: str = "s1l37y20 t18stym3 b1clo64h r88klks r1b0wfc3 lc0zwt5 l14lhr1r"
    price_class: str = "t18stym3 b1clo64h r88klks r1b0wfc3 tnicrlv l14lhr1r"
    name_class: str = "ttu50to t18stym3 hbhlhv b1ba12f6 b1wwsurb n1wpn6v7 l14lhr1r"


@dataclass
class NameRabbitMQ:
    name_exchange_link: str = "LinkLavka"
    name_exchange_soup: str = "SoupLavka"
    exchange_type_link: str = "fanout"
    exchange_type_soup: str = "fanout"


@dataclass
class ForPostgres:
    name_table: str = "lavka"


ForPostgresColumns = {"_id": ("TEXT", "UNIQUE"),
                     "name": ("TEXT", ),
                     "price": ("INT", ),
                     "calories": ("FLOAT", ),
                     "proteins": ("FLOAT", ),
                     "fats": ("FLOAT", ),
                     "carbohydrates": ("FLOAT", )}


class LavkaPlugInLink:
    def __init__(self,
                 get_link: LinkData = LinkData(),
                 get_info: InfoData = InfoData(),
                 get_rabbit: NameRabbitMQ = NameRabbitMQ()):

        self.get_link = get_link
        self.get_info = get_info
        self.get_rabbit = get_rabbit
        self.for_postgres = ForPostgres()
        self.columns_postgres = ForPostgresColumns

    def change_get_link(self, **kwargs):
        self.get_link = LinkData(**kwargs)

    def change_get_info(self, **kwargs):
        self.get_info = InfoData(**kwargs)

    def change_name_rabbit(self, **kwargs):
        self.get_rabbit = NameRabbitMQ(**kwargs)

    def get_link_exchange(self):
        return self.get_rabbit.name_exchange_link

    def get_link_type_exchange(self):
        return self.get_rabbit.exchange_type_link

    def get_soup_exchange(self):
        return self.get_rabbit.name_exchange_soup

    def get_soup_type_exchange(self):
        return self.get_rabbit.exchange_type_soup

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
        crash_flag = False
        params = ["calories", "proteins", "fats", "carbohydrates"]

        ans = dict()
        params_soup = soup.find_all("dd")
        for i in range(len(params_soup)):
            ans.update({params[i]: float(params_soup[i].text.replace(',', '.'))})

        try:
            weight = soup.find('span', class_=self.get_info.weight_class).text.split()[0]
            ans.update({'weight': weight})
        except Exception as ex:
            crash_flag = True
            print("[Except] WEIGHT IS NONE", ex)
            ans.update({'weight': 0})

        try:
            price = soup.find('span', class_=self.get_info.price_class).text.split()[0]
            ans.update({'price': int(price)})
        except Exception as ex:
            crash_flag = True
            print("[Except] PRICE IS NONE", ex)
            ans.update({'price': 0})

        name = soup.find('span', class_=self.get_info.name_class).text
        ans.update({'name': name.replace("\xad", "").replace("\xa0", " ")})
        return ans, crash_flag

    def list_from_dict_for_postgres(self, info: dict):
        ans = []
        for cat in self.columns_postgres.keys():
            ans.append(info.get(cat))
        return ans
