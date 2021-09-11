import os
import schedule
import main
from flask import request, Response
from db_connect import breathhh_get
from datetime import datetime
from main import app, client
from commands import timestamp
from dotenv import load_dotenv

load_dotenv()


@app.route('/help', methods=['POST'])
def help_clerk():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Commands*:  \n'
                                 '/lassie-all - показатели за всё время \n'
                                 '/lassie-day - показатели за день \n'
                                 '/lassie-week - показатели за неделю \n'
                                 '/lassie-month - показатели за месяц \n'
                                 '/breathhh-all - показатели за всё время \n'
                                 '/breathhh-day - показатели за день \n'
                                 '/breathhh-week - показатели за неделю \n'
                                 '/breathhh-month - показатели за месяц \n'
                                 '/donations-all - показатели за всё время \n'
                                 '/donations-day - показатели за день \n'
                                 '/donations-week - показатели за неделю \n'
                                 '/donations-month - показатели за месяц \n')

    return Response(), 200


@app.route('/breathhh-day', methods=['POST'])
def breathhh_day():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*\n'
                                 f"Period: {timestamp.timestamps(1).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA):\n'
                                 f'Conversion to Store (CR1):\n'
                                 f'Conversion to User (CR2):\n'
                                 f'Bounce Rate:\n'
                                 'K-factor Rate (Viral):\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users:\n'
                                 f'Install Rate'
                                 f'Onboarding Rate:\n'
                                 f'Activation Rate:\n'
                                 f'\n'
                                 f'Active Users:\n'
                                 f'Average Day 1 Retention Rate:\n'
                                 f'Average Day 7 Retention Rate:\n'
                                 f'\n'
                                 f'Deleted Users Rate:\n'
                                 f'Uninstall Rate:\n'
                                 f'Conversion to Feedback:\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate:\n'
                                 f'Mood Picker (Diary) Relevance Rate:\n'
                                 f"Warm-Up's Relevance Rate:\n"
                                 f'Background Noise Usage Rate:')

    return Response(), 200


@app.route('/breathhh-week', methods=['POST'])
def breathhh_week():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*\n'
                                 f"Period: {timestamp.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA):\n'
                                 f'Conversion to Store (CR1):\n'
                                 f'Conversion to User (CR2):\n'
                                 f'Bounce Rate:\n'
                                 'K-factor Rate (Viral):\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users:\n'
                                 f'Install Rate'
                                 f'Onboarding Rate:\n'
                                 f'Activation Rate:\n'
                                 f'\n'
                                 f'Active Users:\n'
                                 f'Average Day 1 Retention Rate:\n'
                                 f'Average Day 7 Retention Rate:\n'
                                 f'\n'
                                 f'Deleted Users Rate:\n'
                                 f'Uninstall Rate:\n'
                                 f'Conversion to Feedback:\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate:\n'
                                 f'Mood Picker (Diary) Relevance Rate:\n'
                                 f"Warm-Up's Relevance Rate:\n"
                                 f'Background Noise Usage Rate:')

    return Response(), 200


@app.route('/breathhh-month', methods=['POST'])
def breathhh_month():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*\n'
                                 f"Period: {timestamp.timestamps(30).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA):\n'
                                 f'Conversion to Store (CR1):\n'
                                 f'Conversion to User (CR2):\n'
                                 f'Bounce Rate:\n'
                                 'K-factor Rate (Viral):\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users:\n'
                                 f'Install Rate'
                                 f'Onboarding Rate:\n'
                                 f'Activation Rate:\n'
                                 f'\n'
                                 f'Active Users:\n'
                                 f'Average Day 1 Retention Rate:\n'
                                 f'Average Day 7 Retention Rate:\n'
                                 f'\n'
                                 f'Deleted Users Rate:\n'
                                 f'Uninstall Rate:\n'
                                 f'Conversion to Feedback:\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate:\n'
                                 f'Mood Picker (Diary) Relevance Rate:\n'
                                 f"Warm-Up's Relevance Rate:\n"
                                 f'Background Noise Usage Rate:')
    return Response(), 200


@app.route('/breathhh-all', methods=['POST'])
def breathhh_all():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh*\n'
                                 f"Period: All time\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA):\n'
                                 f'Conversion to Store (CR1):\n'
                                 f'Conversion to User (CR2):\n'
                                 f'Bounce Rate:\n'
                                 'K-factor Rate (Viral):\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users:\n'
                                 f'Install Rate'
                                 f'Onboarding Rate:\n'
                                 f'Activation Rate:\n'
                                 f'\n'
                                 f'Active Users:\n'
                                 f'Average Day 1 Retention Rate:\n'
                                 f'Average Day 7 Retention Rate:\n'
                                 f'\n'
                                 f'Deleted Users Rate:\n'
                                 f'Uninstall Rate:\n'
                                 f'Conversion to Feedback:\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate:\n'
                                 f'Mood Picker (Diary) Relevance Rate:\n'
                                 f"Warm-Up's Relevance Rate:\n"
                                 f'Background Noise Usage Rate:')

    return Response(), 200


