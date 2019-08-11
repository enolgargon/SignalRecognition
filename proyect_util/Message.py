class Message:
    def __init__(self, sender, title, content, description, image_id):
        self.sender = sender
        self.title = title
        self.content = content
        self.description = description
        self.image_id = image_id

    def __str__(self):
        return f'{self.sender} send "{self.description}"'
