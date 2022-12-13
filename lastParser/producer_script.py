#!/usr/bin/env python
"""
Скрипит читает из web_tasks.txt ссылки и
кидает в очередь на обработку ссылки на продукты
"""

import pika
from handler_real import Handler
import plug_in_link as pgl
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='LinkLavka', exchange_type='fanout')

plug = pgl.LavkaPlugInLink(pgl.LinkData(home_link="https://lavka.yandex.ru"))
h = Handler(plug)

f = open("web_tasks.txt", 'r')
for line in f:
    print(line)

    my_url = line

    soups = h.find_soup(my_url, page=False)
    links = h.links_from_soup(soups[0])
    print(len(soups))

    print(soups[0].find_all("a"))
    for link in links:
        print("link is", link)
        channel.basic_publish(exchange='LinkLavka', routing_key='', body=link,
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        print(" [x] Sent %r" % link)


f.close()

connection.close()

"""
Нужно создать exchange с разветлевлением и парочку рандомных очередей
В очередях настроить автоудаление maybe
Читать из файла (мб конфиг) ссылки и кидать их в exchange
"""
