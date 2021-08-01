from datetime import datetime, timedelta
import commands.breathhh
from db_connect import get_actions
import schedule
import threading
import time
from math import floor

now = datetime.today()
yesterday = datetime.today() - timedelta(days=1)
two_days = datetime.today() - timedelta(days=2)
week = datetime.today() - timedelta(days=7)
two_week = datetime.today() - timedelta(days=14)
month = datetime.today() - timedelta(days=30)
two_month = datetime.today() - timedelta(days=60)


def weekly():
    actions = get_actions()
    current_wau = actions.loc[actions['updated_at'] > week]['user_id'].nunique()
    for_compare_wau = actions.loc[(actions['created_at'] > two_week)
                                  & (actions['created_at'] < week)]['user_id'].nunique()

    extensions = actions.loc[(actions['created_at'] >= week) &
                             (actions['url'] == 'Breathhh extension page launch')]
    ext_by_week = extensions.groupby('user_id')['url'].count().describe()['50%']
    for_compare_ext = actions.loc[(actions['created_at'] > two_week) &
                                  (actions['created_at'] < week) &
                                  (actions['url'] == 'Breathhh extension page launch')] \
        .groupby('user_id')['url'].count().describe()['50%']

    utp_week = (actions.loc[actions['created_at'] > week]['url'].value_counts().reset_index()['index']
                .iloc[:5].to_string(index=False).replace('\n', ','))
    utp_week = " ".join(utp_week.split())
    return current_wau, for_compare_wau, ext_by_week, for_compare_ext, utp_week


def compare(x, y):
    try:
        z = x / y * 100 - 100
        if z < 0:
            return f'▼ {floor(z)}% at previous'
        elif z == 0:
            return '0% change at previous'
        elif z > 0:
            return f'▲ +{floor(z)}% at previous'
        else:
            return 'error'
    except ZeroDivisionError:
        return 'Еще не было пользователей за прошлый'


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

