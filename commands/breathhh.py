from flask import request, Response
from db_connect import get_users, get_actions
from datetime import datetime, timedelta
from main import app, client
from math import floor


def compare(x, y):
    try:
        z = x / y * 100 - 100
        if z < 0:
            return f'▼ {floor(z)}% at previous'
        else:
            return f'▲ +{floor(z)}% at previous'
    except ZeroDivisionError:
        return 'Еще не было пользователей за прошлый'


@app.route('/users-total', methods=['POST'])
def users_total():
    users = get_users()
    data = request.form
    channel_id = data.get('channel_id')
    total_users = str(users['id'].count())
    client.chat_postMessage(channel=channel_id, text=f'Breathhh users total - {total_users}')
    return Response(), 200


@app.route('/help', methods=['POST'])
def help_clerk():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Commands*:  \n'
                                 '/breathhh-day - показатели за день \n'
                                 '/breathhh-week - показатели за неделю \n'
                                 '/breathhh-month - показатели за месяц \n'
                                 '/breathhh - показатели за всё время')
    return Response(), 200


@app.route('/breathhh-day', methods=['POST'])
def breathhh_day():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')

    current_dau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=1)]['user_id'].nunique()
    for_compare_dau = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=2))
                                   & (actions['created_at'] < datetime.today() - timedelta(days=1))][
                           'user_id'].nunique())

    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_day = extensions.groupby(extensions['created_at'].dt.day).count().describe()['url']['50%']

    utp_day = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=1)]['url']
               .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
               .to_string(index=False).replace('\n', ','))
    utp_day = " ".join(utp_day.split())

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'

                                 '\n Metric: Daily Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_dau} ({compare(current_dau, for_compare_dau)} day ) \n'

                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Медиана открытия вкладки с дыханием'
                                 f'\n Value: {ext_by_day} \n'

                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 посещенных сайтов'
                                 f'\n Urls: \n {utp_day}')

    return Response(), 200


@app.route('/breathhh-week', methods=['POST'])
def breathhh_week():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    current_wau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=7)]['user_id'].nunique()
    for_compare_wau = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=14))
                                   & (actions['created_at'] < datetime.today() - timedelta(days=7))][
                           'user_id'].nunique())

    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_week = extensions.groupby(extensions['created_at'].dt.isocalendar().week).count().describe()['url']['50%']

    utp_week = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=7)]['url']
                .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
                .to_string(index=False).replace('\n', ','))
    utp_week = " ".join(utp_week.split())

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'

                                 f'\n Metric: Weekly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_wau} ({compare(current_wau, for_compare_wau)} week ) \n'

                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Медиана открытия вкладки с дыханием'
                                 f'\n Value: {ext_by_week} \n'

                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 посещенных сайтов'
                                 f'\n Urls: \n {utp_week}')

    return Response(), 200


@app.route('/breathhh-month', methods=['POST'])
def breathhh_month():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')

    current_mau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=30)]['user_id'].nunique()
    for_compare = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=60))
                               & (actions['created_at'] < datetime.today() - timedelta(days=30))]['user_id'].nunique())

    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_month = extensions.groupby(extensions['created_at'].dt.month).count().describe()['url']['50%']

    utp_month = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=30)]['url']
                 .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
                 .to_string(index=False).replace('\n', ','))
    utp_month = " ".join(utp_month.split())

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'

                                 f'\n Metric: Monthly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_mau} ({compare(current_mau, for_compare)} month ) \n'

                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Медиана открытия вкладки с дыханием'
                                 f'\n Value: {ext_by_month} \n'

                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 посещенных сайтов'
                                 f'\n Urls: \n {utp_month}')
    return Response(), 200


@app.route('/breathhh', methods=['POST'])
def breathhh():
    users = get_users()
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    total_users_reg = str(users['id'].count())

    utp = actions['url'].apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5].to_string(index=False). \
        replace('\n', ',')
    utp = " ".join(utp.split())

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: All time \n'

                                 f'\n Metric: Total users'
                                 f'\n Value: {total_users_reg}\n'

                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 посещенных сайтов'
                                 f'\n Urls: \n {utp}')

    return Response(), 200
