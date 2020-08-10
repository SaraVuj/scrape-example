from models import Product, Category
from statsd import StatsClient
from config import STATSD_HOST, STATSD_PORT, STATSD_PREFIX

c = StatsClient(host=STATSD_HOST, port=STATSD_PORT, prefix=STATSD_PREFIX)


def send_metrics():
    for category in Category.get_all_categories():
        for product in category.get_all_products_for_category():
            c.incr(category.name + '.' + product.title + ".comments", product.comments)
            c.incr(category.name + '.' + product.title + ".price", product.price)
