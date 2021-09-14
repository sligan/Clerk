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
    support_price, support_count = bmc(timestamps=timestamp.timestamps(1))
    client.chat_postMessage(channel=channel_id,
                            text='*Donations - Day*'
                                 f"\n Period: ({(timestamp.timestamps(1).strftime('%d ' + '%B'))}"
                                 f" - {datetime.today().strftime('%d ' + '%B')}) \n"
                                 f'\n Donations: {support_count}'
                                 f'\n Profit: ${support_price}')
    return Response(), 200


@app.route('/Donations-week', methods=['POST'])
def donations_week():
    data = request.form
    channel_id = data.get('channel_id')
    support_price, support_count = bmc(timestamps=timestamp.timestamps(7))
    client.chat_postMessage(channel=channel_id,
                            text='*Donations - Week*'
                                 f'\n Period: ({(timestamp.timestamps(7).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 f'\n Donations: {support_count}'
                                 f'\n Profit: ${support_price}')
    return Response(), 200


@app.route('/Donations-month', methods=['POST'])
def donations_month():
    data = request.form
    channel_id = data.get('channel_id')
    support_price, support_count = bmc(timestamps=timestamp.timestamps(30))
    client.chat_postMessage(channel=channel_id,
                            text='*Donations - Month*'
                                 f'\n Period: ({(timestamp.timestamps(30).strftime("%d " + "%B"))}'
                                 f' - {datetime.today().strftime("%d " + "%B")}) \n'
                                 f'\n Donations: {support_count}'
                                 f'\n Profit: ${support_price}')
    return Response(), 200


@app.route('/Donations-all', methods=['POST'])
def donations_all():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Donations*'
                                 f"\n Period: All time \n"
                                 '\n Buy Me a Coffee donations:'
                                 f'\n Value: {bmc(timestamps=timestamp.start_day())}$')
    return Response(), 200


def bmc(timestamps):
    support_price = 0
    support_count = 0
    auth = {'Authorization': os.getenv('BMC_TOKEN')}
    response = requests.get('https://developers.buymeacoffee.com/api/v1/supporters', headers=auth)
    for data in response.json()['data']:
        date = datetime.strptime(data['support_created_on'][:10], '%Y-%m-%d')
        if date > timestamps:
            support_price += float(data['support_coffee_price'])
            support_count += 1
    return support_price, support_count
