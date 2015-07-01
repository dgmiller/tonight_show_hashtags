# Collect Twitter data from the Tonight Show starring Jimmy Fallon

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import os


# Authentication tokens and keys
ckey = "3dKkKQNv4IhDRYTAq6yGuMb8t"
csecret = "jnKsBAXm0dFlKDRasTmu2Y34eBT3EUSdj6YkFRaj4b290vPPJh"
atoken = "2533036867-6NWiHaQRBAWrcjy59g2PM4hX0tuUs1Hw3TTILpk"
asecret = "NgOmykbCoVEWVv6uRFeYlOTmFweH5h2fJOhZi6KGah8pN"

# The listener receives the data
class listener(StreamListener):
	def on_data(self, data):
		# Twitter returns data in JSON format which needs to be decoded
		decoded = json.loads(data)

		# Converts UTF-8 to ASCII
                print "@%s: (%s) %s" % (
                        decoded['user']['screen_name'],
                        decoded['created_at'],
                        decoded['text'].encode('ascii', 'ignore'))
		print ''
		return True

	def on_error(self, status):
		print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

twitterStream.filter(track=["car"])
