from peewee import IntegerField, CharField, DateTimeField

from .BaseModel import BaseModel

type_to_code = {
    'prohibition': 0,
    'speed': 1,
    'warning': 2,
    'other': 3
}
code_to_type = {
    0: 'prohibition',
    1: 'speed',
    2: 'warning',
    3: 'other'
}


class Signal(BaseModel):
    code = IntegerField()
    name = CharField()
    appearance_time = DateTimeField()
    expiration_time = DateTimeField()
    type = IntegerField()
