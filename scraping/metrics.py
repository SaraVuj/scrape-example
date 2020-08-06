from models import Product
from statsd import StatsClient
from config import STATSD_HOST, STATSD_PORT, STATSD_PREFIX

c = StatsClient(host=STATSD_HOST, port=STATSD_PORT, prefix=STATSD_PREFIX)


def send_metrics():
    for product in Product.get_all_products():
        c.incr(product.title + ".comments", product.comments)
        c.incr(product.title + ".price", product.price)
