# Collect Twitter data from the Tonight Show starring Jimmy Fallon

import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os


# Authentication tokens and keys
ckey = "3dKkKQNv4IhDRYTAq6yGuMb8t"
consumer_secret = "jnKsBAXm0dFlKDRasTmu2Y34eBT3EUSdj6YkFRaj4b290vPPJh"
access_token_key = "2533036867-6NWiHaQRBAWrcjy59g2PM4hX0tuUs1Hw3TTILpk"
access_token_secret = "NgOmykbCoVEWVv6uRFeYlOTmFweH5h2fJOhZi6KGah8pN"


start_time = time.time() #grabs the system time
keyword_list = ['#byutami'] #track list


# listener class override
class listener(StreamListener):

    def __init__(self, start_time, time_limit=60):

        self.time = start_time
        self.limit = time_limit

    def on_data(self, data):

        while (time.time() - self.time) < self.limit:

            try:

                saveFile = open('raw_tweets.json', 'a')
                saveFile.write(data)
                saveFile.write('\n')
                saveFile.close()

                return True


            except BaseException, e:
                print 'failed ondata,', str(e)
                time.sleep(5)
                pass

        exit()

    def on_error(self, status):

        print statuses

auth = OAuthHandler(ckey, consumer_secret) # OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, listener(start_time, time_limit=20))
twitterStream.filter(track=keyword_list, languages=['en'])
