import os
import requests
import schedule
import main
from flask import request, Response
from db_connect import get_users, get_actions
from datetime import datetime
from main import app, client
from commands import timestamp


@app.route('/breathhh-users-total', methods=['POST'])
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
                            text="*Breathhh*"
                                 f"\n Period: Day ({(timestamp.yesterday.strftime('%d ' + '%B'))}"
                                 f" - {datetime.today().strftime('%d ' + '%B')}) \n"
                                 "\n Metric: Landing Users"
                                 "\n Description: Количество пользоватей посетивших Breathhh.app"
                                 f"\n Value: {ga_metrics('1daysAgo', 'ga:users')} \n"
                                 "\n Metric: Daily Active Users"
                                 "\n Description: Активные пользователи"
                                 f"\n Value: {current_dau} ({timestamp.compare(current_dau, for_compare_dau)}) \n"
                                 "\n Metric: Daily Breath Rate"
                                 "\n Description: Среднее количество показов тренажера дыхания для каждого пользователя"
                                 " за текущий период"
                                 f"\n Value: {ext_by_day} ({timestamp.compare(ext_by_day, for_compare_ext)})\n"
                                 "\n Metric: Urls Top-5"
                                 "\n Description: Топ 5 популярных сайтов"
                                 f"\n Urls: \n {utp_day}")

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
                                 "\n Metric: Users Sessions"
                                 "\n Description: Количество пользоватей посетивших Breathhh.app"
                                 f"\n Value: {ga_metrics('7daysAgo', 'ga:users')} \n"
                                 f'\n Metric: Weekly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_wau} ({timestamp.compare(current_wau, for_compare_wau)}) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_week} ({timestamp.compare(ext_by_week, for_compare_ext)})\n'
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
                                 "\n Metric: Landing Users"
                                 "\n Description: Количество пользоватей посетивших Breathhh.app"
                                 f"\n Value: {ga_metrics('30daysAgo', 'ga:users')} \n"
                                 f'\n Metric: Monthly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_mau} ({timestamp.compare(current_mau, for_compare)}) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_month} ({timestamp.compare(ext_by_month, for_compare_ext)})\n'
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
                                 "\n Metric: Landing Users"
                                 "\n Description: Количество пользоватей посетивших Breathhh.app"
                                 f"\n Value: {ga_metrics('2021-01-01', 'ga:users')} \n"
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
                                 "\n Metric: Landing Users"
                                 "\n Description: Количество пользоватей посетивших Breathhh.app"
                                 f"\n Value: {ga_metrics('7daysAgo', 'ga:users')} \n"
                                 f'\n Metric: Weekly Active Users'
                                 '\n Description: Активные пользователи'
                                 f'\n Value: {current_wau} ({timestamp.compare(current_wau, for_compare_wau)}) \n'
                                 '\n Metric: Daily Breath Rate'
                                 '\n Description: Среднее количество показов тренажера дыхания для каждого пользователя'
                                 ' за текущий период'
                                 f'\n Value: {ext_by_week} ({timestamp.compare(ext_by_week, for_compare_ext)})\n'
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
                                     "\n Metric: Landing Users"
                                     "\n Description: Количество пользоватей посетивших Breathhh.app"
                                     f"\n Value: {ga_metrics('30daysAgo', 'ga:users')} \n"
                                     f'\n Metric: Monthly Active Users'
                                     '\n Description: Активные пользователи'
                                     f'\n Value: {current_mau} ({timestamp.compare(current_mau, for_compare)}) \n'
                                     '\n Metric: Daily Breath Rate'
                                     '\n Description: Среднее количество показов тренажера дыхания для каждого '
                                     'пользователя '
                                     ' за текущий период'
                                     f'\n Value: {ext_by_month} ({timestamp.compare(ext_by_month, for_compare_ext)} '
                                     ')\n '
                                     '\n Metric: Urls Top-5'
                                     '\n Description: Топ 5 популярных сайтов'
                                     f'\n Urls: \n {utp_month}')


def ga_metrics(startDate, metrics):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=main.view_id_breathhh,
                                       dateRanges=[{'startDate': startDate, 'endDate': 'today'}],
                                       metrics=[{'expression': metrics}])])).execute()
    for report in response.get('reports', []):
        columnheader = report.get('columnHeader', {})
        metricheaders = columnheader.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            daterangevalues = row.get('metrics', [])
            for i, values in enumerate(daterangevalues):
                for metricheaders, value in zip(metricheaders, values.get('values')):
                    return value


def bmc():
    auth = {'Authorization': os.getenv('BMC_TOKEN')}
    response = requests.get('https://developers.buymeacoffee.com/api/v1/extras', headers=auth)
    print(response.json())

schedule.every().sunday.at('20:59').do(weekly_report)
schedule.every().day.at('21:00').do(monthly_report)
