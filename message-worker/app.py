
import os
import time
# TODO: encode the time digest
# import base64
import logging
import traceback

# for rabbitmq connectivity
import pika
# kubernetes API abstraction
from kubernetes import client, config

# FIXME: that's some awful code

QUEUE_SUBJECT = 'food'
NAMESPACE = 'default'
POD_NAME = os.environ.get('MY_POD_NAME', 'n/a')
JOB_WORKER_NAME = 'job-worker'
JOB_ITEM_KEY = 'MY_JOB_ITEM'
JOB_BACKOFF_LIMIT = 5
# FIXME: define the container image in a different way
# FIXME: fix the tag name -> use a different tagger in skaffold?
CONTAINER_IMAGE = 'gcr.io/k8s-skaffold/%s:b4b09c8-dirty' % JOB_WORKER_NAME

logger = logging.getLogger()


def make_pod_message(message):
    return "[wrkr-%s] %s" % (POD_NAME, str(message))


def cus_log(message):
    # FIXME: why should this be error?
    logger.error(make_pod_message(message))


def make_env_var(work_item):
    return client.V1EnvVar(name=JOB_ITEM_KEY, value=str(work_item))


def make_job_name(work_item):
    time_digest = str(time.time())
    return "job-%s-%s" % (work_item, time_digest)


def make_container(work_item):
    container = client.V1Container(
        image=CONTAINER_IMAGE,
        image_pull_policy="IfNotPresent",
        name=JOB_WORKER_NAME,
        env=[make_env_var(work_item)]
    )
    return container


def make_job_template(work_item):
    job_template_spec = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(
            restart_policy="OnFailure",
            containers=[make_container(work_item)]
        )
    )
    return job_template_spec


def make_job(work_item):
    job = client.V1Job()
    job.metadata = client.V1ObjectMeta()
    job.metadata.name = make_job_name(work_item)
    job.spec = client.V1JobSpec(
        template=make_job_template(work_item),
        backoff_limit=JOB_BACKOFF_LIMIT,
        ttl_seconds_after_finished=100
    )
    return job


def submit_job(batch_api, work_item):
    body = make_job(work_item)
    cus_log("Submitting job: %s" % body.metadata.name)
    batch_api.create_namespaced_job("default", body)


def process_body(body):
    config.load_incluster_config()
    batch_api = client.BatchV1Api()
    submit_job(batch_api, str(body))


def parse_body(body):
    return str(body, "utf-8")


def callback(ch, method, properties, body):
    message = parse_body(body)
    cus_log('Received %r' % message)
    process_body(message)


try:
    cus_log('Connecting...')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_SUBJECT)

    channel.basic_consume(callback,
                          queue=QUEUE_SUBJECT,
                          no_ack=True)

    cus_log('Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
except Exception as e:
    cus_log('Got an error: %s' % str(e))
    error = traceback.format_exc()
    cus_log(error)
finally:
    logger.info(make_pod_message('Cleaned up'))
