from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import threading
import json
import csv

stopTime = "21:30"
Thursday = 3
wordSearch = "car"
csvFilename = "car.csv"
csvFilenameFiltered = "carFiltered.csv"
profanityArray = open("BadWords.txt", "r").read().split('\n')

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

def saveToFile(fileData, filter):
	outfile = open(csvFilename,'a')
	outfile.write(fileData)
	outfile.close()
	if not filter:
	    outfile = open(csvFilenameFiltered,'a')
	    outfile.write(fileData)
	    outfile.close()
	
def hasProfanity(profaneData):
    profaneData = profaneData.lower()
    for currentWord in profanityArray:
        if currentWord in profaneData:
            return True
    return False

ckey = 'IWSJe1TLJBvSOQyahRUrL6t13'
csecret = 'bnw4Trgd7y2zEGZ3kN8jbkaDQuArDfbIExEXPOoOeAm1BdG0rV'
atoken = '2331310884-rSIiYPVgCZROan1aBNmYWAyJYtggEDJy2NLzKJL'
asecret = 'PQl6pl6YLpBva22cpJVYwmk28m6NGOJgPleggzmWnYrad'

class listener(StreamListener):
    
    def on_data(self, data): # screen_name, created_at, timestamp_ms, text
        decoded = json.loads(data) # decoded is a dictionary
        isRetweet = 'retweeted_status' in decoded
    
        name = '@' + str(decoded['user']['screen_name']).replace(',','|').replace('\n',' ') + ','
        create = str(decoded['created_at']).replace(' +0000', '').replace(',','|').replace('\n',' ') + ','
        timestamp = str(decoded['timestamp_ms']).replace(',','|').replace('\n',' ') + ','
        text = str(decoded['text'].encode('utf-8')).replace(',','|').replace('\n',' ') + '\n'
        try:
            print name + create
            finishedText = name + create + timestamp + text
            saveToFile(finishedText, isRetweet or hasProfanity(finishedText))
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
