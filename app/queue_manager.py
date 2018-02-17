from queue import Queue


class QueueManager(object):
    def __init__(self, size=1):
        self._queue = Queue(maxsize=size)
        self._observers = []

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
