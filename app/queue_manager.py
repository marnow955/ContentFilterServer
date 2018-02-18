from queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler


class QueueManager(object):
    """ If size is 1 the callback functions is run immediately.
        Else callback is run when queue is full or when timeout reached.
        Size equals 0 means that queue is endless, so callback is run on timeout
        Timeout in seconds.
    """

    def __init__(self, size: int = 1, timeout: int = 10):
        self._queue = Queue(maxsize=size)
        self._observers = []
        if size is not 1:
            self._scheduler = BackgroundScheduler()
            self._scheduler.add_job(self._scheduler_job, 'interval', seconds=timeout)
            self._scheduler.start()

    def _scheduler_job(self):
        if not self._queue.empty():
            for callback in self._observers:
                callback()

    def add_to_queue(self, content):
        if content not in self._queue.queue:
            self._queue.put(content)
        if self._queue.full():
            for callback in self._observers:
                callback()

    def bind_to(self, callback):
        self._observers.append(callback)

    def get_from_queue(self):
        if self._queue.not_empty:
            return self._queue.get()
        else:
            return None

    def get_queue_size(self):
        return self._queue.qsize()

    def get_max_queue_size(self):
        return self._queue.maxsize

    def is_queue_empty(self):
        return self._queue.empty()
