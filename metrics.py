from app import Laptop
from app import db, timeout
from statsd import StatsClient
from twisted.internet import task, reactor
c = StatsClient(host="192.168.76.140",port=8125,prefix="laptopovi")

db.connect()
def send_matrics():
    for laptop in Laptop.select():
        c.incr(laptop.naziv.replace('\xa0', ' ') + ".comments", laptop.broj_komentara)
        c.incr(laptop.naziv.replace('\xa0', ' ') + ".price", laptop.cena)

def sending():
    loop = task.LoopingCall(send_matrics)
    loop.start(timeout)
    reactor.run()

db.close()