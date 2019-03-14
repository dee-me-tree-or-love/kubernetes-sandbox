
import os
import logging

import pika

QUEUE_SUBJECT = 'food'
POD_NAME = os.environ.get('MY_POD_NAME', 'n/a')
logger = logging.getLogger()


def make_pod_message(message):
    return "[wrkr-%s] %s" % (POD_NAME, str(message))


def callback(ch, method, properties, body):
    # FIXME: why should this be error?
    logger.error(make_pod_message('Received %r' % body))


try:
    logger.error(make_pod_message('Connecting...'))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_SUBJECT)

    channel.basic_consume(callback,
                          queue=QUEUE_SUBJECT,
                          no_ack=True)

    logger.error(make_pod_message(
        'Waiting for messages. To exit press CTRL+C')
    )

    channel.start_consuming()
except Exception as e:
    logger.error(make_pod_message('Got an error: %s' % str(e)))
finally:
    logger.info(make_pod_message('Cleaned up'))
