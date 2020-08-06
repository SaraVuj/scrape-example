from peewee import *
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = CharField()
    comments = IntegerField()
    price = IntegerField()
    url = CharField()

    @staticmethod
    def get_all_products():
        return Product.select()

    @staticmethod
    def get_product_by_title(title):
        product = Product.select().where(Product.title == title)
        if product.exists():
            return product
        else:
            return None
