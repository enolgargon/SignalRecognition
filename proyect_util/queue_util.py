from .LoggerControl import LoggerControl
from .Message import Message


def put(queue, element):
    LoggerControl().get_logger(element.sender).info(
        f"New element in queue {queue} : [{element.title}] {element.description}")
    queue.put(element.to_json())


def get(queue):
    return Message.from_json(queue.get())
