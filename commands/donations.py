import os
import requests
from flask import request, Response
from main import app, client
from dotenv import load_dotenv
from commands import timestamp
from datetime import datetime
load_dotenv()


@app.route('/donations-day', methods=['POST'])
def donations_day():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Donations*'
                                 f"\n Period: Day ({(timestamp.yesterday.strftime('%d ' + '%B'))}"
                                 f" - {datetime.today().strftime('%d ' + '%B')}) \n"
                                 '\n Buy Me a Coffee donations:'
                                 f'\n Value: {bmc(timestamps=timestamp.yesterday)}$')
    return Response(), 200


@app.route('/Donations-week', methods=['POST'])
def donations_week():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Donations*'
                                 f'\n Period: Week ({(timestamp.week.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 '\n Buy Me a Coffee donations:'
                                 f'\n Value: {bmc(timestamps=timestamp.week)}$')
    return Response(), 200


@app.route('/Donations-month', methods=['POST'])
def donations_month():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Donations*'
                                 f'\n Period: Month ({(timestamp.month.strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 '\n Buy Me a Coffee donations:'
                                 f'\n Value: {bmc(timestamps=timestamp.month)}$')
    return Response(), 200


@app.route('/Donations-all', methods=['POST'])
def donations_all():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Donations*'
                                 f"\n Period: All time \n"
                                 '\n Buy Me a Coffee donations:'
                                 f'\n Value: {bmc(timestamps=timestamp.start_2021)}$')
    return Response(), 200


def bmc(timestamps):
    support_price = 0
    auth = {'Authorization': os.getenv('BMC_TOKEN')}
    response = requests.get('https://developers.buymeacoffee.com/api/v1/supporters', headers=auth)
    for data in response.json()['data']:
        date = datetime.strptime(data['support_created_on'][:10], '%Y-%m-%d')
        if date > timestamps:
            support_price += float(data['support_coffee_price'])
    return support_price
