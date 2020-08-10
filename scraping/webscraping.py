import requests
from bs4 import BeautifulSoup
from db import db
from models import Laptop
from config import URL, USER_AGENT


def initialize():
    db.connect()
    db.create_tables([Laptop])


def web_scrape():
    url = URL
    headers = {'User-Agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for li in soup.findAll('li', attrs={'class': 'item'}):
        title = li.find('span', attrs={'itemprop': 'name'})
        comments = li.find('div', attrs={'class': 'ratings'}).find('span', attrs={'class': 'text-info'})
        if comments:
            count = int(comments.text)
        else:
            count = 0
        special_price = li.find('p', attrs={'class': 'special-price'})
        if special_price:
            price = special_price.find('span', attrs={'class': 'price'})
        else:
            price = li.find('span', attrs={'class': 'price'})
        url = li.find('a', href=True, attrs={'class': 'product-image'})
        model = title.text.replace('/', '-').replace('.', '-').replace('"', '-').replace('\xa0', '-')
        laptop = Laptop.get_laptop_by_title(model)
        if laptop:
            pass
        else:
            Laptop.create(title=model,
                          comments=count, price=int(price.text[:-4].replace('.', "")),
                          url=url.get('href'))
