from datetime import datetime


class Signal:
    def __init__(self, code, name, appearance_time=datetime.now(), expiration_time=None):
        self.code = code
        self.name = name
        self.appearance_time = appearance_time
        self.expiration_time = expiration_time

    def is_valid(self, current_time=datetime.now()):
        return self.expiration_time is None or self.appearance_time < current_time < self.expiration_time
