import os
import schedule
import main
from flask import request, Response
from db_connect import breathhh_get
from datetime import datetime
from main import app, client
from commands import calculations
from dotenv import load_dotenv
import pandas as pd
from threading import Thread

load_dotenv()


# функция для вывода интервала (день\неделя\месяц)
def main_function(frst, scnd, frst_ga, scnd_ga, comp_frst, comp_scnd, comp_frst_ga, comp_scnd_ga, name, channel_id):
    user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users \
        , install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate \
        , conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate \
        , warm_up_rel_rate, background_noise_rate, retention_one_day, retention_seven_day \
        = breathhh_metrics(frst, scnd, frst_ga, scnd_ga)

    user_acquisition_compare, conversion_to_store_compare, conversion_to_user_compare, bounce_rate_compare, \
    k_factor_rate_compare, new_users_compare, install_rate_compare, onboarding_rate_compare, activation_rate, \
    active_users_prev_compare, deleted_users_rate_compare, uninstall_rate_compare, conversion_feedback_compare, \
    breathing_sim_rel_rate_compare, mood_picker_dairy_rate_compare, warm_up_rel_rate_compare, \
    background_noise_rate_compare, retention_one_day_compare, retention_seven_day_compare = \
        compare_metrics(frst, scnd, frst_ga, scnd_ga, comp_frst, comp_scnd, comp_frst_ga, comp_scnd_ga)

    client.chat_postMessage(channel=channel_id,
                            text=f'*Breathhh - {name}*\n'
                                 f"Period: {calculations.timestamps(frst).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {user_acquisition} ({user_acquisition_compare})\n'
                                 f'Conversion to Store (CR1): {conversion_to_store}% ({conversion_to_store_compare})\n'
                                 f'Conversion to User (CR2): {conversion_to_user}% ({conversion_to_user_compare})\n'
                                 f'Bounce Rate: {round(bounce_rate, 1)}% ({bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users} ({new_users_compare})\n'
                                 f'Install Rate: {install_rate}% ({install_rate_compare})\n'
                                 f'Onboarding Rate: {onboarding_rate}% ({onboarding_rate_compare})\n'
                                 f'Activation Rate: :thinking_face:\n'
                                 f'\n'
                                 f'Active Users: {active_users} ({active_users_prev_compare})\n'
                                 f"Average Day 1 Retention Rate: "
                                 f"{round(retention_one_day, 1)}% ({retention_one_day_compare})\n"
                                 f"Average Day 7 Retention Rate:"
                                 f" {round(retention_seven_day, 1)}% ({retention_seven_day_compare})\n"
                                 f'\n'
                                 f'Deleted Users Rate: {deleted_users_rate}% ({deleted_users_rate_compare})\n'
                                 f'Uninstall Extension Rate: {uninstall_rate}% ({uninstall_rate_compare})\n'
                                 f'Conversion to Feedback: {conversion_feedback}% ({conversion_feedback_compare})\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate: {breathing_sim_rel_rate}% '
                                 f'({breathing_sim_rel_rate_compare})\n'
                                 f'Mood Picker (Diary) Relevance Rate: {mood_picker_dairy_rate}% '
                                 f'({mood_picker_dairy_rate_compare})\n'
                                 f"Warm-Up's Relevance Rate: {warm_up_rel_rate}% ({warm_up_rel_rate_compare})\n"
                                 f'Background Noise Usage Rate: :thinking_face:')


#  функции для избежания ответа "operation time out" от Slack
@app.route('/breathhh-day', methods=['POST'])
def breathhh_day():
    data = request.form
    channel_id = data.get('channel_id')
    thr = Thread(target=main_function,
                 args=[1, 0, '1DaysAgo', '0DaysAgo', 2, 1, '2DaysAgo', '1DaysAgo', 'Day', channel_id])
    thr.start()
    return Response(), 200


@app.route('/breathhh-week', methods=['POST'])
def breathhh_week():
    data = request.form
    channel_id = data.get('channel_id')
    thr = Thread(target=main_function,
                 args=[7, 0, '7DaysAgo', '0DaysAgo', 14, 7, '14DaysAgo', '7DaysAgo', 'Week', channel_id])
    thr.start()
    return Response(), 200


@app.route('/breathhh-month', methods=['POST'])
def breathhh_month():
    data = request.form
    channel_id = data.get('channel_id')
    thr = Thread(target=main_function,
                 args=[30, 0, '30DaysAgo', '0DaysAgo', 60, 30, '60DaysAgo', '30DaysAgo', 'Month', channel_id])
    thr.start()
    return Response(), 200


