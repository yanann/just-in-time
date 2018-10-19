
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
import googlemaps

import configuration


START = "42.365515, -71.122141"


class Bot(object):

	"""
		Initializes Bot object
	"""
	def __init__(self):
		super(Bot, self).__init__()
		self.name = "justintime"
		self.emoji = ":dog:"
		
		# access app credentials
		self.oauth = {"client_id": configuration.SLACK_CLIENT_ID,
					  "client_secret": configuration.SLACK_CLIENT_SECRET,
					  "scope": "bot"}

		self.verification = configuration.SLACK_VER_TOKEN
		self.client = SlackClient(configuration.SLACK_BOT_TOKEN)

	"""
		Uses Google Maps API to find location of a place and determine estimated travel time btw HBS and destination
		----
		end: str destination
	"""
	def maps(self, destination, channel, response_code):
		
		#initialize Google Maps object
		gmaps = googlemaps.Client(key=configuration.GOOG_DISTANCE_KEY)

		#find address for the search term, restrict location to ~5 mile radius of HBS
		location_list = gmaps.places_autocomplete(destination, session_token = "0123456789", location = START, radius = 9000, strict_bounds= True)
		
		
		#if multiple returns, ask user to select one
		if len(location_list) > 1 and response_code == 0:
			bot_response = "Hm... we couldn't find your exact location. Is it any of the ones below?\n"
			
			for x in location_list:
				bot_response = bot_response + x["description"] + "\n"

			bot_response = bot_response + "\n Enter your response as 'Select [choice from list above]'"
	
			self.answer(channel, bot_response)
			return -1

		else:
			#select the first option as the destination
			selected_placeID = location_list[0]["place_id"]
			selected_placeID = "place_id:" + selected_placeID

			#calculate travel time
			results = gmaps.distance_matrix(START, destinations = selected_placeID)
			return results["rows"][0]["elements"][0]["duration"]["text"]

	"""
		Bot answers user
		----
		channel: str, Slack channel the bot will post to
		bot_response: str, message the bot will post
	"""
	def answer(self, channel, bot_response):
		
		#send message to user
		self.client.api_call('chat.postMessage',
			channel=channel,
			text= bot_response)

	"""
		Determine what kind of call and how bot should answer
		----
		slack_event: JSON, info on user's message
		response_code: int, identifies type of bot response
	"""

	def listener(self, slack_event, response_code):
		channel = slack_event["event"]['channel']
		bot_response = ""
		est_time = None

		if response_code == 0:
		
			#calculate estimated time to location user initially typed
			destination = slack_event["event"]["text"].split("travel time to ",1)[1]
			est_time = self.maps(destination, channel, 0)

			#if more than one location was found, return immediately
			if est_time == -1:
				return make_response("Task received", 200)

		else:
			#calculate estimated time to location user selected from list
			destination = slack_event["event"]["text"].split("select ",1)[1]
			est_time = self.maps(destination, channel, 1)
		
		bot_response = "The travel time to {} from HBS is {}".format(destination, est_time)
		self.answer(channel, bot_response)

		return make_response("Task received", 200)
