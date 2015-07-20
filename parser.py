# this parses the text data and graphs trends etc.

with open('soccer.txt', 'r') as f:
    data = f.readlines()

a = len(data)

alltweets = open('july15.txt', 'a')
problems = []
for x in range(a):
    try:
        tweet = data[x].split(',', 3)
        text = tweet[3]
        alltweets.write(text)
    except:
        problems.append(x)
alltweets.close()

with open('july15.txt', 'r') as t:
    tweets = t.readlines()

b = len(tweets)
c = 0
for n in range(0, b):
    d = len(tweets[n])
    c += d

print "Number of tweets:", b
print "Average characters / tweet:", c / b


