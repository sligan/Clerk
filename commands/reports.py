import os
import schedule
from flask import Response
from datetime import datetime, timedelta
from commands.breathhh import breathhh_metrics, compare_metrics
from commands.Alpaca import alpaca_metrics, al_compare_metrics
from commands.lassie import lassie_metrics
from main import client
from commands import calculations
from dotenv import load_dotenv

load_dotenv()


# функция для вычисления каждых последующих 30 дней для автоотчета
def month_report_day():
    my_date = datetime.strptime("01/01/21", "%m/%d/%y")
    while my_date < datetime.today():
        my_date += timedelta(days=30)
    return int(my_date.day)


def weekly_report():

    l_new_users, l_compare_nu, l_new_users_landing, l_compare_nul, l_bounce_rate, l_compare_br, l_k_factor_rate, \
    l_compare_k_factor, l_conversion_to_user, l_compare_cto, l_aha_moment_rate, l_compare_amr, l_onboarding_rate, \
    l_compare_or, l_average_interval_increases_rate, l_compare_ir, l_compare_cau, l_active_users = \
        lassie_metrics(start='14DaysAgo', end='7DaysAgo', lower_date=7, higher_date=14)

    a_new_users_landing, a_conversion_to_install, a_bounce_rate, a_k_factor_rate, a_new_teams, a_aha_moment_rate, \
    a_active_teams = alpaca_metrics(higher_date=7, lower_date=0, start='7DaysAgo', end='today')

    a_new_users_compare, a_conversion_to_install_compare, a_bounce_rate_compare, a_k_factor_rate_compare, \
    a_new_teams_compare, a_aha_moment_rate_compare, a_active_teams_compare \
        = al_compare_metrics(higher_date=7, lower_date=0, start='7DaysAgo', end='today', higher_date_prev=14,
                             lower_date_prev=7, start_prev='14DaysAgo', end_prev='7DaysAgo')

    user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users \
        , install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate \
        , conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate \
        , warm_up_rel_rate, background_noise_rate, retention_one_day, retention_seven_day \
        = breathhh_metrics(7, 0, '7DaysAgo', '0DaysAgo')

    user_acquisition_compare, conversion_to_store_compare, conversion_to_user_compare, bounce_rate_compare, \
    k_factor_rate_compare, new_users_compare, install_rate_compare, onboarding_rate_compare, activation_rate, \
    active_users_prev_compare, deleted_users_rate_compare, uninstall_rate_compare, conversion_feedback_compare, \
    breathing_sim_rel_rate_compare, mood_picker_dairy_rate_compare, warm_up_rel_rate_compare, \
    background_noise_rate_compare, retention_one_day_compare, retention_seven_day_compare = \
        compare_metrics(7, 0, '7DaysAgo', '0DaysAgo', 14, 7, '14DaysAgo', '7DaysAgo')

    client.chat_postMessage(channel=os.getenv('CHANNEL'),
                            text='*Lassie Smoke – Week*\n'
                                 f"Period: {calculations.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {l_new_users_landing} ({l_compare_nul})\n'
                                 f'Conversion to User (CR1): {l_conversion_to_user}% ({l_compare_cto})\n'
                                 f'Bounce Rate: {round(l_bounce_rate, 1)}% ({l_compare_br})\n'
                                 f'K-factor Rate (Viral): {l_k_factor_rate}% ({l_compare_k_factor})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {l_new_users} ({l_compare_nu})\n'
                                 f'Onboarding Rate: {l_onboarding_rate}% ({l_compare_or})\n'
                                 f'Aha-moment Rate: {l_aha_moment_rate}% ({l_compare_amr})\n'
                                 f'Average Interval Increases Rate: '
                                 f'{l_average_interval_increases_rate}% ({l_compare_ir})\n'
                                 f'Active Users: {l_active_users} ({l_compare_cau})\n'
                                 '\n'
                                 '******************************************'
                                 '\n'
                                 '*Alpaca – Week*\n'
                                 f"Period: {calculations.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {a_new_users_landing} ({a_new_users_compare})\n'
                                 f'Conversion to Install (CR1): {a_conversion_to_install}%'
                                 f' ({a_conversion_to_install_compare})\n'
                                 f'Bounce Rate: {round(a_bounce_rate, 1)}% ({a_bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {a_k_factor_rate}% ({a_k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Teams: {a_new_teams} ({a_new_teams_compare})\n'
                                 f'Aha-moment Rate: {a_aha_moment_rate}% ({a_aha_moment_rate_compare})\n'
                                 f'Active Teams: {a_active_teams} ({a_active_teams_compare})\n'
                                 '\n'
                                 '******************************************'
                                 '\n'
                                 '*Breathhh - Week*\n'
                                 f"Period: {calculations.timestamps(7).strftime('%d ' + '%B')} "
                                 f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                 '\n'
                                 '*Marketing* 📢\n'
                                 f'User Acquisition (UA): {user_acquisition} ({user_acquisition_compare})\n'
                                 f'Conversion to Store (CR1): {conversion_to_store}% '
                                 f'({conversion_to_store_compare})\n'
                                 f'Conversion to User (CR2): {conversion_to_user}% ({conversion_to_user_compare})\n'
                                 f'Bounce Rate: {round(bounce_rate, 1)}% ({bounce_rate_compare})\n'
                                 f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 f'New Users: {new_users} ({new_users_compare})\n'
                                 f'Install Rate: {install_rate}% ({install_rate_compare})\n'
                                 f'Onboarding Rate: {onboarding_rate}% ({onboarding_rate_compare})\n'
                                 f'Activation Rate: :thinking_face:\n'
                                 f'Active Users: {active_users} ({active_users_prev_compare})\n'
                                 f"Average Day 1 Retention Rate: "
                                 f"{round(retention_one_day, 1)}% ({retention_one_day_compare})\n"
                                 f"Average Day 7 Retention Rate:"
                                 f" {round(retention_seven_day, 1)}% ({retention_seven_day_compare})\n"
                                 f'Deleted Users Rate: {deleted_users_rate}% ({deleted_users_rate_compare})\n'
                                 f'Uninstall Extension Rate: {uninstall_rate}% ({uninstall_rate_compare})\n'
                                 f'Conversion to Feedback: {conversion_feedback}% ({conversion_feedback_compare})\n'
                                 f'Breathing Simulator Relevance Rate: {breathing_sim_rel_rate}% '
                                 f'({breathing_sim_rel_rate_compare})\n'
                                 f'Mood Picker (Diary) Relevance Rate: {mood_picker_dairy_rate}% '
                                 f'({mood_picker_dairy_rate_compare})\n'
                                 f"Warm-Up's Relevance Rate: {warm_up_rel_rate}% ({warm_up_rel_rate_compare})\n"
                                 f'Background Noise Usage Rate: :thinking_face:')
    return Response(), 200


