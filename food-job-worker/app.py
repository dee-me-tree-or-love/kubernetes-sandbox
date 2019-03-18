import os

from processor import process_input
from custom_logger import cus_log


def get_job_item():
    item = os.environ.get('MY_JOB_ITEM')
    if item is None:
        raise ValueError('job is not available')
    return item


if __name__ == "__main__":
    try:
        item = get_job_item()
        result = process_input(item)
        cus_log("Final result: %s" % result)
        cus_log("Done.")
    except Exception as e:
        cus_log("Caught an error! %s" % str(e))
        exit(1)
