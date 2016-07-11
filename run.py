import json
import sqlite3
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# project imports
import database

# stream listener class
class Streamy(StreamListener):
	def on_data(self, data):
		try:
			print(data.name+" ["+data.created_at+"]")
			print(data.text)
			if data.geo_enabled == True:
				print("\tGeo Supplied: "+data.place.name+" ["+data.place.place_type+"]")
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		print(status)
		return True

# open config file
with open('config.json') as config_file:
	config = json.load(config_file)
	print(config)

# connect to twitter
auth = OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_token"], config["access_secret"])
api = tweepy.API(auth)

# access streaming list, if supplied
list_members = []
if config["list_name"] == 0:
	print("Accessing livestream for user ["+api.me().name+"]")
else:
	userlist = api.list_members(api.me().name, config["list_name"])
	for user in userlist:
		list_members.append(user.id_str)
	print("Accessing livestream for user ["+api.me().name+"] and list ("+config["list_name"]+"), counting "+str(len(userlist))+" list members.")

twitter_stream = Stream(auth, Streamy())
if len(list_members) > 0:
	twitter_stream.filter(follow=list_members)
print("Starting StreamyMcStreamface")
