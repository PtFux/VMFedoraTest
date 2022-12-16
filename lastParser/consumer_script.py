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
saver_bd = PostgresDB()
# Подключение к базе данных
saver_bd.init_db()

# Создание таблицы в этой базе данных
# saver_bd.create_table()
if (plug.for_postgres.name_table, ) not in saver_bd.check_tables():
    saver_bd.create_table(plug.for_postgres.name_table, plug.columns_postgres)
    saver_bd.commit_connection()

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
    html_text, url = body.decode().split("%%%")

    info, crash = plug.find_info(html_text, url)
    saver_bd.insert_one(info)

    value = tuple(plug.list_from_dict_for_postgres(info))
    print(value)
    saver_bd.insert(plug.for_postgres.name_table, value)
    saver_bd.commit_connection()

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
