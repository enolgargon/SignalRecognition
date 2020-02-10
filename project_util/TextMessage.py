import json


class TextMessage:
    def __init__(self, sender, title, content, description, image_id):
        self.sender = sender
        self.title = title
        self.content = content
        self.description = description
        self.image_id = image_id

    def __str__(self):
        return f'{self.sender} send "{self.description}"'

    def to_json(self):
        print("Esto si")
        return json.dumps({
            'sender': self.sender,
            'title': self.title,
            'content': self.content,
            'description': self.description,
            'image_id': self.image_id
        })

    @staticmethod
    def from_json(json_content):
        data = json.loads(json_content)
        return TextMessage(data['sender'], data['title'], data['content'], data['description'],
                           data.get('image_id', ''))
