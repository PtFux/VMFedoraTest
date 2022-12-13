#!/usr/bin/env python
"""
Файл и читает одну очередь, берет оттуда ссылки и в созданный другой обменник кидает
получившейся супы продуктов
"""

import pika
from handler_real import Handler
import plug_in_link as pgl

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

plug = pgl.LavkaPlugInLink(pgl.LinkData(home_link="https://lavka.yandex.ru"))
h = Handler(plug)
channel.exchange_declare(exchange='LinkLavka', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='LinkLavka', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    chan = conn.channel()

    chan.exchange_declare(exchange='LinkLavkaSoup', exchange_type='fanout')

    print(" [x] Received %r" % body.decode())

    my_url = body.decode()
    message = h.find_html(my_url, page=False)[0]

    if message is None:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    message = str(message)
    chan.basic_publish(exchange='LinkLavkaSoup', routing_key='', body=message,
                       properties=pika.BasicProperties(
                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=False)

channel.start_consuming()
