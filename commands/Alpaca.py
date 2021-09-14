import main
from math import floor
from flask import request, Response
from db_connect import alpaca_get
from datetime import datetime
from main import app, client
from commands import timestamp
from dotenv import load_dotenv
import os

load_dotenv()


@app.route('/alpaca-day', methods=['POST'])
def alpaca_day():
    data = request.form
    channel_id = data.get('channel_id')

    new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams = alpaca_metrics(higher_date=1, lower_date=0, start='1DaysAgo', end='today')

    new_users_compare, conversion_to_install_compare, bounce_rate_compare, k_factor_rate_compare, \
        new_teams_compare, aha_moment_rate_compare, active_teams_compare \
        = compare_metrics(higher_date=1, lower_date=0, start='1DaysAgo', end='today', higher_date_prev=2,
                          lower_date_prev=1, start_prev='2DaysAgo', end_prev='1DaysAgo')

    client.chat_postMessage(channel=channel_id,
                            text='*Alpaca – Day*\n'
                                 f"Period: {timestamp.timestamps(1).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({new_users_compare})\n'
                                 f'Conversion to Install (CR1): {conversion_to_install}%'
                                 f' ({conversion_to_install_compare})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Teams: {new_teams} ({new_teams_compare})\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({aha_moment_rate_compare})\n'
                                 '\n'
                                 f'Active Teams: {active_teams} ({active_teams_compare})')
    return Response(), 200


@app.route('/alpaca-week', methods=['POST'])
def alpaca_week():
    data = request.form
    channel_id = data.get('channel_id')

    new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams = alpaca_metrics(higher_date=7, lower_date=0, start='7DaysAgo', end='today')

    new_users_compare, conversion_to_install_compare, bounce_rate_compare, k_factor_rate_compare, \
        new_teams_compare, aha_moment_rate_compare, active_teams_compare \
        = compare_metrics(higher_date=7, lower_date=0, start='7DaysAgo', end='today', higher_date_prev=14,
                          lower_date_prev=7, start_prev='14DaysAgo', end_prev='7DaysAgo')

    client.chat_postMessage(channel=channel_id,
                            text='*Alpaca – Week*\n'
                                 f"Period: {timestamp.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({new_users_compare})\n'
                                 f'Conversion to Install (CR1): {conversion_to_install}%'
                                 f' ({conversion_to_install_compare})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Teams: {new_teams} ({new_teams_compare})\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({aha_moment_rate_compare})\n'
                                 '\n'
                                 f'Active Teams: {active_teams} ({active_teams_compare})')
    return Response(), 200


@app.route('/alpaca-month', methods=['POST'])
def alpaca_month():
    data = request.form
    channel_id = data.get('channel_id')

    new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams = alpaca_metrics(higher_date=30, lower_date=0, start='30DaysAgo', end='today')

    new_users_compare, conversion_to_install_compare, bounce_rate_compare, k_factor_rate_compare, \
        new_teams_compare, aha_moment_rate_compare, active_teams_compare \
        = compare_metrics(higher_date=30, lower_date=0, start='30DaysAgo', end='today', higher_date_prev=60,
                          lower_date_prev=30, start_prev='60DaysAgo', end_prev='30DaysAgo')

    client.chat_postMessage(channel=channel_id,
                            text='*Alpaca – Month*\n'
                                 f"Period: {timestamp.timestamps(30).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({new_users_compare})\n'
                                 f'Conversion to Install (CR1): {conversion_to_install}%'
                                 f' ({conversion_to_install_compare})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Teams: {new_teams} ({new_teams_compare})\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({aha_moment_rate_compare})\n'
                                 '\n'
                                 f'Active Teams: {active_teams} ({active_teams_compare})')
    return Response(), 200


@app.route('/alpaca-all', methods=['POST'])
def alpaca_all():
    data = request.form
    channel_id = data.get('channel_id')

    new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams = alpaca_metrics(higher_date=timestamp.start_day(), lower_date=0,
                                      start=f'{timestamp.start_day()}DaysAgo', end='today')

    client.chat_postMessage(channel=channel_id,
                            text='*Alpaca – All*\n'
                                 f"Period: All time\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing}\n'
                                 f'Conversion to Install (CR1): {conversion_to_install}%\n'
                                 f'Bounce Rate: {floor(bounce_rate)}%\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}%\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Teams: {new_teams}\n'
                                 f'Aha-moment Rate: {aha_moment_rate}%\n'
                                 '\n'
                                 f'Active Teams: {active_teams}')
    return Response(), 200


