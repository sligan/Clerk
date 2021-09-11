# import main
# from math import floor
# from flask import request, Response
# from db_connect import alpaca_get
# from datetime import datetime
# from main import app, client
# from commands import timestamp
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
#
# @app.route('/alpaca-day', methods=['POST'])
# def alpaca_day():
#     data = request.form
#     channel_id = data.get('channel_id')
#
#     client.chat_postMessage(channel=channel_id,
#                             text='*Alpaca – Day*\n'
#                                  f"Period: {timestamp.timestamps(1).strftime('%d ' + '%B')} "
#                                  f"- {datetime.today().strftime('%d ' + '%B')}\n"
#                                  '\n'
#                                  '*Marketing* 📢\n'
#                                  f'User Acquisition (UA): {} ({})\n'
#                                  f'Conversion to Install (CR1): {}% ({})\n'
#                                  f'Bounce Rate: {floor()}% ({})\n'
#                                  'K-factor Rate (Viral): {this} {previous}\n'
#                                  '\n'
#                                  '*Product* 🍏\n'
#                                  f'New Teams: {} ({})\n'
#                                  f'Aha-moment Rate: {}% ({})\n'
#                                  '\n'
#                                  f'Active Users: {} ({})')
#     return Response(), 200
#
#
# @app.route('/alpaca-week', methods=['POST'])
# def alpaca_week():
#     data = request.form
#     channel_id = data.get('channel_id')
#
#     client.chat_postMessage(channel=channel_id,
#                             text='*Alpaca – Week*\n'
#                                  f"Period: {timestamp.timestamps(7).strftime('%d ' + '%B')} "
#                                  f"- {datetime.today().strftime('%d ' + '%B')}\n"
#                                  '\n'
#                                  '*Marketing* 📢\n'
#                                  f'User Acquisition (UA): {} ({})\n'
#                                  f'Conversion to Install (CR1): {}% ({})\n'
#                                  f'Bounce Rate: {floor()}% ({})\n'
#                                  'K-factor Rate (Viral): {this} {previous}\n'
#                                  '\n'
#                                  '*Product* 🍏\n'
#                                  f'New Teams: {} ({})\n'
#                                  f'Aha-moment Rate: {}% ({})\n'
#                                  '\n'
#                                  f'Active Users: {} ({})')
#     return Response(), 200
#
#
# @app.route('/alpaca-month', methods=['POST'])
# def alpaca_month():
#     data = request.form
#     channel_id = data.get('channel_id')
#
#     client.chat_postMessage(channel=channel_id,
#                             text='*Alpaca – Month*\n'
#                                  f"Period: {timestamp.timestamps(30).strftime('%d ' + '%B')} "
#                                  f"- {datetime.today().strftime('%d ' + '%B')}\n"
#                                  '\n'
#                                  '*Marketing* 📢\n'
#                                  f'User Acquisition (UA): {} ({})\n'
#                                  f'Conversion to Install (CR1): {}% ({})\n'
#                                  f'Bounce Rate: {floor()}% ({})\n'
#                                  'K-factor Rate (Viral): {this} {previous}\n'
#                                  '\n'
#                                  '*Product* 🍏\n'
#                                  f'New Teams: {} ({})\n'
#                                  f'Aha-moment Rate: {}% ({})\n'
#                                  '\n'
#                                  f'Active Users: {} ({})')
#     return Response(), 200
#
#
# @app.route('/alpaca-all', methods=['POST'])
# def alpaca_all():
#     data = request.form
#     channel_id = data.get('channel_id')
#
#     client.chat_postMessage(channel=channel_id,
#                             text='*Alpaca – Day*\n'
#                                  f"Period: All time\n"
#                                  '\n'
#                                  '*Marketing* 📢\n'
#                                  f'User Acquisition (UA): {} ({})\n'
#                                  f'Conversion to Install (CR1): {}% ({})\n'
#                                  f'Bounce Rate: {floor()}% ({})\n'
#                                  'K-factor Rate (Viral): {this} {previous}\n'
#                                  '\n'
#                                  '*Product* 🍏\n'
#                                  f'New Teams: {} ({})\n'
#                                  f'Aha-moment Rate: {}% ({})\n'
#                                  '\n'
#                                  f'Active Users: {} ({})')
#     return Response(), 200
#
#
# def alpaca_ga_metrics(startDate, metrics, endDate):
#     response = main.analytics.reports().batchGet(
#         body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_ALPACA'),
#                                        dateRanges=[{'startDate': startDate, 'endDate': endDate}],
#                                        metrics=[{'expression': metrics}])])).execute()
#     for report in response.get('reports', []):
#         columnheader = report.get('columnHeader', {})
#         metricheaders = columnheader.get('metricHeader', {}).get('metricHeaderEntries', [])
#         for row in report.get('data', {}).get('rows', []):
#             daterangevalues = row.get('metrics', [])
#             for i, values in enumerate(daterangevalues):
#                 for metricheaders, value in zip(metricheaders, values.get('values')):
#                     return value
#
#
# def alpaca_metrics():
#     new_users_db = ''
#     new_users_landing = alpaca_ga_metrics(startDate='', metrics="ga:newUsers", endDate='')
#     conversion_to_install = new_users_db / new_users_landing
#     bounce_rate = alpaca_ga_metrics(startDate='', metrics="ga:bounceRate", endDate='')
#     k_factor_rate = ''
#     new_teams = new_users_db
#     aha_moment_rate = ''
#     active_teams = ''
#
