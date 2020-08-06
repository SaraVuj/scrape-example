from metrics import send_metrics
from looping import looping

looping(send_metrics)
