

def display(dset) :

    inverse = dset.invert_view()

    tweets = inverse.get_info("tweets")

    result = ""
    for t in tweets :

        result += t + '\n\n'


    return result
