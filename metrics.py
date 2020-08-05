from app import Laptop
from app import db
from statsd import StatsClient
c = StatsClient(host="192.168.76.140",port=8125,prefix="laptopovi")

db.connect()
for laptop in Laptop.select():
    c.incr(laptop.naziv.replace('\xa0', ' ') + ".comments", laptop.broj_komentara)
    c.incr(laptop.naziv.replace('\xa0', ' ') + ".price", laptop.cena)
db.close()