from .LoggerControl import LoggerControl
from .Message import Message
from .TextMessage import TextMessage

def put(queue, element, queue_name='Unknown'):
    LoggerControl().get_logger(element.sender).info(
        f"New element in queue {queue_name} : [{element.title}] {element.description}")
    element.to_json()
    #queue.put(element.to_json())


def get(queue):
    return Message.from_json(queue.get())


def getText(queue):
    return TextMessage.from_json(queue.get())
