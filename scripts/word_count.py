import builtins

def meta(dset) :

    pos = dset.get_info('pos')


    result = []
    for p in pos :
        result.append(len(list(builtins.filter(lambda x: x != ',', p))))

    return result

#TODO yeah that was a pretty big oversight I guess, I should probably fix the whole filter thing shouldn't I?

def filter(dset) :
    count = dset.get_info('word_count')

    if count[0] <= 10 :  #It returns a list of size one! careful about that, it can cause some odd bugs if you forget
        return False
    
    else :
        return True
