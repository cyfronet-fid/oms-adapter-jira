import functools
from time import sleep

import redis_lock

from oms_jira.extensions import redis_client


REDIS_LOCK_POLL_TIME = 1


def singleton_task(f):
    """
    Decorator that prevents a task form being executed with the same task
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Create lock_id used as cache key
        lock_id = f.__name__

        lock = redis_lock.Lock(redis_client, lock_id)

        # allow only one process to run, otherwise remove next tasks in chain
        while not lock.acquire(blocking=False):
            sleep(REDIS_LOCK_POLL_TIME)
        try:
            return f(*args, **kwargs)
        finally:
            lock.release()
    return wrapper
