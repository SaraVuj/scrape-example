from flask import Flask, g, request, jsonify, redirect, url_for
from db import db
from models import Product
from flask_httpauth import HTTPTokenAuth
from config import TOKEN
from base64 import b64decode, b64encode
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

auth_token = b64encode(TOKEN.encode())


@auth.verify_token
def verify_token(token):
    if b64decode(token).decode() == TOKEN:
        return auth_token


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/products')
@auth.login_required
def get_all_products():
    products = Product.get_all_products()
    return jsonify([product.to_json() for product in products])


@app.route('/products/<title>')
@auth.login_required
def get_product(title):
    product = Product.get_product_by_title(title).get()
    return product.to_json()


@app.route('/products/<title>', methods=['DELETE'])
@auth.login_required
def delete_product(title):
    Product.delete_by_title(title)
    return redirect(url_for('get_all_products'))


@app.route('/products/<title>', methods=['PUT'])
@auth.login_required
def update_product(title):
    old_title = title
    product = Product.get_product_by_title(old_title).get()
    product.title = request.form['title']
    product.url = request.form['url']
    product.price = request.form['price']
    product.comments = request.form['comments']
    product.save_changes()
    return redirect(url_for('get_product', title=product.title))


if __name__ == '__main__':
    app.run(debug=True)
