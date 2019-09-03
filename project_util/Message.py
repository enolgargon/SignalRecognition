import json

import cv2


class Message:
    base_image_route = '../../images/'

    def __init__(self, sender, title, content, description, image_id):
        self.sender = sender
        self.title = title
        self.content = content
        self.description = description
        self.image_id = image_id

    def __str__(self):
        return f'{self.sender} send "{self.description}"'

    def to_json(self):
        cv2.imwrite(Message.base_image_route + self.image_id + '.png', self.content)
        return json.dumps({
            'sender': self.sender,
            'title': self.title,
            'description': self.description,
            'image_id': self.image_id
        })

    @staticmethod
    def from_json(json_content):
        data = json.loads(json_content)
        return Message(data['sender'], data['title'], cv2.imread(Message.base_image_route + data['image_id'] + '.png'),
                       data['description'], data['image_id'])
