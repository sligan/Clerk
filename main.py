from slackeventsapi import SlackEventAdapter
from flask import Flask
from dotenv import load_dotenv
import slack
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception


load_dotenv()
app = Flask(__name__)
client = slack.WebClient(token=os.getenv('TOKEN'))
slack_event_adapter = SlackEventAdapter(os.getenv('SECRET'), '/slack/events', app)
scopes = ['https://www.googleapis.com/auth/analytics.readonly']
key_file_loc = os.getenv('GA_KEY_LOC')
view_id = os.getenv('GA_VIEW_ID')


@app.before_first_request
def init_rollbar():
    rollbar.init(os.getenv('ACCESS_TOKEN'), environment='development')
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


if __name__ == '__main__':
    from commands.breathhh import *
    app.run(port=os.getenv('PORT'))
