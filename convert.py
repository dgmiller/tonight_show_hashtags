# This is a file that should read and convert JSON data.

import json

data = open("raw_tweets.json", 'r')
print data.read()
data.close()