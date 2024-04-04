from abc import ABC, abstractmethod
from datetime import *
from typing import Dict


class Message(ABC):
    def __init__(self, context, to: str, text_to_reply: str, timee):
        self.from_ = context
        self.to: str = to
        self.to_reply: str = text_to_reply
        self.time: datetime = timee
        self.empty = False
        self.time = datetime.now()
        self.closest_time_to_send = datetime.now()

    @abstractmethod
    def send(self):
        pass

    def get_time(self):
        return self.time

    def is_empty(self):
        return self.empty

    def __str__(self) -> str:
        return self.to_reply
    
    def __lt__(self, other):
        return self.closest_time_to_send < other.closest_time_to_send


class MessageSchedule(Message):
    def __init__(self, period: timedelta, start: datetime,  *args, **kwars):
        super().__init__(*args, **kwars)
        self.period = period
        self.start = start
        self.closest_time_to_send = start

    async def send(self):
        await self.from_.send_message(self.to, self.to_reply)
        if self.closest_time_to_send >= datetime.now():
            self.closest_time_to_send = self.set_new_time()

    def set_new_time(self):
        return self.closest_time_to_send + self.period

    def __str__(self) -> str:
        return self.to_reply

    def __lt__(self, other):
        return self.closest_time_to_send < other.closest_time_to_send


class MessageOnce(Message):
    def __init__(self, time_to_send: datetime, *args, **kwars):
        super().__init__(*args, **kwars)
        self.closest_time_to_send = time_to_send

    def __lt__(self, other):
        return self.closest_time_to_send < other.closest_time_to_send

    async def send(self):
        self.create_text()
        await self.from_.send_message(self.to, self.text)
        self.empty = True

    def create_text(self):
        try:
            self.text = generate_text(self.to_reply)
        except Exception as e:
            print(e)
            return -1


def generate_text(prev_msg: str):
    return "Сгенерированный текст"
