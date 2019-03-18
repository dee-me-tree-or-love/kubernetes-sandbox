from flask import Flask, request, abort, jsonify

import pika


application = Flask(__name__)


def make_subject(content):
    return str(next(iter(content.keys())))


def make_message(content):
    return str(next(iter(content.values())))


def prepare_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))


def prepare_channel(connection, subject):
    channel = connection.channel()
    channel.queue_declare(queue=subject)
    return channel


def send_message(channel, message, subject):
    channel.basic_publish(exchange='', routing_key=subject, body=message)


def close_connection(connection):
    connection.close()


def process_request_content(content):
    subject = make_subject(content)
    message = make_message(content)

    connection = prepare_connection()
    channel = prepare_channel(connection, subject)
    send_message(channel, message, subject)
    close_connection(connection)

    return (message, subject)


@application.route('/publish', methods=['POST'])
def publish_message():
    if not request.is_json:
        abort(404)
    try:
        content = request.get_json()
        message, subject = process_request_content(content)

        return jsonify(sent=message, subject=subject)
    except:
        abort(504)


if __name__ == "__main__":
    application.run()
