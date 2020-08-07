from flask import Flask, render_template, g, request
from db import db
from models import Product

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/products')
def get_all_products():
    return render_template('products.html', products=Product.get_all_products())


@app.route('/products/delete', methods=['POST'])
def delete_product():
    title = request.form['title']
    Product.delete_by_title(title)
    return get_all_products()


@app.route('/products/update', methods=['POST'])
def render_update_product():
    title = request.form['title']
    product = Product.get_product_by_title(title).get()
    return render_template('update_product.html', product=product)


@app.route('/products/updated', methods=['POST'])
def update_product():
    old_title = request.form['old_title']
    product = Product.get_product_by_title(old_title).get()
    product.title = request.form['title']
    product.url = request.form['url']
    product.price = request.form['price']
    product.comments = request.form['comments']
    product.save_changes()
    return get_all_products()
