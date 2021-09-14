import main
import os
from math import floor
from flask import request, Response
from db_connect import lassie_get
from datetime import datetime
from main import app, client
from commands import timestamp
from dotenv import load_dotenv

load_dotenv()


@app.route('/lassie-day', methods=['POST'])
def new_lassie_day():
    data = request.form
    channel_id = data.get('channel_id')

    new_users, compare_nu, new_users_landing, compare_nul, bounce_rate, compare_br, k_factor_rate, \
        compare_k_factor, conversion_to_user, compare_cto, aha_moment_rate, compare_amr, onboarding_rate, \
        compare_or, average_interval_increases_rate, compare_ir, compare_cau, active_users =\
        lassie_metrics(start='2DaysAgo', end='1DaysAgo', lower_date=1, higher_date=2)

    client.chat_postMessage(channel=channel_id,
                            text='*Lassie Smoke – Day*\n'
                                 f"Period: {timestamp.timestamps(1).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({compare_nul})\n'
                                 f'Conversion to User (CR1): {conversion_to_user}% ({compare_cto})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({compare_br})\n'
                                 'K-factor Rate (Viral): {this} {previous}\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users} ({compare_nu})\n'
                                 f'Onboarding Rate: {onboarding_rate}% ({compare_or})\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({compare_amr})\n'
                                 f'Average Interval Increases Rate: {average_interval_increases_rate}% ({compare_ir})\n'
                                 '\n'
                                 f'Active Users: {active_users} ({compare_cau})')
    return Response(), 200


@app.route('/lassie-week', methods=['POST'])
def new_lassie_week():
    data = request.form
    channel_id = data.get('channel_id')

    new_users, compare_nu, new_users_landing, compare_nul, bounce_rate, compare_br, k_factor_rate, \
        compare_k_factor, conversion_to_user, compare_cto, aha_moment_rate, compare_amr, onboarding_rate, \
        compare_or, average_interval_increases_rate, compare_ir, compare_cau, active_users = \
        lassie_metrics(start='14DaysAgo', end='7DaysAgo', lower_date=7, higher_date=14)

    client.chat_postMessage(channel=channel_id,
                            text='*Lassie Smoke – Week*\n'
                                 f"Period: {timestamp.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({compare_nul})\n'
                                 f'Conversion to User (CR1): {conversion_to_user}% ({compare_cto})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({compare_br})\n'
                                 'K-factor Rate (Viral): {this} {previous}\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users} ({compare_nu})\n'
                                 f'Onboarding Rate: {onboarding_rate}% {compare_or}\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({compare_amr})\n'
                                 f'Average Interval Increases Rate: {average_interval_increases_rate}% ({compare_ir})\n'
                                 '\n'
                                 f'Active Users: {active_users} ({compare_cau})')
    return Response(), 200


@app.route('/lassie-month', methods=['POST'])
def lassie_month():
    data = request.form
    channel_id = data.get('channel_id')

    new_users, compare_nu, new_users_landing, compare_nul, bounce_rate, compare_br, k_factor_rate, \
        compare_k_factor, conversion_to_user, compare_cto, aha_moment_rate, compare_amr, onboarding_rate, \
        compare_or, average_interval_increases_rate, compare_ir, compare_cau, active_users = \
        lassie_metrics(start='60DaysAgo', end='30DaysAgo', lower_date=30, higher_date=60)

    client.chat_postMessage(channel=channel_id,
                            text='*Lassie Smoke – Month*\n'
                                 f"Period: {timestamp.timestamps(30).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing} ({compare_nul})\n'
                                 f'Conversion to User (CR1): {conversion_to_user}% ({compare_cto})\n'
                                 f'Bounce Rate: {floor(bounce_rate)}% ({compare_br})\n'
                                 'K-factor Rate (Viral): {this} {previous}\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users} ({compare_nu})\n'
                                 f'Onboarding Rate: {onboarding_rate}% {compare_or}\n'
                                 f'Aha-moment Rate: {aha_moment_rate}% ({compare_amr})\n'
                                 f'Average Interval Increases Rate: {average_interval_increases_rate}% ({compare_ir})\n'
                                 '\n'
                                 f'Active Users: {active_users} ({compare_cau})')
    return Response(), 200


@app.route('/lassie-all', methods=['POST'])
def lassie_all():
    data = request.form
    channel_id = data.get('channel_id')

    new_users = new_users_db(timestamp.start_day())
    new_users_landing = lassie_ga_metrics(startDate='2021-01-01', metrics="ga:newUsers")
    conversion_to_user = timestamp.compare2_0(new_users, new_users_landing)
    bounce_rate = float(lassie_ga_metrics(startDate='2021-01-01', metrics="ga:bounceRate"))
    onboarding_rate = timestamp.compare2_0(new_users_db_active(timestamp.start_day()), new_users)
    aha_moment_rate = timestamp.compare2_0(aha(timestamp.start_day()), new_users)
    average_interval_increases_rate = timestamp.compare2_0(interval(timestamp.start_day()), new_users)
    active_users = count_active_users(timestamp.start_day())
    k_factor_rate = timestamp.compare2_0(lassie_ga_metrics(startDate='2021-01-01', metrics="ga:newUsers",
                                                           dimensions=[{'name': 'ga:referralPath'}]), new_users_landing)

    client.chat_postMessage(channel=channel_id,
                            text='*Lassie Smoke – Month*\n'
                                 f"Period: All time\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {new_users_landing}\n'
                                 f'Conversion to User (CR1): {conversion_to_user}%\n'
                                 f'Bounce Rate: {floor(bounce_rate)}%\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users}\n'
                                 f'Onboarding Rate: {onboarding_rate}%\n'
                                 f'Aha-moment Rate: {aha_moment_rate}%\n'
                                 f'Average Interval Increases Rate: {average_interval_increases_rate}%\n'
                                 '\n'
                                 f'Active Users: {active_users}')
    return Response(), 200


