import requests
from bs4 import BeautifulSoup as BS
import configparser  # импортируем библиотеку
import json

"""
Модуль обработки текста html - возвращает словари данных продуктов
"""


class LavkaSoup:
    def __init__(self):
        self.weight_class = "s1l37y20 t18stym3 b1clo64h r88klks r1b0wfc3 lc0zwt5 l14lhr1r"
        self.price_class = "t18stym3 b1clo64h r88klks r1b0wfc3 tnicrlv l14lhr1r"
        self.name_class = "ttu50to t18stym3 hbhlhv b1ba12f6 b1wwsurb n1wpn6v7 l14lhr1r"

    def find_info(self, html):
        soup = BS(html, 'html.parser')
        # data = json.loads(soup.find('script', type='application/ld+json').text)
        params = ["calories", "proteins", "fats", "carbohydrates"]

        ans = dict()
        params_soup = soup.find_all("dd")
        for i in range(len(params_soup)):
            ans.update({params[i]: params_soup[i].text})

        weight = soup.find('span', class_=self.weight_class).text.split()[0]
        ans.update({'weight': weight})

        price = soup.find('span', class_=self.price_class).text.split()[0]
        ans.update({'price': price})

        name = soup.find('span', class_=self.name_class).text
        ans.update({'name': name.replace("\xad", "")})
        return ans
