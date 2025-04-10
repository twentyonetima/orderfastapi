from celery import Celery
import time
from config import RABBITMQ_URL
import logging
logger = logging.getLogger(__name__)

celery_app = Celery("order_tasks", broker=RABBITMQ_URL)

@celery_app.task
def process_order(order_id: str):
    logger.info("Started processing order")
    time.sleep(2)
    logger.info(f"Order {order_id} processed")