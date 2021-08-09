import main
from flask import request, Response
from db_connect import lassie_get
from datetime import datetime
from main import app, client
from commands import timestamp


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
    count_new_users_id = lassie_get(query="SELECT count(distinct(id)) FROM users WHERE created_at > now() - interval "
                                          "'24 hours'")
    count_active_users = lassie_get(query="SELECT count(distinct(user_id)) FROM smoking_actions WHERE smoke_at > "
                                          "now() - interval '24 hours'")
    aha = lassie_get(query="SELECT count(distinct(smoke_at)), count(distinct(users.id)) as id_count FROM users join "
                           "smoking_actions on users.id = smoking_actions.user_id WHERE users.created_at > now() - "
                           "interval '24 hours' HAVING count(distinct(smoke_at)) >= 5")
    ret = lassie_get(query="SELECT count(sa.smoke_at),count(distinct(users.id)) FROM users join smoking_actions sa "
                           "on users.id = sa.user_id WHERE users.created_at between CURRENT_DATE - interval'3 days' "
                           "and current_date - interval'2 days' GROUP BY users.id HAVING count(sa.smoke_at) > 3")

    landing_conversion_rate = timestamp.compare2_0(lessie_ga_metrics(startDate="1daysAgo", metrics="ga:newUsers"),
                                                   count_new_users_id.iloc[0]["count"])
    aha_rate = timestamp.compare2_0(aha.iloc[0]['id_count'], count_active_users.iloc[0]["count"])
    # ваще не работает пока aha null

    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f"\n Period: Day ({(timestamp.yesterday.strftime('%d ' + '%B'))}"
                                 f" - {datetime.today().strftime('%d ' + '%B')}) \n"
                                 '\n Metric: Landing Users'
                                 '\n Description: Количество сессий по лендингу'
                                 f'\n Value: {lessie_ga_metrics(startDate="1daysAgo", metrics="ga:users")} \n'
                                 '\n Metric: Landing Conversion Rate'
                                 '\n Description: Конверсия с лендинга в установку '
                                 f'\n Value: {landing_conversion_rate} \n'
                                 '\n Metric: Aha-moment rate'
                                 '\n Description: % пользователей нажавших "i smoked" как минимум 5 раз'
                                 f'\n Value: тут будет aha_rate \n'
                                 '\n Metric: Active users'
                                 '\n Description: Количество активных пользователей'
                                 f'\n Value: {count_active_users.loc[0]["count"]} \n'
                                 '\n Metric: 3-day retention Rate'
                                 '\n Description: '
                                 f'\n Value:{ret}')

    return Response(), 200


@app.route('/lassie-week', methods=['POST'])
def lassie_week():
    pass


@app.route('/lassie-month', methods=['POST'])
def lassie_month():
    pass


@app.route('/lassie', methods=['POST'])
def lassie():
    data = request.form
    channel_id = data.get('channel_id')
    total_users = lassie_get(query="select count(distinct(id)) from users")
    client.chat_postMessage(channel=channel_id,
                            text="*Lassie Smoke*"
                                 f"\n Period: All time \n"
                            '\n Metric: Total Users'
                            '\n Description: Суммарное количество пользователей'
                            f'\n Value: {total_users[0]["count"]}\n')


def lessie_ga_metrics(startDate, metrics):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=main.view_id_lassie,
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