# только вывод статистики за всё время
def main_function_all(channel_id):
    user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users, \
    install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate, \
    conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate, warm_up_rel_rate, background_noise_rate, \
    retention_one_day, retention_seven_day = \
        breathhh_metrics(calculations.start_day(), 0, f'{calculations.start_day()}DaysAgo', '0DaysAgo')

    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh - All*\n'
                                 f"Period: All time\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {user_acquisition}\n'
                                 f'Conversion to Store (CR1): {conversion_to_store}%\n'
                                 f'Conversion to User (CR2): {conversion_to_user}%\n'
                                 f'Bounce Rate: {round(bounce_rate)}%\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}%\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users}\n'
                                 f'Install Rate: {install_rate}%\n'
                                 f'Onboarding Rate: {onboarding_rate}%\n'
                                 f'Activation Rate: :thinking_face:\n'
                                 f'\n'
                                 f'Active Users: {active_users}\n'
                                 f'Average Day 1 Retention Rate: '
                                 f'{round(retention_one_day, 1)}%\n'
                                 f'Average Day 7 Retention Rate: '
                                 f'{round(retention_seven_day, 1)}%\n'
                                 f'\n'
                                 f'Deleted Users Rate: {deleted_users_rate}%\n'
                                 f'Uninstall Rate: {uninstall_rate}%\n'
                                 f'Conversion to Feedback: {conversion_feedback}%\n'
                                 f'\n'
                                 f'Breathing Simulator Relevance Rate: {breathing_sim_rel_rate}%\n'
                                 f'Mood Picker (Diary) Relevance Rate: {mood_picker_dairy_rate}%\n'
                                 f"Warm-Up's Relevance Rate: {warm_up_rel_rate}%\n"
                                 f'Background Noise Usage Rate: :thinking_face:')


@app.route('/breathhh-all', methods=['POST'])
def breathhh_all():
    data = request.form
    channel_id = data.get('channel_id')
    thr = Thread(target=main_function_all, args=[channel_id])
    thr.start()
    return Response(), 200


# функция которая считает статистики за период по заданным интервалам
def breathhh_metrics(higher_date, lower_date, start, end):
    user_acquisition = int(breathhh_ga_metrics(startDate=start, metrics="ga:newUsers", endDate=end)['ga:newUsers'][0])

    conversion_to_store = calculations.compare2_0(int(
        breathhh_ga_metrics(startDate=start, metrics="ga:users",
                            endDate=end,
                            dimensions=[{'name': 'ga:pagePath'}],
                            filters='ga:pagePath=@/webstore/detail/ext')
        ['ga:users'].sum()),
        user_acquisition)

    conversion_to_user = calculations.compare2_0(new_users_db(higher_date, lower_date),
                                                 user_acquisition)
    try:
        bounce_rate = breathhh_ga_metrics(startDate=start, metrics="ga:bounceRate", endDate=end)['ga:bounceRate'][0]
    except IndexError:
        bounce_rate = 0

    k_factor_rate = calculations.compare2_0(int(breathhh_ga_metrics(
        startDate=start, endDate=end, metrics="ga:newUsers",
        dimensions=[{'name': 'ga:referralPath'}])['ga:newUsers'][0]), user_acquisition)

    new_users = new_users_db_installed(higher_date, lower_date)
    install_rate = calculations.compare2_0(new_users_db_installed(higher_date, lower_date), user_acquisition)
    onboarding_rate = calculations.compare2_0(onboard_users(higher_date, lower_date), new_users)
    activation_rate = ''  # пока не нужно
    active_users = active_users_db(higher_date, lower_date)
    deleted_users_rate = calculations.compare2_0(acc_removed(higher_date, lower_date), active_users)
    uninstall_rate = calculations.compare2_0(ext_removed(higher_date, lower_date), active_users)
    conversion_feedback = conversion_to_feedback(higher_date, lower_date)
    breathing_sim_rel_rate = simulator_relevance_rate(higher_date, lower_date)
    mood_picker_dairy_rate = picker_relevance_rate(higher_date, lower_date)
    warm_up_rel_rate = warm_up_relevance_rate(higher_date, lower_date)
    background_noise_rate = ''
    retention_one_day = retention_by_day(higher_date, lower_date, days=1)
    retention_seven_day = retention_by_day(higher_date, lower_date, days=7)

    return user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users, \
           install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate, \
           conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate, \
           warm_up_rel_rate, background_noise_rate, retention_one_day, retention_seven_day


