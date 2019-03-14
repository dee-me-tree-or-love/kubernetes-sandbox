import os
import logging

POD_NAME = os.environ.get('MY_POD_NAME', 'n/a')

logger = logging.getLogger()


def make_pod_message(message):
    return "[job-%s] %s" % (POD_NAME, str(message))


def cus_log(message):
    logger.error(make_pod_message(message))
