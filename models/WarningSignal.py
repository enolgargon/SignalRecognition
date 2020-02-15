from datetime import datetime, timedelta

from .Signal import Signal


class WarningSignal(Signal):
    def __init__(self, code, name, appearance_time=datetime.now(), duration=5):
        super().__init__(code, name, appearance_time, appearance_time + timedelta(minutes=duration))
