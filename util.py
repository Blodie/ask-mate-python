from datetime import datetime
from time import time


def get_current_time():
    return datetime.fromtimestamp(int(time())).strftime("%Y-%m-%d %H:%M:%S")