# возвращает % от сравнения интервалов (настоящий / предыдущий)
def compare_metrics(higher_date, lower_date, start, end, higher_date_prev, lower_date_prev, start_prev, end_prev):
    user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users, \
    install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate, \
    conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate, warm_up_rel_rate, background_noise_rate, \
    retention_one_day, retention_seven_day = breathhh_metrics(higher_date, lower_date, start, end)

    user_acquisition_prev, conversion_to_store_prev, conversion_to_user_prev, bounce_rate_prev, k_factor_rate_prev, \
    new_users_prev, install_rate_prev, onboarding_rate_prev, activation_rate_prev, active_users_prev, \
    deleted_users_rate_prev, uninstall_rate_prev, conversion_feedback_prev, breathing_sim_rel_rate_prev, \
    mood_picker_dairy_rate_prev, warm_up_rel_rate_prev, background_noise_rate_prev, retention_one_day_prev, \
    retention_seven_day_prev = breathhh_metrics(higher_date_prev, lower_date_prev, start_prev, end_prev)

    user_acquisition_compare = calculations.compare(user_acquisition, user_acquisition_prev)
    conversion_to_store_compare = calculations.compare(conversion_to_store, conversion_to_store_prev)
    conversion_to_user_compare = calculations.compare(conversion_to_user, conversion_to_user_prev)
    bounce_rate_compare = calculations.compare(bounce_rate, bounce_rate_prev)
    k_factor_rate_compare = calculations.compare(k_factor_rate, k_factor_rate_prev)
    new_users_compare = calculations.compare(new_users, new_users_prev)
    install_rate_compare = calculations.compare(install_rate, install_rate_prev)
    onboarding_rate_compare = calculations.compare(onboarding_rate, onboarding_rate_prev)
    activation_rate = ''  # in progress
    active_users_prev_compare = calculations.compare(active_users, active_users_prev)
    deleted_users_rate_compare = calculations.compare(deleted_users_rate, deleted_users_rate_prev)
    uninstall_rate_compare = calculations.compare(uninstall_rate, uninstall_rate_prev)
    conversion_feedback_compare = calculations.compare(conversion_feedback, conversion_feedback_prev)
    breathing_sim_rel_rate_compare = calculations.compare(breathing_sim_rel_rate, breathing_sim_rel_rate_prev)
    mood_picker_dairy_rate_compare = calculations.compare(mood_picker_dairy_rate, mood_picker_dairy_rate_prev)
    warm_up_rel_rate_compare = calculations.compare(warm_up_rel_rate, warm_up_rel_rate_prev)
    background_noise_rate_compare = ''  # in progress
    retention_one_day_compare = calculations.compare(retention_one_day, retention_one_day_prev)
    retention_seven_day_compare = calculations.compare(retention_seven_day, retention_seven_day_prev)

    return user_acquisition_compare, conversion_to_store_compare, conversion_to_user_compare, bounce_rate_compare, \
           k_factor_rate_compare, new_users_compare, install_rate_compare, onboarding_rate_compare, activation_rate, \
           active_users_prev_compare, deleted_users_rate_compare, uninstall_rate_compare, conversion_feedback_compare, \
           breathing_sim_rel_rate_compare, mood_picker_dairy_rate_compare, warm_up_rel_rate_compare, \
           background_noise_rate_compare, retention_one_day_compare, retention_seven_day_compare


# функция для вывода информации из GA
def breathhh_ga_metrics(startDate, metrics, endDate, dimensions=None, filters=''):
    response = main.analytics.reports().batchGet(
        body=dict(reportRequests=[dict(viewId=os.getenv('GA_VIEW_ID_BREATHHH'),
                                       dateRanges=[{'startDate': startDate, 'endDate': endDate}],
                                       dimensions=dimensions,
                                       metrics=[{'expression': metrics}],
                                       filtersExpression=filters)])).execute()
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeader = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        df_columns = dimensionHeader + [head['name'] for head in metricHeaders]
        df_rows = []
        for row in rows:
            dimension = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])[0].get('values', [])
            df_row = dimension + [float(value) for value in dateRangeValues]
            df_rows.append(df_row)
        return pd.DataFrame(df_rows, columns=df_columns)


# SQL запросы
def new_users_db_installed(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(id) "
                               "FROM users "
                               "WHERE extension_state = 'extension_installed' "
                               f"and created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def new_users_db(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(id) "
                               "FROM users "
                               "WHERE created_at between"
                               f" now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def onboard_users(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(id) "
                               "FROM users "
                               "WHERE onboarding_state = 'onboarding_extension_installed_step' "
                               "and extension_state ='extension_installed' "
                               f"and created_at between now() - interval'{higher_date} days' and now() - interval "
                               f"'{lower_date} days'")
    return count.iloc[0]["count"]