def monthly_report():
    if datetime.today().day == month_report_day():

        l_new_users, l_compare_nu, l_new_users_landing, l_compare_nul, l_bounce_rate, l_compare_br, l_k_factor_rate, \
        l_compare_k_factor, l_conversion_to_user, l_compare_cto, l_aha_moment_rate, l_compare_amr, l_onboarding_rate, \
        l_compare_or, l_average_interval_increases_rate, l_compare_ir, l_compare_cau, l_active_users = \
            lassie_metrics(start='60DaysAgo', end='30DaysAgo', lower_date=30, higher_date=60)

        a_new_users_landing, a_conversion_to_install, a_bounce_rate, a_k_factor_rate, a_new_teams, a_aha_moment_rate, \
        a_active_teams = alpaca_metrics(higher_date=30, lower_date=0, start='30DaysAgo', end='today')

        a_new_users_compare, a_conversion_to_install_compare, a_bounce_rate_compare, a_k_factor_rate_compare, \
        a_new_teams_compare, a_aha_moment_rate_compare, a_active_teams_compare \
            = al_compare_metrics(higher_date=30, lower_date=0, start='30DaysAgo', end='today', higher_date_prev=60,
                                 lower_date_prev=30, start_prev='60DaysAgo', end_prev='30DaysAgo')

        user_acquisition, conversion_to_store, conversion_to_user, bounce_rate, k_factor_rate, new_users \
            , install_rate, onboarding_rate, activation_rate, active_users, deleted_users_rate, uninstall_rate \
            , conversion_feedback, breathing_sim_rel_rate, mood_picker_dairy_rate \
            , warm_up_rel_rate, background_noise_rate, retention_one_day, retention_seven_day \
            = breathhh_metrics(30, 0, '30DaysAgo', '0DaysAgo')

        user_acquisition_compare, conversion_to_store_compare, conversion_to_user_compare, bounce_rate_compare, \
        k_factor_rate_compare, new_users_compare, install_rate_compare, onboarding_rate_compare, activation_rate, \
        active_users_prev_compare, deleted_users_rate_compare, uninstall_rate_compare, conversion_feedback_compare, \
        breathing_sim_rel_rate_compare, mood_picker_dairy_rate_compare, warm_up_rel_rate_compare, \
        background_noise_rate_compare, retention_one_day_compare, retention_seven_day_compare = \
            compare_metrics(30, 0, '30DaysAgo', '0DaysAgo', 60, 30, '60DaysAgo', '30DaysAgo')

        client.chat_postMessage(channel=os.getenv('CHANNEL'),
                                text='*Lassie Smoke – Month*\n'
                                     f"Period: {calculations.timestamps(30).strftime('%d ' + '%B')} "
                                     f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                     '\n'
                                     '*Marketing* 📢\n'
                                     f'User Acquisition (UA): {l_new_users_landing} ({l_compare_nul})\n'
                                     f'Conversion to User (CR1): {l_conversion_to_user}% ({l_compare_cto})\n'
                                     f'Bounce Rate: {round(l_bounce_rate, 1)}% ({l_compare_br})\n'
                                     f'K-factor Rate (Viral): {l_k_factor_rate}% ({l_compare_k_factor})\n'
                                     '\n'
                                     '*Product* 🍏\n'
                                     f'New Users: {l_new_users} ({l_compare_nu})\n'
                                     f'Onboarding Rate: {l_onboarding_rate}% ({l_compare_or})\n'
                                     f'Aha-moment Rate: {l_aha_moment_rate}% ({l_compare_amr})\n'
                                     f'Average Interval Increases Rate: '
                                     f'{l_average_interval_increases_rate}% ({l_compare_ir})\n'
                                     '\n'
                                     f'Active Users: {l_active_users} ({l_compare_cau})\n'
                                     '\n'
                                     '******************************************'
                                     '\n'
                                     '*Alpaca – Month*\n'
                                     f"Period: {calculations.timestamps(30).strftime('%d ' + '%B')} "
                                     f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                     '\n'
                                     '*Marketing* 📢\n'
                                     f'User Acquisition (UA): {a_new_users_landing} ({a_new_users_compare})\n'
                                     f'Conversion to Install (CR1): {a_conversion_to_install}%'
                                     f' ({a_conversion_to_install_compare})\n'
                                     f'Bounce Rate: {round(a_bounce_rate, 1)}% ({a_bounce_rate_compare})\n'
                                     f'K-factor Rate (Viral): {a_k_factor_rate}% ({a_k_factor_rate_compare})\n'
                                     '\n'
                                     '*Product* 🍏\n'
                                     f'New Teams: {a_new_teams} ({a_new_teams_compare})\n'
                                     f'Aha-moment Rate: {a_aha_moment_rate}% ({a_aha_moment_rate_compare})\n'
                                     f'Active Teams: {a_active_teams} ({a_active_teams_compare})\n'
                                     '\n'
                                     '******************************************'
                                     '\n'
                                     '*Breathhh - Month*\n'
                                     f"Period: {calculations.timestamps(30).strftime('%d ' + '%B')} "
                                     f"- {datetime.today().strftime('%d ' + '%B')}\n"
                                     '\n'
                                     '*Marketing* 📢\n'
                                     f'User Acquisition (UA): {user_acquisition} ({user_acquisition_compare})\n'
                                     f'Conversion to Store (CR1): {conversion_to_store}% '
                                     f'({conversion_to_store_compare})\n'
                                     f'Conversion to User (CR2): {conversion_to_user}% ({conversion_to_user_compare})\n'
                                     f'Bounce Rate: {round(bounce_rate, 1)}% ({bounce_rate_compare})\n'
                                     f'K-factor Rate (Viral): {k_factor_rate}% ({k_factor_rate_compare})\n'
                                     '\n'
                                     '*Product* 🍏\n'
                                     f'New Users: {new_users} ({new_users_compare})\n'
                                     f'Install Rate: {install_rate}% ({install_rate_compare})\n'
                                     f'Onboarding Rate: {onboarding_rate}% ({onboarding_rate_compare})\n'
                                     f'Activation Rate: :thinking_face:\n'
                                     f'Active Users: {active_users} ({active_users_prev_compare})\n'
                                     f"Average Day 1 Retention Rate: "
                                     f"{round(retention_one_day, 1)}% ({retention_one_day_compare})\n"
                                     f"Average Day 7 Retention Rate:"
                                     f" {round(retention_seven_day, 1)}% ({retention_seven_day_compare})\n"
                                     f'Deleted Users Rate: {deleted_users_rate}% ({deleted_users_rate_compare})\n'
                                     f'Uninstall Extension Rate: {uninstall_rate}% ({uninstall_rate_compare})\n'
                                     f'Conversion to Feedback: {conversion_feedback}% ({conversion_feedback_compare})\n'
                                     f'Breathing Simulator Relevance Rate: {breathing_sim_rel_rate}% '
                                     f'({breathing_sim_rel_rate_compare})\n'
                                     f'Mood Picker (Diary) Relevance Rate: {mood_picker_dairy_rate}% '
                                     f'({mood_picker_dairy_rate_compare})\n'
                                     f"Warm-Up's Relevance Rate: {warm_up_rel_rate}% ({warm_up_rel_rate_compare})\n"
                                     f'Background Noise Usage Rate: :thinking_face:')

        return Response(), 200


# недельный отчет в 23:59 по мск
schedule.every().sunday.at('20:59').do(weekly_report)
# отчет каждые 30 дней
schedule.every().day.at('20:59').do(monthly_report)
