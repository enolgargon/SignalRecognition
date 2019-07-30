class Message:
    def __init__(self, sender, title, content, description):
        self.sender = sender
        self.title = title
        self.content = content
        self.description = description

    def __str__(self):
        return f'{self.sender} send "{self.description}"'
