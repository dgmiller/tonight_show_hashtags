##A filter to remove tweets that have things you can not say on television with them

import os
import re

def filter(dset) :

    tweet_text = dset.get_info('tweet')[0]

    badwords = [w.strip() for w in open(os.path.join(os.path.dirname(__file__), 'badwords.txt')).readlines()]

    for b in badwords :
        if re.match(r'.*\b' + b.replace(' ', r'\s*') + r'\b.*', tweet_text.lower()) :
            return False


    return True
