import json
import slackclient
from flask import Flask, request, make_response, render_template

import configuration
import bot
import sys
import googlemaps

JIT_bot = bot.Bot()
slack = JIT_bot.client

app = Flask(__name__)


START = "42.365515, -71.122141"

"""
Event handling
----
eventy_type: str,  Slack event type captured
slack_event: JSON, Information about the Slack event

"""
def _event_handler(event_type, slack_event):
	# call on the bot to answer if it was mentioned
	if event_type == "app_mention" and "travel time" in slack_event["event"]["text"]:
		
		#notify bot that a user wants to find the travel time
		JIT_bot.listener(slack_event, 0)
		return make_response("Task received", 200) 

	elif event_type == "app_mention" and "select" in slack_event["event"]["text"]:
		
		#notify bot that a user has selected a loation
		JIT_bot.listener(slack_event, 1)
		return make_response("Task received", 200) 

	else:

		# Return error message if the event_type does not have a handler
		message = "You have not added a handler for %s" % event_type
		return make_response(message, 200, {"X-Slack-No-Retry": 1})


"""
Listens to incoming events from Slack
"""
@app.route("/", methods=["POST"])
def hears():
	slack_event = json.loads(request.data)

	#listen for verification POST
	if "challenge" in slack_event:
		return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

	#if event is something the bot is subcribed to, then pass event to event_type
	if "event" in slack_event:
		event_type = slack_event["event"]["type"]
		return _event_handler(event_type, slack_event)

	#error handling of non-subscribed events
	else:
		return make_response("Incorrect request!", 404, {"X-Slack-No-Retry": 1})


"""
Default landing page for URL
"""
@app.route("/", methods=["GET"])

def hello():
	return "Hello world!"

if __name__ == "__main__":
	app.run()


