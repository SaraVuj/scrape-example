from peewee import *
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = CharField()

    @staticmethod
    def get_all_categories():
        return Category.select()

    @staticmethod
    def get_category_by_name(name):
        category = Category.select().where(Category.name == name)
        if category.exists():
            return category
        else:
            return None

    def get_all_products_for_category(self):
        return Product.select().where(Product.category == self)


class Product(BaseModel):
    title = CharField()
    comments = IntegerField()
    price = IntegerField()
    url = CharField()
    category = ForeignKeyField(Category, backref='products')

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

    @staticmethod
    def delete_by_title(title):
        product = Product.get(Product.title == title)
        product.delete_instance()

    def save_changes(self):
        self.save()
