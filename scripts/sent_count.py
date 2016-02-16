##this counts the number of sentences in a tweet



def meta (dset) :

    tokens = dset.get_info('get_tokens') #The tokenizer already accounts for cases like abbreviations and ellipses

    result = []
    for t in tokens :

        result.append(len([w for w in t if w == '.' ])) #Fancy way to add up all of the elements that are a period


    return result


def filter(dset) :

    count = dset.get_info('sent_count') 

    if count[0] > 3 :
        return False
    else :
        return True
