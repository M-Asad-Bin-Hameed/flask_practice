import os
from loguru import logger
from datetime import datetime

logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)
log_file = os.path.join(logs_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
logger.add(log_file)