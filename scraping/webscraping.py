import requests
from bs4 import BeautifulSoup
from db import db
from models import Product, Category
from config import URLS, USER_AGENT


def initialize():
    db.connect()
    db.create_tables([Category, Product])


def web_scrape():
    for u in URLS:
        if u['type'] == 'winwin':
            url = u['url']
            headers = {'User-Agent': USER_AGENT}

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            category = soup.find('div', attrs={'class': 'category-title'})
            category_name = category.text.replace('/', '-').replace('\u0161', 's').replace('\u010d', 'c').replace('\u017e', 'z').strip()
            cat = Category.get_category_by_name(category_name)
            if cat:
                pass
            else:
                cat = Category.create(name=category_name)

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
                model = title.text.replace('/', '-').replace(' ', '-').replace(',', '-').replace('*', '-').replace('.', '-').replace('"', '-').replace('\xa0', '-').replace('\u0161', 's').replace('\u010d', 'c').replace('\u017e', 'z')
                product = Product.get_product_by_title(model)
                if product:
                    pass
                else:
                    Product.create(title=model,
                                   comments=count, price=int(price.text[:-4].replace('.', "")),
                                   url=url.get('href'), category=cat)
