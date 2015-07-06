import re
from re import sub
import cookielib
from cookielib import CookieJar
import urllib2
from urllib2 import urlopen

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

keyWord = 'obama'
startingLink = 'https://twitter.com/search/realtime?q='



def main():
    
    try:
        sourceCode = opener.open('https://twitter.com/search/realtime?q='+keyWord+'&src=hash').read()
        print sourceCode
    
    except, Exception, e:
        print str(e)
        print 'errored in the main try'
        time.sleep(555)
        
main()