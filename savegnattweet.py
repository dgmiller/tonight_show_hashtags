from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = 'IWSJe1TLJBvSOQyahRUrL6t13'
csecret = 'bnw4Trgd7y2zEGZ3kN8jbkaDQuArDfbIExEXPOoOeAm1BdG0rV'
atoken = '2331310884-rSIiYPVgCZROan1aBNmYWAyJYtggEDJy2NLzKJL'
asecret = 'PQl6pl6YLpBva22cpJVYwmk28m6NGOJgPleggzmWnYrad'

class listener(StreamListener):
    
    def on_data(self, data):
        try:
            print data
            saveFile = open('twitDB.csv','a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException, e:
            print 'failed ondata,',str(e)
            time.sleep(5)
        
    def on_error(self, status):
        print status
        
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#byutami"])



