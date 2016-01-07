# Collect Twitter data from the Tonight Show starring Jimmy Fallon

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from . import dataset
import json
import os


# Authentication tokens and keys
ckey = "3dKkKQNv4IhDRYTAq6yGuMb8t"
csecret = "jnKsBAXm0dFlKDRasTmu2Y34eBT3EUSdj6YkFRaj4b290vPPJh"
atoken = "2533036867-6NWiHaQRBAWrcjy59g2PM4hX0tuUs1Hw3TTILpk"
asecret = "NgOmykbCoVEWVv6uRFeYlOTmFweH5h2fJOhZi6KGah8pN"

# The listener receives the data
class listener(StreamListener):

    ##the injection method recieves a string and will be called
    # with each tweet
    def __init__ (self, injection_method) :
        self.injection_method = injection_method

    def on_data(self, data):
        # Twitter returns data in JSON format which needs to be decoded
        decoded = json.loads(data)

        # Converts UTF-8 to ASCII
        self.injection_method("%s%s(%s)%s%s" % (
            decoded['user']['screen_name'],
            dataset.DATA_SEP,
            decoded['created_at'],
            dataset.DATA_SEP, #TODO tightly coupled here to the dataset class
            decoded['text'].replace('\n', ''))) #TODO find way to preserve newlines?
            #decoded['text'].encode('ascii', 'ignore')))
        return True

    def on_error(self, status):
        print (status)

##Singleton class for controlling the web streamer
class streamer :


    ##accepts initial hashtag (without #) as parameter
    def __init__(self,) :
        self.tstreamer = None
        self.data = None
        self.inject_data = None

    ##does what the name implies, stream must first be stopped however
    # returns true if successful
    def set_hashtag(self, hashtag) :
        if (not self.tstreamer) :
            self.data = dataset.dataset(hashtag)
            self.inject_data = self.data.get_injection_method()
            return True
        else :
            return False

    ##returns current hashtag that is set
    # returns none if there is none
    def get_hashtag(self) :
        if (self.data) :
            return self.data.hashtag
        else :
            return None

    ##return true if the streamer is currently running, false if otherwise
    def is_running(self) :
        if (self.tstreamer) :
            return True;
        else :
            return False

    ##starts the streamer, returns true if successful, false if otherwise
    # if it is not successful it means it is already running, or else you did not set
    # the hashtag with the set_hashtag method
    def start_streamer(self) :
        if (not self.tstreamer and self.data) :
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            self.tstreamer = Stream(auth, listener(lambda x : self.inject_data((x,)))) #my silly inject data method takes a list not a string . . . 
            self.tstreamer.filter(track=[self.data.hashtag], async=True)
            return True;
        else :
            return False;

    ##stops the streamer, if it returns false it means that it was not running
    # in the first place
    def stop_streamer(self) :
        if (self.tstreamer) :
            self.tstreamer.disconnect()
            self.tstreamer = None
            return True
        else :
            return False

driver = streamer()
#there! singelton by convention, only ever call this method!
def get_driver() :
    return driver

