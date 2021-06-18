from slackeventsapi import SlackEventAdapter
from flask import Flask
from dotenv import load_dotenv
import slack
import os

load_dotenv()
app = Flask(__name__)
client = slack.WebClient(token=os.getenv('TOKEN'))
slack_event_adapter = SlackEventAdapter(os.getenv('SECRET'), '/slack/events', app)


if __name__ == '__main__':
    from commands.breathhh import *
    app.run(debug=False)
