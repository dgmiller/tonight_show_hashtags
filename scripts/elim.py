


def display(dset) :


    result = "\n\n"

    for f in ['1', '2', '3', '4', '5'] :

        total = dset.get_view(f).get_current_size()
        eliminated = total - dset.intersect_view(f).get_current_size()
        if (total != 0) :
            percent = (eliminated/total) * 100
        else :
            percent = 0

        result += "\t{} : {} eliminated out of {}; {:.0f}% \n".format(f, eliminated, total, percent)

    return result
