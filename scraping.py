from scraping.webscraping import initialize
from scraping.webscraping import web_scrape
from scraping.looping import looping

initialize()
looping(web_scrape)
