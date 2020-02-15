from datetime import datetime

from .Signal import Signal


class ProhibitionSignal(Signal):
    def __init__(self, code, name, appearance_time=datetime.now()):
        super().__init__(code, name, appearance_time)

    def invalidate(self, current_time=datetime.now()):
        super().expiration_time = current_time
