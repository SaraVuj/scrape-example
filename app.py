import requests
from peewee import *
from bs4 import BeautifulSoup
from twisted.internet import task, reactor
db=SqliteDatabase('laptopovi.db')


class BaseModel(Model):
    class Meta:
        database=db

class Laptop(BaseModel):
    naziv=CharField()
    broj_komentara=IntegerField()
    cena=IntegerField()
    url=CharField()

db.connect()
db.create_tables([Laptop])

timeout=600.0

def webScrape():
    url = "https://www.winwin.rs/laptop-i-tablet-racunari/laptop-notebook-racunari.html?manufacturer=53794"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    print("executing")

    for li in soup.findAll('li', attrs={'class':'item'}):

        naziv=li.find('span', attrs={'itemprop':'name'})
        #print(naziv.text.replace('/',"-").replace('.',"-").replace('"',"-"))
        broj_komentara=li.find('div', attrs={'class':'ratings'}).find('span',attrs={'class':'text-info'})
        if broj_komentara:
            #print(broj_komentara.text)
            broj=int(broj_komentara.text)
        else:
            broj=0
        special_price = li.find('p',attrs={'class':'special-price'})
        if special_price:
            cena = special_price.find('span',attrs={'class':'price'})
        else:
            cena=li.find('span',attrs={'class':'price'})
        #print(cena.text[:-4]) # RSD izbacen
        url=li.find('a', href=True, attrs={'class':'product-image'})
        #print(url.get('href'))
        model=naziv.text.replace('/',"-").replace('.',"-").replace('"',"-")
        laptop = Laptop.select().where(Laptop.naziv == model)
        if laptop.exists():
           pass
        else:
            Laptop.create(naziv=model,
                          broj_komentara=broj, cena=int(cena.text[:-4].replace('.', "")),
                          url=url.get('href'))


loop = task.LoopingCall(webScrape)
loop.start(timeout)
reactor.run()
db.close()