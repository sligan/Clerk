import os
import requests
from flask import request, Response
from main import app, client
from dotenv import load_dotenv
load_dotenv()


@app.route('/business', methods=['POST'])
def business():
    data = request.form
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id,
                            text='*Buy Me a Coffee*'
                                 '\n Total donations:'
                                 f'\n Value: {bmc()}$')
    return Response(), 200


def bmc():
    support = 0
    auth = {'Authorization': os.getenv('BMC_TOKEN')}
    response = requests.get('https://developers.buymeacoffee.com/api/v1/supporters', headers=auth)
    for data in response.json()['data']:
        support += float(data['support_coffee_price'])
    return support
