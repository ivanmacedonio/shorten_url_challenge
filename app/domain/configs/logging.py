import logging
import logging.handlers
import queue
from logging.handlers import QueueHandler, QueueListener

log_queue = queue.Queue()

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(threadName)s - %(message)s"))

queue_handler = QueueHandler(log_queue)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(queue_handler)

listener = QueueListener(log_queue, stream_handler)
listener.start()

__all__ = ["logger", "listener"]