def alpaca_ga_metrics(startDate, metrics, endDate, dimensions=None):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_ALPACA'),
                                       dateRanges=[{'startDate': startDate, 'endDate': endDate}],
                                       dimensions=dimensions,
                                       metrics=[{'expression': metrics}])])).execute()
    for report in response.get('reports', []):
        columnheader = report.get('columnHeader', {})
        metricheaders = columnheader.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            daterangevalues = row.get('metrics', [])
            for i, values in enumerate(daterangevalues):
                for metricheaders, value in zip(metricheaders, values.get('values')):
                    return value


def alpaca_metrics(higher_date, lower_date, start, end):
    new_users_landing = alpaca_ga_metrics(startDate=start, metrics="ga:newUsers", endDate=end)

    conversion_to_install = timestamp.compare2_0(new_teams_db(higher_date, lower_date), new_users_landing)

    bounce_rate = float(alpaca_ga_metrics(startDate=start, metrics="ga:bounceRate", endDate=end))

    no_ref = alpaca_ga_metrics(startDate=start, endDate=end, metrics="ga:newUsers",
                               dimensions=[{'name': 'ga:referralPath'}])

    k_factor_rate = timestamp.compare2_0(no_ref, new_users_landing)

    new_teams = new_teams_db(higher_date, lower_date)

    aha_moment_rate = timestamp.compare2_0(aha_moment(higher_date, lower_date), new_teams_db(higher_date, lower_date))

    active_teams = active_teams_db(higher_date, lower_date)

    return new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams


def compare_metrics(higher_date, lower_date, start, end, higher_date_prev, lower_date_prev, start_prev, end_prev):

    new_users_landing, conversion_to_install, bounce_rate, k_factor_rate, new_teams, aha_moment_rate, \
        active_teams = alpaca_metrics(higher_date=higher_date, lower_date=lower_date, start=start, end=end)

    new_users_landing_prev, conversion_to_install_prev, bounce_rate_prev, k_factor_rate_prev, new_teams_prev, \
        aha_moment_rate_prev, active_teams_prev \
        = alpaca_metrics(higher_date=higher_date_prev, lower_date=lower_date_prev, start=start_prev, end=end_prev)

    new_users_compare = timestamp.compare(new_users_landing, new_users_landing_prev)

    conversion_to_install_compare = timestamp.compare(conversion_to_install, conversion_to_install_prev)

    bounce_rate_compare = timestamp.compare(bounce_rate, bounce_rate_prev)

    k_factor_rate_compare = timestamp.compare(k_factor_rate, k_factor_rate_prev)

    new_teams_compare = timestamp.compare(new_teams, new_teams_prev)

    aha_moment_rate_compare = timestamp.compare(aha_moment_rate, aha_moment_rate_prev)

    active_teams_compare = timestamp.compare(active_teams, active_teams_prev)

    return new_users_compare, conversion_to_install_compare, bounce_rate_compare, k_factor_rate_compare, \
        new_teams_compare, aha_moment_rate_compare, active_teams_compare


def new_teams_db(higher_date, lower_date=0):
    count = alpaca_get(query="select count(team_id) from teams where created_at between "
                             f"now()-interval '{higher_date} days' and now()-interval '{lower_date} days'")
    return count.iloc[0]["count"]


def aha_moment(higher_date, lower_date=0):
    count = alpaca_get(query="with ids as(select team_id from actions where created_at between "
                             f"now()-interval '{higher_date} days' and now() - interval '{lower_date} days' "
                             "group by 1 having count(value) > 2) select count(1) from ids")
    return count.iloc[0]["count"]


def active_teams_db(higher_date, lower_date=0):
    count = alpaca_get(query="select count(distinct team_id) from actions where created_at between "
                             f"now()-interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]