def lassie_metrics(start, end, higher_date, lower_date):
    new_users = new_users_db(lower_date)
    compare_nu = timestamp.compare(new_users, new_users_db(higher_date, lower_date))

    new_users_landing = lassie_ga_metrics(startDate=end, metrics="ga:newUsers")
    compare_nul = timestamp.compare(new_users_landing,
                                    lassie_ga_metrics(startDate=start, metrics="ga:newUsers", endDate=end))

    bounce_rate = float(lassie_ga_metrics(startDate=end, metrics="ga:bounceRate"))
    compare_br = timestamp.compare(bounce_rate,
                                   lassie_ga_metrics(startDate=start, metrics='ga:bounceRate', endDate=end))

    k_factor_rate = timestamp.compare2_0(lassie_ga_metrics(startDate=end, metrics="ga:newUsers",
                                                           dimensions=[{'name': 'ga:referralPath'}]), new_users_landing)
    k_factor_rate_prev = timestamp.compare2_0(lassie_ga_metrics(startDate=start, endDate=end, metrics="ga:newUsers",
                                                                dimensions=[{'name': 'ga:referralPath'}]),
                                              lassie_ga_metrics(startDate=start, metrics="ga:newUsers", endDate=end))
    compare_k_factor = timestamp.compare(k_factor_rate, lassie_ga_metrics(startDate=start, endDate=end,
                                                                          metrics="ga:newUsers",
                                                                          dimensions=[{'name': 'ga:referralPath'}]))

    conversion_to_user = timestamp.compare2_0(new_users, new_users_landing)
    conversion_to_user_prev = timestamp.compare2_0(new_users_db(higher_date, lower_date),
                                                   lassie_ga_metrics(startDate=start, metrics='ga:newUsers',
                                                                     endDate=end))
    compare_cto = timestamp.compare(conversion_to_user, conversion_to_user_prev)

    aha_moment_rate = timestamp.compare2_0(aha(lower_date), new_users)
    aha_moment_rate_prev = timestamp.compare2_0(aha(higher_date, lower_date), new_users_db(higher_date, lower_date))
    compare_amr = timestamp.compare(aha_moment_rate, aha_moment_rate_prev)

    onboarding_rate = timestamp.compare2_0(new_users_db_active(lower_date), new_users)
    compare_or = timestamp.compare(onboarding_rate, timestamp.compare2_0(new_users_db_active(higher_date, lower_date),
                                                                         new_users_db(higher_date, lower_date)))

    average_interval_increases_rate = timestamp.compare2_0(interval(lower_date), new_users)
    average_interval_increases_rate_prev = timestamp.compare2_0(interval(higher_date, lower_date),
                                                                new_users_db(higher_date, lower_date))
    compare_ir = timestamp.compare(average_interval_increases_rate, average_interval_increases_rate_prev)

    compare_cau = timestamp.compare(count_active_users(lower_date), count_active_users(higher_date, lower_date))

    active_users = count_active_users(lower_date)

    return new_users, compare_nu, new_users_landing, compare_nul, bounce_rate, compare_br, k_factor_rate,\
        compare_k_factor, conversion_to_user, compare_cto, aha_moment_rate, compare_amr, onboarding_rate,\
        compare_or, average_interval_increases_rate, compare_ir, compare_cau, active_users


def lassie_ga_metrics(startDate, metrics, endDate='today', dimensions=None):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_LESSIE'),
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


def new_users_db(first_date, second_date=0):
    count = lassie_get(query="SELECT count(distinct(id)) FROM users WHERE created_at between "
                             f"now() - interval '{first_date} days' and now() - interval '{second_date} days'")
    return count.iloc[0]["count"]


def new_users_db_active(first_date, second_date=0):
    count = lassie_get(query="SELECT count(distinct(id)) FROM users WHERE created_at between "
                             f"now() - interval '{first_date} days' and now() - interval '{second_date} days'"
                             f"and state = 'active'")
    return count.iloc[0]["count"]


def count_active_users(first_date, second_date=0):
    count = lassie_get(query="SELECT count(distinct(user_id)) FROM smoking_actions "
                             f"WHERE smoke_at between now() - interval '{first_date} days'"
                             f" and now() - interval '{second_date} days'")
    return count.iloc[0]["count"]


def aha(first_date, second_date=0):
    count = lassie_get(query="WITH count_smoke AS (SELECT user_id FROM smoking_actions GROUP BY user_id HAVING count("
                             "smoke_at) > 5) SELECT count(distinct id) FROM users JOIN count_smoke ON "
                             "count_smoke.user_id = users.id WHERE users.created_at between "
                             f"now() - interval '{first_date} days' and now() - interval '{second_date} days'")
    return count.iloc[0]['count']


def interval(first_date, second_date=0):
    count = lassie_get(query="SELECT count(id) FROM users "
                             f"WHERE created_at between now() - interval '{first_date} days' "
                             f"and now() - interval '{second_date} days' and score > 0")
    return count.iloc[0]['count']
