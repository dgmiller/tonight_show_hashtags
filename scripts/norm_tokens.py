from nltk.corpus import wordnet

##list of tokens normalized by wordnet.morphy
#TODO the actual tweets have characters with \\n\\n stuck on them, we should figure out a way to clean that

def meta (dset) :

    tokens = dset.get_info('get_tokens')

    result = []

    for t in tokens :
        buf = []

        for w in t :

            w = w.lower()

            morphed = wordnet.morphy(w)

            if (morphed) :
                buf.append(morphed)
            else :
                buf.append(w)

        result.append(buf)
        
    return result
