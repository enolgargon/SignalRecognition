from .Message import Message


def put(queue, element):
    # log message
    queue.put(element.to_json())


def get(queue):
    return Message.from_json(queue.get())
