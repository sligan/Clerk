from datetime import datetime, timedelta
import schedule
import threading
import time
from math import floor


def timestamps(days):
    return datetime.today() - timedelta(days=days)


def start_day():
    x = datetime.strptime("01/01/21", "%m/%d/%y")
    y = datetime.today() - x
    return y.days


def compare(x, y):
    try:
        z = float(x) / float(y) * 100 - 100
        if z < 0:
            return f'▼ {floor(z)}%'
        elif z == 0:
            return '0%'
        elif z > 0:
            return f'▲ +{floor(z)}%'
        else:
            return '0%'
    except ZeroDivisionError:
        return '0%'


def compare2_0(lower, higher):
    try:
        z = int(lower) / int(higher) * 100
        if z == 0:
            return '0'
        elif z > 0:
            return f'{floor(z)}'
    except ZeroDivisionError:
        return '0'
    except TypeError:
        return '0'


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


stop_run_continuously = run_continuously()
