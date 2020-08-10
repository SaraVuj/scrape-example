from scraping.metrics import send_metrics
from scraping.looping import looping

looping(send_metrics)
