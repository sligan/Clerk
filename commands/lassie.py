import os
import schedule
import main
from flask import request, Response
from db_connect import lessie_get_users
from datetime import datetime, timedelta
from main import app, client
from commands import timestamp
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


@app.route('/lassie-users-total', methods=['POST'])
def lessie_users_total():
    users = lessie_get_users("""SELECT count(id) FROM users""")
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f'Lessie Smoke users total - {users.iloc[0]["count"]}')
    return Response(), 200


@app.route('/lassie-day', methods=['POST'])
def lassie_day():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text=
                            f' количество сессий на сайте лесси {lessie_ga_metrics(startDate="1daysAgo")}')
    return Response(), 200


@app.route('/lassie-week', methods=['POST'])
def lassie_week():
    pass


@app.route('/lassie-month', methods=['POST'])
def lassie_month():
    pass


def lessie_ga_metrics(startDate, metrics='ga:sessions'):
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
