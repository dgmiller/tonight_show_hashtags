from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = 'IWSJe1TLJBvSOQyahRUrL6t13'
csecret = 'bnw4Trgd7y2zEGZ3kN8jbkaDQuArDfbIExEXPOoOeAm1BdG0rV'
atoken = '2331310884-rSIiYPVgCZROan1aBNmYWAyJYtggEDJy2NLzKJL'
asecret = 'PQl6pl6YLpBva22cpJVYwmk28m6NGOJgPleggzmWnYrad'

class listener(StreamListener):
    
    def on_data(self, data):
        tweet = data.split(',"text":"')[1].split('","source')[0]
        print tweet+'\n' + ('-' * 30)
        return True
        
    def on_error(self, status):
        print status
        
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#io15"])
