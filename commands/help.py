from flask import request, Response
from main import app, client


# help с описанием метрик
@app.route('/breathhh-help', methods=['POST'])
def breathhh_help():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Breathhh - Help*\n'
                                 '*Marketing* 📢\n'
                                 'User Acquisition (UA) - Количество новых пользователей на лендинге.\n'
                                 'Conversion to Store (CR1) - Отношение количества новых пользователей на лендинге, '
                                 'к пользователям ушедшим в Web Store. \n'
                                 'Conversion to User (CR2) - Отношение количества новых пользователей лендинга, к '
                                 'зарегистрированным пользователям. \n'
                                 'Bounce Rate - Показатель отказов с лендинга. \n'
                                 'K-factor Rate (Viral) - Процент пользователей, пришедших на лендинг напрямую, '
                                 'без реферальных ссылок со сторонних сайтов. \n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 'New Users - Количество новых пользователей в базе данных. \n'
                                 'Install Rate - Процент пользователей лендинга, которые установил расширение. \n'
                                 'Onboarding Rate - Процент пользователей лендинга, которые прошли онбординг. \n'
                                 'Activation Rate - _in progress_ \n'
                                 '\n'
                                 'Active Users - Количество активных пользователей. \n'
                                 'Average Day 1 Retention Rate - Процент пользователей, которые продолжили '
                                 'использовать продукт на следующий день. \n '
                                 'Average Day 7 Retention Rate - Процент пользователей, который продолжили '
                                 'использовать продукт на седьмой день. \n'
                                 '\n'
                                 'Deleted Users Rate - Процент активных пользователей удаливших аккаунт. \n'
                                 'Uninstall Rate - Процент активных пользователей удаливших расширение. \n'
                                 'Conversion to Feedback - Процент пользователей, которые оставили обратную связь '
                                 'после удаления расширения. \n'
                                 '\n'
                                 'Breathing Simulator Relevance Rate - Процент вкладок с дыханием, которые закрыли '
                                 'более чем за 5 секунд. \n '
                                 'Mood Picker (Diary) Relevance Rate - Процент вкладок с дневником настроения, '
                                 'в которых была реаакция (поставлен смайл). \n '
                                 "Warm-Up's Relevance Rate - Процент вкладок с разминкой, которые закрыли "
                                 "более чем за 5 секунд. \n "
                                 'Background Noise Usage Rate - _in progress_')
    return Response(), 200


@app.route('/lassie-help', methods=['POST'])
def lassie_help():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Lassie Smoke - Help*\n'
                                 '*Marketing* 📢\n'
                                 'User Acquisition (UA) - Количество новых пользователей на лендинге.\n'
                                 'Conversion to User (CR1) - Отношение количества новых пользователей лендинга к '
                                 'зарегистрированным пользователям. \n'
                                 'Bounce Rate - Показатель отказов с лендинга.\n'
                                 'K-factor Rate (Viral) - Процент пользователей, пришедших на лендинг напрямую, '
                                 'без реферальных ссылок со сторонних сайтов. \n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 'New Users - Количество новых пользователей в базе данных.\n'
                                 'Onboarding Rate - Процент пользователей лендинга, которые прошли онбординг. \n'
                                 'Aha-moment Rate - Процент пользователей, которые как выкурили, как минимум, '
                                 '3 сигареты.\n '
                                 'Average Interval Increases Rate - Процент пользователей, которые увеличили '
                                 'интервал между курением.\n '
                                 'Active Users - Количество активных пользователей.')
    return Response(), 200


@app.route('/alpaca-help', methods=['POST'])
def alpaca_help():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Alpaca - Help*\n'
                                 '*Marketing* 📢\n'
                                 'User Acquisition (UA) - Количество новых пользователей на лендинге.\n'
                                 'Conversion to Install (CR1) - Процент пользователей с лендинга, которые начали'
                                 ' пользоваться продуктом. \n'
                                 'Bounce Rate - Показатель отказов с лендинга.\n'
                                 'K-factor Rate (Viral) - Процент пользователей, пришедших на лендинг напрямую, '
                                 'без реферальных ссылок со сторонних сайтов. \n'
                                 '\n'
                                 '*Product* 🍏\n'
                                 'New Teams - Количество новых команд в базе данных. \n'
                                 'Aha-moment Rate - Процент новых команд, которым Alpaca ответила сокращенной ссылкой '
                                 'как минимум 3 раза. \n'
                                 'Active Teams - Количество активных команд.')
    return Response(), 200
