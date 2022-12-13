#!/usr/bin/env python
"""
Скрипит читает из web_tasks.txt ссылки на категории товаров в ЯндексЛавке и
кидает в очередь на обработку ссылки на продукты через RabbitMQ
"""

import pika
from handler_real import Handler
import plug_in_link as pgl

# установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# инициализация канала
channel = connection.channel()

# подключение плагина
plug = pgl.LavkaPlugInLink(pgl.LinkData(home_link="https://lavka.yandex.ru"))
# экземпляр обработчика
h = Handler(plug)

# создание exchange
channel.exchange_declare(exchange=plug.get_link_exchange(), exchange_type=plug.get_link_type_exchange())

# читаем файл сайтов с категориями
with open("web_tasks.txt", 'r') as f:
    for line in f:
        print(f"[URL] Обработка {line}")
        my_url = line

        # достаем soup
        soups = h.find_soup(my_url, page=False)
        # достаем ссылки на товары
        links = h.links_from_soup(soups[0])

        for link in links:
            print("[URL] Product's link is", link)
            # кидаем в exchange link
            channel.basic_publish(exchange=plug.get_link_exchange(), routing_key='', body=link,
                                  properties=pika.BasicProperties(
                                      delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
            print(" [x] Sent %r" % link)

# закрываем соединение
connection.close()
