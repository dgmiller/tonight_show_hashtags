import string
import csv
import datetime
from itertools import izip
import plotly.plotly as py
from plotly.graph_objs import *

newlist = []
with open('july15_dates_only.csv','rU') as f:
	for line in f:
		newlist.append(line)

datetimes = []
for item in newlist:
	item = item.replace(" ","")
	item = item.replace("+00002015\n","")
	item = item.replace("WedJul","")
	item = item.replace("ThuJul","")
	item = item.replace("FriJul","")
	item = item.replace(":","")
	item = item[:-2]
	item = int(item)
	datetimes.append(item)
		
counts = []	
timeperiod = []
	
def countTweets(start,stop):
	while (start - 2400)%10000 != 0:
		numtweets = 0
		for x in range(start,stop):
			numtweets += datetimes.count(x)
		counts.append(numtweets)
		timeperiod.append([start,stop])
		if start == 170315:
			break
		if (start - 45) % 100 == 0:
			start += 55
			stop += 15
		elif (stop - 45) % 100 == 0:
			start += 15
			stop += 55
		else:
			start += 15
			stop += 15
		
countTweets(151930,151945)
countTweets(160000,160015)
countTweets(170000,170015)

times = []
startdate = datetime.datetime(2015,7,15)
starttime = startdate.replace(hour=13,minute=30)
for x in range(0,128):
	times.append(str(starttime))
	starttime += datetime.timedelta(minutes=15)

#trace1 = Scatter(
#	x = times,
#	y = counts,
#	fill = 'tozeroy'
#)
#data = Data([trace1])
#plot_url = py.plot(data, filename='coolgraph')

with open("times.csv",'wb') as f:
	writer = csv.writer(f)
	writer.writerows(izip(times,counts))

	