def active_users_db(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(distinct user_id) "
                               "FROM actions where created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def ext_removed(higher_date, lower_date=0):
    count = breathhh_get(query="with active_users as (select distinct user_id from actions where created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days') "
                               f"select count(id) from users right join active_users "
                               f"on active_users.user_id = users.id "
                               f"where extension_state = 'extension_removed'")
    return count.iloc[0]["count"]


def acc_removed(higher_date, lower_date=0):
    count = breathhh_get(query="WITH active_users as "
                               "(SELECT distinct user_id "
                               "FROM actions "
                               "WHERE created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days') "
                               f"SELECT count(id) "
                               f"FROM users RIGHT JOIN active_users ON active_users.user_id = users.id "
                               f"WHERE name = 'deleted_user'")
    return count.iloc[0]["count"]


def conversion_to_feedback(higher_date, lower_date=0):
    del_users = breathhh_get(query="SELECT count(id) AS count_del "
                                   "FROM users "
                                   "WHERE extension_state = 'extension_removed' "
                                   f"and updated_at between now()-interval '{higher_date} days' "
                                   f"and now()-interval '{lower_date} days'")

    del_with_feedback = breathhh_get(query="SELECT count(user_id) AS count_feedback "
                                           "FROM feedbacks "
                                           f"WHERE created_at between now()-interval '{higher_date} days' "
                                           f"and now()-interval '{lower_date} days'")
    percent = calculations.compare2_0(del_with_feedback.iloc[0]['count_feedback'], del_users.iloc[0]['count_del'])
    return percent


def simulator_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT EXTRACT(seconds FROM closed_at - opened_at) AS active_time "
                               "FROM actions "
                               "WHERE kind in ('extension','breathing') and created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    sum_all = count['active_time'].count()
    more = (count['active_time'] > 5).sum()
    calc = calculations.compare2_0(more, sum_all)
    return calc


def picker_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="WITH count_actions AS("
                               "SELECT count(created_at) as actions "
                               "FROM actions "
                               "WHERE kind = 'diary' and "
                               "created_at between "
                               f"now()-interval '{higher_date} days' and now() - interval '{lower_date} days'), "
                               "count_moods AS "
                               "(SELECT count(created_at) as moods "
                               "FROM moods "
                               f"WHERE created_at between "
                               f"now()-interval '{higher_date} days' and now() - interval '{lower_date} days') "
                               "SELECT * "
                               "FROM count_actions, count_moods")
    from_actions = count['actions'].iloc[0]
    from_moods = count['moods'].iloc[0]
    rate = calculations.compare2_0(from_moods, from_actions)
    return rate


def warm_up_relevance_rate(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT EXTRACT(seconds FROM closed_at - opened_at) AS active_time "
                               "FROM actions where url='diary' and created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    sum_all = count['active_time'].count()
    more = (count['active_time'] > 5).sum()
    calc = calculations.compare2_0(more, sum_all)
    return calc


def feedback_users(higher_date, lower_date=0):
    count = breathhh_get(query="SELECT count(user_id) "
                               "FROM feedbacks "
                               "WHERE created_at between "
                               f"now() - interval '{higher_date} days' and now() - interval '{lower_date} days'")
    return count.iloc[0]["count"]


def retention_by_day(higher_date=60, lower_date=0, days=1):
    ret = breathhh_get(
        query="WITH mydates AS "
              "(SELECT date_trunc('day', dates.dates)::date AS dates FROM generate_series"
              "((SELECT min(created_at) FROM actions), (SELECT max(created_at) FROM actions), interval '1 day') "
              "AS dates), ret AS "
              "(SELECT distinct date_trunc('day', actions.created_at)::date AS date, "
              "count(distinct actions.user_id) AS active_users, count(distinct future_actions.user_id) "
              "AS retained_users, count(distinct future_actions.user_id)::float / count(distinct actions.user_id)"
              "::float*100 AS retention "
              "FROM actions "
              "LEFT JOIN actions AS future_actions on actions.user_id = future_actions.user_id and "
              "date_trunc('day', actions.created_at)::date = "
              f"date_trunc('day', future_actions.created_at)::date - interval '{days} Days' "
              "WHERE actions.kind != 'url' "
              "group by 1) "
              "SELECT avg(retention) "
              "FROM mydates "
              "LEFT JOIN ret on mydates.dates = ret.date "
              f"WHERE dates between now() - interval '{higher_date + 1} days' and now() - interval '{lower_date} days'")
    return ret['avg'][0]


# информация ии breathhh-week каждое воскресенье в 23:59 по МСК
schedule.every().sunday.at('20:59').do(main_function, 7, 0, '7DaysAgo', '0DaysAgo', 14, 7, '14DaysAgo',
                                       '7DaysAgo', 'Week', os.getenv('CHANNEL'))

# информация из breathhh-month каждые 30 дней в 23:59 по МСК
schedule.every(30).days.at('20:59').do(main_function, 30, 0, '30DaysAgo', '0DaysAgo', 60, 30, '60DaysAgo', '30DaysAgo',
                                       'Month', os.getenv('CHANNEL'))
