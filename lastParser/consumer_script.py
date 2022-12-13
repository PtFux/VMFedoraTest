#!/usr/bin/env python

"""
Файл и читает очередь для soups, берет оттуда супы, распарсивает
и закидывает в базу данных
"""

import pika
import plug_in_link as pgl
from data_base import PostgresDB

# Соединение с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# Инициализая канала
channel = connection.channel()

# Инициализация плагина обработки
plug = pgl.LavkaPlugInLink()
# Инициализация сохранения в бд
save_bd = PostgresDB()
# Подключение к базе данных
save_bd.init_db()
# Создание таблицы в этой базе данных
save_bd.create_table()

# Настройка exchange в RabbitMQ
channel.exchange_declare(exchange=plug.get_soup_exchange(), exchange_type=plug.get_soup_type_exchange())

# Создание очереди
result = channel.queue_declare(queue='', exclusive=True)
# Получение имя очереди
queue_name = result.method.queue

# Связывание очереди и exchange
channel.queue_bind(exchange=plug.get_soup_exchange(), queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    html_text = body.decode()

    info, crash = plug.find_info(html_text)

    save_bd.insert_one(info)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    if crash:
        f = open("bags.txt", 'a')
        f.write(f"{html_text}\n{info}")
        f.close()


# хз, вроде максимальное элементов в очереди
channel.basic_qos(prefetch_count=1)
# настройка получения сообщений с подтверждением получения
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=False)

# Включение  режима ожидания
channel.start_consuming()
