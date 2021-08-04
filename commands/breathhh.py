import os
from flask import request, Response
from db_connect import get_users, get_actions
from datetime import datetime
from main import app, client
from commands import timestamp
import schedule


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
                                 '/breathhh - показатели за всё время \n'
                                 '/breathhh-day - показатели за день \n'
                                 '/breathhh-week - показатели за неделю \n'
                                 '/breathhh-month - показатели за месяц \n')
    return Response(), 200


@app.route('/breathhh-day', methods=['POST'])
def breathhh_day():
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')

    current_dau = actions.loc[actions['updated_at'] > timestamp.yesterday]['user_id'].nunique()
    for_compare_dau = actions.loc[(actions['created_at'] > timestamp.two_days)
                                  & (actions['created_at'] < timestamp.yesterday)]['user_id'].nunique()

    extensions = actions.loc[(actions['created_at'] >= timestamp.yesterday) &
                             (actions['url'] == 'Breathhh extension page launch')]
    ext_by_day = extensions.groupby('user_id')['url'].count().describe()['50%']
    for_compare_ext = actions.loc[(actions['created_at'] > timestamp.two_days) &
                                  (actions['created_at'] < timestamp.yesterday) &
                                  (actions['url'] == 'Breathhh extension page launch')] \
        .groupby('user_id')['url'].count().describe()['50%']

    utp_day = (actions.loc[actions['created_at'] > timestamp.yesterday]['url'].value_counts().reset_index()['index']
               .iloc[:5].to_string(index=False).replace('\n', ','))
    utp_day = " ".join(utp_day.split())

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Day ({(timestamp.yesterday.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 '\n Metric: Daily Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_dau} ({timestamp.compare(current_dau, for_compare_dau)} day) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_day} ({timestamp.compare(ext_by_day, for_compare_ext)} day)\n'
                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 популярных сайтов'
                                 f'\n Urls: \n {utp_day}')

    return Response(), 200


@app.route('/breathhh-week', methods=['POST'])
def breathhh_week():
    data = request.form
    channel_id = data.get('channel_id')
    current_wau, for_compare_wau, ext_by_week, for_compare_ext, utp_week = timestamp.weekly()
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Week ({(timestamp.week.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 f'\n Metric: Weekly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_wau} ({timestamp.compare(current_wau, for_compare_wau)} week) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_week} ({timestamp.compare(ext_by_week, for_compare_ext)} week)\n'
                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 популярных сайтов'
                                 f'\n Urls: \n {utp_week}')

    return Response(), 200


@app.route('/breathhh-month', methods=['POST'])
def breathhh_month():
    data = request.form
    channel_id = data.get('channel_id')
    current_mau, for_compare, ext_by_month, for_compare_ext, utp_month = timestamp.monthly()
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: Month ({(timestamp.month.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 f'\n Metric: Monthly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_mau} ({timestamp.compare(current_mau, for_compare)} month) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_month} ({timestamp.compare(ext_by_month, for_compare_ext)} month)\n'
                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 популярных сайтов'
                                 f'\n Urls: \n {utp_month}')
    return Response(), 200


@app.route('/breathhh', methods=['POST'])
def breathhh():
    users = get_users()
    actions = get_actions()
    data = request.form
    channel_id = data.get('channel_id')
    total_users_reg = str(users['id'].count())

    utp = actions['url'].value_counts().reset_index()['index'].iloc[:5]. \
        to_string(index=False).replace('\n', ',')
    utp = " ".join(utp.split())

    extensions = actions.loc[actions['url'] == 'Breathhh extension page launch'].groupby('user_id')['url'].count() \
        .describe()['50%']

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*'
                                 f'\n Period: All time \n'
                                 f'\n Metric: Total users'
                                 f'\n Value: {total_users_reg}\n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 f'\n Value: {extensions} \n'
                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 посещенных сайтов'
                                 f'\n Urls: \n {utp} ')

    return Response(), 200


def weekly_report():
    current_wau, for_compare_wau, ext_by_week, for_compare_ext, utp_week = timestamp.weekly()
    client.chat_postMessage(channel=os.getenv('CHANNEL'),
                            text='*Breathhh*'
                                 f'\n Period: Week ({(timestamp.week.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 f'\n Metric: Weekly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_wau} ({timestamp.compare(current_wau, for_compare_wau)} week) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_week} ({timestamp.compare(ext_by_week, for_compare_ext)} week)\n'
                                 '\n Metric: Urls Top-5'
                                 '\n Description: Топ 5 популярных сайтов'
                                 f'\n Urls: \n {utp_week} ')


def monthly_report():
    if datetime.today().day == 1:
        current_mau, for_compare, ext_by_month, for_compare_ext, utp_month = timestamp.monthly()
        client.chat_postMessage(channel=os.getenv('CHANNEL'),
                                text='*Breathhh*'
                                     f'\n Period: Month ({(timestamp.month.strftime("%d " + "%B"))}'
                                     f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                     f'\n Metric: Monthly Active Users'
                                     '\n Description: Активные пользователи'
                                     f'\n Value: {current_mau} ({timestamp.compare(current_mau, for_compare)} month) \n'
                                     '\n Metric: Daily Breath Rate'
                                     '\n Description: Среднее количество показов тренажера дыхания для каждого '
                                     'пользователя '
                                     ' за текущий период'
                                     f'\n Value: {ext_by_month} ({timestamp.compare(ext_by_month, for_compare_ext)} '
                                     'month)\n '
                                     '\n Metric: Urls Top-5'
                                     '\n Description: Топ 5 популярных сайтов'
                                     f'\n Urls: \n {utp_month}')


schedule.every().sunday.at('20:59').do(weekly_report)
schedule.every().day.at('21:00').do(monthly_report)
