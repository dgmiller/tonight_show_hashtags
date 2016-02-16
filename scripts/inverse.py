

def display(dset) :

    chosen = ''

    for i in ['1', '2', '3', '4', '5'] :

        if dset.intersect_view(i).get_current_size() > 0 :
            chosen = i


    if chosen == '' :
        return "invalid filters"


    inverse = dset.invert_view()

    inverse = inverse.intersect_view('RT')
    inverse = inverse.intersect_view('clean')
    inverse = inverse.intersect_view(chosen)

    tweets = inverse.get_info("tweet")

    result = ""
    for t in tweets :

        result += t + '\n\n'


    return result
