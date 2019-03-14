from flask import Flask, request, abort, jsonify

import pika


application = Flask(__name__)

QUEUE_SUBJECT = 'food'


def make_message(content):
    return content[QUEUE_SUBJECT]


@application.route('/publish', methods=['POST'])
def publish_message():
    if not request.is_json:
        abort(404)
    try:
        content = request.get_json()
        message = make_message(content)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_SUBJECT)
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_SUBJECT,
                              body=message)
        connection.close()
        return jsonify(sent=message)
    except:
        abort(504)


if __name__ == "__main__":
    application.run()
