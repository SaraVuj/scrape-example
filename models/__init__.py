from peewee import *
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Laptop(BaseModel):
    title = CharField()
    comments = IntegerField()
    price = IntegerField()
    url = CharField()

    @staticmethod
    def get_all_laptops():
        return Laptop.select()

    @staticmethod
    def get_laptop_by_title(title):
        laptop = Laptop.select().where(Laptop.title == title)
        if laptop.exists():
            return laptop
        else:
            return None
