from flask import request, Response
from db_connect import get_users, get_actions
from datetime import datetime, timedelta
from main import app, client


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
    actions = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=1)]
    current_dau = actions['user_id'].nunique()
    client.chat_postMessage(channel=channel_id,
                            text='Project: Breathhh \n Metric: DAU '
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))} - '
                                 f'{datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_dau}')
    return Response(), 200


@app.route('/breathhh-wau', methods=['POST'])
def wau():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    actions = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=7)]
    current_wau = actions['user_id'].nunique()
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: WAU'
                                 f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))} - '
                                 f'{datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_wau}')
    return Response(), 200


@app.route('/breathhh-mau', methods=['POST'])
def mau():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    actions = actions.loc[actions['updated_at'] > datetime.today() - timedelta(days=30)]
    current_mau = actions['user_id'].nunique()
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: MAU'
                                 f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))} - '
                                 f'{datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {current_mau}')
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
    ext_by_day = extensions.groupby(extensions['created_at'].dt.day).count()
    ext_by_day = ext_by_day.describe()['url']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                                 f'\n Period: Day ({((datetime.today() - timedelta(days=1)).strftime("%d " + "%B"))} - '
                                 f'{datetime.today().strftime("%d " + "%B")})'
                                 f'\n Value: {ext_by_day}')
    return Response(), 200


@app.route('/breathhh-dbr-week', methods=['POST'])
def dbr_week():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_week = extensions.groupby(extensions['created_at'].dt.isocalendar().week).count()
    ext_by_week = ext_by_week.describe()['url']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                            f'\n Period: Week ({((datetime.today() - timedelta(days=7)).strftime("%d " + "%B"))} - '
                            f'{datetime.today().strftime("%d " + "%B")})'
                            f'\n Value: {ext_by_week}')
    return Response(), 200


@app.route('/breathhh-dbr-month', methods=['POST'])
def dbr_month():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch']
    ext_by_month = extensions.groupby(extensions['created_at'].dt.month).count()
    ext_by_month = ext_by_month.describe()['id']['50%']
    client.chat_postMessage(channel=channel_id,
                            text=f'Project: Breathhh \n Metric: DBR'
                            f'\n Period: Month ({((datetime.today() - timedelta(days=30)).strftime("%d " + "%B"))} - '
                            f'{datetime.today().strftime("%d " + "%B")})'
                            f'\n Value: {ext_by_month}')
    return Response(), 200
