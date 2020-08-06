from models import Laptop
from statsd import StatsClient
from config import STATSD_HOST, STATSD_PORT, STATSD_PREFIX

c = StatsClient(host=STATSD_HOST, port=STATSD_PORT, prefix=STATSD_PREFIX)


def send_metrics():
    for laptop in Laptop.get_all_laptops():
        c.incr(laptop.title + ".comments", laptop.comments)
        c.incr(laptop.title + ".price", laptop.price)
