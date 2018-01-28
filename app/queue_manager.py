from queue import Queue

queue = Queue()


def add_to_queue(id):
    queue.put(id)


def get_from_queue():
    if queue.not_empty:
        return queue.get()
    else:
        return None
