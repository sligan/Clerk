import main
import os
from flask import request, Response
from db_connect import lassie_get
from datetime import datetime
from main import app, client
from commands import timestamp
from dotenv import load_dotenv

load_dotenv()


@app.route('/lassie-users-total', methods=['POST'])
def lessie_users_total():
    users = lassie_get("""SELECT count(id) FROM users""")
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f'Lessie Smoke users total - {users.iloc[0]["count"]}')
    return Response(), 200


@app.route('/lassie-day', methods=['POST'])
def lassie_day():
    data = request.form
    channel_id = data.get('channel_id')
    ret = retention()
    landing_conversion_rate = timestamp.compare2_0(count_new_users('1 days'),
                                                   lassie_ga_metrics(startDate="1daysAgo", metrics="ga:newUsers"))

    aha_rate = timestamp.compare2_0(aha('1 days'), count_active_users('1 days'))
    ret_rate = timestamp.compare2_0(ret.iloc[0]['count'], count_active_users('1 days'))

    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f"\n Period: Day ({(timestamp.timestamps(1).strftime('%d ' + '%B'))}"
                                 f" - {datetime.today().strftime('%d ' + '%B')}) \n"
                                 '\n Metric: Landing Users'
                                 '\n Description: Количество сессий по лендингу'
                                 f'\n Value: {lassie_ga_metrics(startDate="1daysAgo", metrics="ga:users")} \n'
                                 '\n Metric: Landing Conversion Rate'
                                 '\n Description: Конверсия с лендинга в установку '
                                 f'\n Value: {landing_conversion_rate} \n'
                                 '\n Metric: Aha-moment rate'
                                 '\n Description: % новых пользователей нажавших "i smoked" как минимум 5 раз'
                                 f'\n Value: {aha_rate} \n'
                                 '\n Metric: Active users'
                                 '\n Description: Количество активных пользователей'
                                 f'\n Value: {count_active_users("1 days")} \n'
                                 '\n Metric: 3-day retention Rate'
                                 '\n Description: '
                                 f'\n Value: {ret_rate}')

    return Response(), 200


@app.route('/lassie-week', methods=['POST'])
def lassie_week():
    data = request.form
    channel_id = data.get('channel_id')
    # ret = retention()
    landing_conversion_rate = timestamp.compare2_0(count_new_users('7 days'),
                                                   lassie_ga_metrics(startDate="7daysAgo", metrics="ga:newUsers"))

    aha_rate = timestamp.compare2_0(aha('7 days'), count_active_users('7 days'))
    # ret_rate = timestamp.compare2_0(ret.iloc[0]['count'], count_active_users('7 days'))

    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f'\n Period: Week ({(timestamp.timestamps(7).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 '\n Metric: Landing Users'
                                 '\n Description: Количество сессий по лендингу'
                                 f'\n Value: {lassie_ga_metrics(startDate="7daysAgo", metrics="ga:users")} \n'
                                 '\n Metric: Landing Conversion Rate'
                                 '\n Description: Конверсия с лендинга в установку '
                                 f'\n Value: {landing_conversion_rate} \n'
                                 '\n Metric: Aha-moment rate'
                                 '\n Description: % новых пользователей нажавших "i smoked" как минимум 5 раз'
                                 f'\n Value: {aha_rate} \n'
                                 '\n Metric: Active users'
                                 '\n Description: Количество активных пользователей'
                                 f'\n Value: {count_active_users("7 days")} \n')
    # '\n Metric: 3-day retention Rate'
    # '\n Description: '
    # f'\n Value: {ret_rate}')
    return Response(), 200


@app.route('/lassie-month', methods=['POST'])
def lassie_month():
    data = request.form
    channel_id = data.get('channel_id')
    # ret = retention()
    landing_conversion_rate = timestamp.compare2_0(count_new_users('30 days'),
                                                   lassie_ga_metrics(startDate="30daysAgo", metrics="ga:newUsers"))

    aha_rate = timestamp.compare2_0(aha('30 days'), count_active_users('30 days'))
    # ret_rate = timestamp.compare2_0(ret.iloc[0]['count'], count_active_users('7 days'))

    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f'\n Period: Month ({(timestamp.timestamps(30).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 '\n Metric: Landing Users'
                                 '\n Description: Количество сессий по лендингу'
                                 f'\n Value: {lassie_ga_metrics(startDate="30daysAgo", metrics="ga:users")} \n'
                                 '\n Metric: Landing Conversion Rate'
                                 '\n Description: Конверсия с лендинга в установку '
                                 f'\n Value: {landing_conversion_rate} \n'
                                 '\n Metric: Aha-moment rate'
                                 '\n Description: % новых пользователей нажавших "i smoked" как минимум 5 раз'
                                 f'\n Value: {aha_rate} \n'
                                 '\n Metric: Active users'
                                 '\n Description: Количество активных пользователей'
                                 f'\n Value: {count_active_users("30 days")} \n')
    # '\n Metric: 3-day retention Rate'
    # '\n Description: '
    # f'\n Value: {ret_rate}')
    return Response(), 200


@app.route('/lassie-all', methods=['POST'])
def lassie_all():
    data = request.form
    channel_id = data.get('channel_id')
    total_users = lassie_get(query="select count(distinct(id)) from users")
    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f"\n Period: All time \n"
                                 '\n Metric: Total Users'
                                 '\n Description: Суммарное количество пользователей'
                                 f'\n Value: {total_users[0]["count"]}\n')


def lassie_ga_metrics(startDate, metrics):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_LESSIE'),
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


def count_new_users(days_count):
    count = lassie_get(query="SELECT count(distinct(id)) FROM users "
                             f"WHERE created_at > now() - interval '{days_count}'")
    return count.iloc[0]["count"]


def count_active_users(days_count):
    count = lassie_get(query="SELECT count(distinct(user_id)) FROM smoking_actions "
                             f"WHERE smoke_at > now() - interval '{days_count}'")
    return count.iloc[0]["count"]


def aha(days_count):
    count = lassie_get(query="WITH count_smoke AS (SELECT user_id FROM smoking_actions GROUP BY user_id HAVING count("
                             "smoke_at) > 5) SELECT count(distinct id) FROM users JOIN count_smoke ON "
                             f"count_smoke.user_id = users.id WHERE users.created_at > now() - interval '{days_count}'")
    return count.iloc[0]['count']


def retention():
    return lassie_get(query="WITH count_smoke AS (SELECT user_id FROM smoking_actions "
                            "WHERE smoke_at > now() - interval '1 days' GROUP BY user_id "
                            "HAVING count(smoke_at) > 3) SELECT count(distinct id) "
                            "FROM users JOIN count_smoke ON count_smoke.user_id = users.id "
                            "WHERE users.created_at between now() - interval '3 days' and now() - interval '2 days'")
