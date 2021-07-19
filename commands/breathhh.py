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


@app.route('/breathhh-dau', methods=['POST'])
def dau():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    current_dau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=1)]['user_id'].nunique()
    for_compare = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=2))
                               & (actions['created_at'] < datetime.today() - timedelta(days=1))]['user_id'].nunique())
    client.chat_postMessage(channel=channel_id,
                            text='Project: Breathhh \n Metric: DAU '
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_dau} ({compare(current_dau, for_compare)} day )')
    return Response(), 200


@app.route('/breathhh-wau', methods=['POST'])
def wau():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    current_wau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=7)]['user_id'].nunique()
    for_compare = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=14))
                               & (actions['created_at'] < datetime.today() - timedelta(days=7))]['user_id'].nunique())
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: WAU'
                                 f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_wau} ({compare(current_wau, for_compare)} week )')
    return Response(), 200


@app.route('/breathhh-mau', methods=['POST'])
def mau():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    current_mau = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=30)]['user_id'].nunique()
    for_compare = (actions.loc[(actions['created_at'] > datetime.today() - timedelta(days=60))
                               & (actions['created_at'] < datetime.today() - timedelta(days=30))]['user_id'].nunique())
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: MAU'
                                 f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_mau} ({compare(current_mau, for_compare)} month )')
    return Response(), 200


@app.route('/breathhh-3-day-retention', methods=['POST'])
def day_3_retention():
    pass


@app.route('/breathhh-dbr-day', methods=['POST'])
def dbr_day():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_day = extensions.groupby(extensions['created_at'].dt.day).count().describe()['url']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {ext_by_day}')
    return Response(), 200


@app.route('/breathhh-dbr-week', methods=['POST'])
def dbr_week():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_week = extensions.groupby(extensions['created_at'].dt.isocalendar().week).count().describe()['url']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                                 f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {ext_by_week}')
    return Response(), 200


@app.route('/breathhh-dbr-month', methods=['POST'])
def dbr_month():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_month = extensions.groupby(extensions['created_at'].dt.month).count().describe()['url']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                                 f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {ext_by_month}')
    return Response(), 200


@app.route('/breathhh-utp5-day', methods=['POST'])
def utp5_day():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    utp_day = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=1)]['url']
               .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
               .to_string(index=False).replace('\n', ','))
    utp_day = " ".join(utp_day.split())
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: UTP5'
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Top 5 URLs: \n {utp_day}')
    return Response(), 200


@app.route('/breathhh-utp5-week', methods=['POST'])
def utp5_week():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    utp_week = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=7)]['url']
                .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
                .to_string(index=False).replace('\n', ','))
    utp_week = " ".join(utp_week.split())
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: UTP5'
                                 f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Top 5 URLs: \n {utp_week}')
    return Response(), 200


@app.route('/breathhh-utp5-month', methods=['POST'])
def utp5_month():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    utp_month = (actions.loc[actions['created_at'] > datetime.today() - timedelta(days=30)]['url']
                 .apply(lambda x: x[8::]).value_counts().reset_index()['index'].iloc[:5]
                 .to_string(index=False).replace('\n', ','))
    utp_month = " ".join(utp_month.split())
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: UTP5'
                                 f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")})'
                                 f'\n Top 5 URLs: \n {utp_month}')
    return Response(), 200
