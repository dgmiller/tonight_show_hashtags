


def display(dset) :


    sort_lengths = [];
    for i in range(1,6) :

        sort_lengths.append(len(dset.get_view(str(i)).get_info('tweet')))



    total_sorted = sum(sort_lengths)

    total_to_sort = len(dset.get_view('RT').intersect_view('clean').get_info('tweet'))

    remaining = total_to_sort - total_sorted


    result = '''
    
    Total Sorted : {} 
    Remaining : {} 

    1 : {}
    2 : {}
    3 : {}
    4 : {}
    5 : {} 
    '''.format(total_sorted, remaining, sort_lengths[0], sort_lengths[1], sort_lengths[2], sort_lengths[3], sort_lengths[4])


    return result


