#!/usr/bin/env python
"""
Файл и читает очередь LinkLavkaSoup, берет оттуда супы, распарсивает
и закидывает в базу данных
"""

import pika
# from info_in_soup import LavkaSoup
import plug_in_link as pgl
from data_base import PostgresDB


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

lavka = pgl.LavkaPlugInLink()
save_bd = PostgresDB()
save_bd.init_db()
save_bd.create_table()

channel.exchange_declare(exchange='LinkLavkaSoup', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='LinkLavkaSoup', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    html_text = body.decode()

    info, crash = lavka.find_info(html_text)

    save_bd.insert_one(info)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    if crash:
        f = open("bags.txt", 'a')
        f.write(f"{html_text}\n{info}")
        f.close()


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=False)

channel.start_consuming()
