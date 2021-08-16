import main
from flask import request, Response
from db_connect import alpaca_get
from datetime import datetime
from main import app, client
from commands import timestamp


@app.route('/Alpaca-day', methods=['POST'])
def Alpaca_day():
    landing_users = alpaca_ga_metrics(startDate="1daysAgo", metrics="ga:newUsers")
    # landing_conversion_rate =
    # active_teams =
    # total_users =
    # aha =
    # uninstall_rate =
    pass


@app.route('/Alpaca-week', methods=['POST'])
def Alpaca_week():
    pass


@app.route('/Alpaca-month', methods=['POST'])
def Alpaca_month():
    pass


@app.route('/Alpaca', methods=['POST'])
def Alpaca():
    pass


def alpaca_ga_metrics(startDate, metrics):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=main.view_id_alpaca,
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
