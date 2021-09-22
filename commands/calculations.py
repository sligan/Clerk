from datetime import datetime, timedelta
import schedule
import threading
import time


# если нужно высчитать какой-либо день
def timestamps(days):
    return datetime.today() - timedelta(days=days)


# возвращает кол-во дней прошедших с начала года
def start_day():
    x = datetime.strptime("01/01/21", "%m/%d/%y")
    y = datetime.today() - x
    return y.days


# применяется при сравнении периодов
def compare(x, y):
    try:
        z = float(x) / float(y) * 100 - 100
        if z < 0:
            return f'▼ {round(z, 1)}%'
        elif z == 0:
            return '0%'
        elif z > 0:
            return f'▲ +{round(z, 1)}%'
        else:
            return '0%'
    except ZeroDivisionError:
        return ' -- '


# функция для обычного деления
def compare2_0(lower, higher):
    try:
        z = float(lower) / float(higher) * 100
        if z == 0:
            return '0'
        elif z > 0:
            return f'{round(z, 1)}'
    except ZeroDivisionError:
        return '0'
    except TypeError:
        return '0'


# для запуска двух потоков schedule
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
