from flask import Flask, render_template, g, request, jsonify
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
    products = Product.get_all_products()
    return jsonify([product.json() for product in products])
    # return render_template('products.html', products=products)


@app.route('/products/<title>')
def get_product(title):
    product = Product.get_product_by_title(title).get()
    return product.json()


@app.route('/products/<title>', methods=['DELETE'])
def delete_product(title):
    # title = request.form['title']
    Product.delete_by_title(title)
    return get_all_products()

#
# @app.route('/products/<title>', methods=['POST'])
# def render_update_product(title):
#     # title = request.form['title']
#     product = Product.get_product_by_title(title).get()
#     return render_template('update_product.html', product=product)


@app.route('/products/<title>', methods=['PUT'])
def update_product(title):
    # old_title = request.form.get('old_title')
    old_title = title
    product = Product.get_product_by_title(old_title).get()
    product.title = request.form['title']
    product.url = request.form['url']
    product.price = request.form['price']
    product.comments = request.form['comments']
    product.save_changes()
    return product.json()


if __name__ == '__main__':
    app.run(debug=True)
