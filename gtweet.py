from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import threading
import json
import csv

stopTime = "14:30"
Thursday = 2
wordSearch = "car"
csvFilename = "test.txt"

def main():
	threading.Timer(1, checkDateTime).start()
	twitterStream.filter(track=[wordSearch])

def checkDateTime():
    currentDay = datetime.datetime.now().weekday()
    currentTime = datetime.datetime.now().time().isoformat()[0:5]
    if currentDay == Thursday and currentTime == stopTime:
    	twitterStream.disconnect()
    	quit()
    else:
    	threading.Timer(1, checkDateTime).start()

ckey = 'IWSJe1TLJBvSOQyahRUrL6t13'
csecret = 'bnw4Trgd7y2zEGZ3kN8jbkaDQuArDfbIExEXPOoOeAm1BdG0rV'
atoken = '2331310884-rSIiYPVgCZROan1aBNmYWAyJYtggEDJy2NLzKJL'
asecret = 'PQl6pl6YLpBva22cpJVYwmk28m6NGOJgPleggzmWnYrad'

class listener(StreamListener):
    
    def on_data(self, data): # screen_name, created_at, timestamp_ms, in_reply_to_screen_name, text
        decoded = json.loads(data) # decoded is a dictionary
        name = str(decoded['user']['screen_name']) + ','
        create = str(decoded['created_at']) + '\n'
        try:
            print name + create
            outfile = open(csvFilename,'a')
            outfile.write(name)
            outfile.write(create)
            outfile.close()
            return True
        except BaseException, e:
            print 'failed ondata,',str(e)
            time.sleep(1)
       
        
    def on_error(self, status):
        print status
        
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
main()