def breathhh_ga_metrics(startDate, metrics, endDate):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_BREATHHH'),
                                       dateRanges=[{'startDate': startDate, 'endDate': endDate}],
                                       metrics=[{'expression': metrics}])])).execute()
    for report in response.get('reports', []):
        columnheader = report.get('columnHeader', {})
        metricheaders = columnheader.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            daterangevalues = row.get('metrics', [])
            for i, values in enumerate(daterangevalues):
                for metricheaders, value in zip(metricheaders, values.get('values')):
                    return value


def breathhh_metrics(higher_date, lower_date, startDate, endDate):
    user_acquisition = breathhh_ga_metrics(startDate=startDate, metrics="ga:newUsers", endDate=endDate)
    conversion_to_store = 123 / user_acquisition
    conversion_to_user = timestamp.compare(new_users_db(higher_date, lower_date),
                                           user_acquisition)  # все пользователи которые попали в базу?
    bounce_rate = float(breathhh_ga_metrics(startDate=startDate, metrics="ga:bounceRate", endDate=endDate))
    k_factor_rate = ''
    new_users = new_users_db_installed(higher_date, lower_date)  # а тут только те, которые ext_installed
    install_rate = timestamp.compare(new_users_db_installed(higher_date, lower_date), user_acquisition)
    onboarding_rate = timestamp.compare(onboard_users(higher_date, lower_date), new_users)
    active_users = active_users_db(higher_date, lower_date)
    one_day_retention = ''
    seven_day_retention = ''
    deleted_users_rate = timestamp.compare(acc_removed(higher_date, lower_date), active_users)
    uninstall_rate = timestamp.compare(ext_removed(higher_date, lower_date), active_users)
    conversion_to_feedback = ''  # где узнать то дал фидбек или нет челик
    breathing_sim_rel_rate = simulator_relevance_rate(higher_date, lower_date)
    warm_up_rel_rate = warm_up_relevance_rate(higher_date, lower_date)
    background_noise_rate = ''


# schedule.every().sunday.at('20:59').do(weekly_report)
# schedule.every().day.at('21:00').do(monthly_report)


def new_users_db_installed(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(id) FROM users WHERE extension_state = 'extension_installed' and "
                               f"created_at between now() - interval '{higher_date} days' "
                               f"and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def new_users_db(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(id) FROM users WHERE created_at between"
                               f" now() - interval '{higher_date} days' and interval '{lower_date} days'")
    return count.iloc[0]["count"]


def onboard_users(higher_date, lower_date=0):
    count = breathhh_get(query="select count(id) from users where onboarding_state ="
                               "'onboarding_extension_installed_step' and extension_state ='extension_installed'"
                               f"and created_at between now() - interval'{higher_date} days' and interval"
                               f"'{lower_date} days'")
    return count.iloc[0]["count"]


def active_users_db(higher_date, lower_date=0):
    count = breathhh_get(query="select count(distinct user_id) from actions where created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def ext_removed(higher_date, lower_date=0):
    count = breathhh_get(query="with active_users as (select distinct user_id from actions where created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days') "
                               f"select count(id) from users right join active_users on active_users.user_id = users.id"
                               f" where extension_state = 'extension_removed'")
    return count.iloc[0]["count"]


def acc_removed(higher_date, lower_date=0):
    count = breathhh_get(query="with active_users as (select distinct user_id from actions where created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days') "
                               f"select count(id) from users right join active_users on active_users.user_id = users.id"
                               f" where name = 'deleted_user'")
    return count.iloc[0]["count"]


def simulator_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="select count(extract(seconds from closed_at - opened_at)) as active_time "
                               "from actions where kind in ('extension','breathing') and created_at between"
                               f" now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    more, lower = (count['active_time'] > 5).sum(), (count['active_time'] < 5).sum()
    calc = timestamp.compare(lower, more)
    return calc


def picker_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="select count(extract(seconds from closed_at - opened_at)) as active_time "
                               "from actions where url='diary' and created_at between"
                               f" now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    more, lower = (count['active_time'] > 5).sum(), (count['active_time'] < 5).sum()
    calc = timestamp.compare(lower, more)
    return calc


def warm_up_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="select count(extract(seconds from closed_at - opened_at)) as active_time "
                               "from actions where url='diary' and created_at between"
                               f" now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    more, lower = (count['active_time'] > 5).sum(), (count['active_time'] < 5).sum()
    calc = timestamp.compare(lower, more)
    return calc
