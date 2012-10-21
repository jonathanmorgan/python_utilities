'''
queryset_generator and queryset_list_generator based on:
https://gist.github.com/897894
'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python standard libraries
import gc
import logging

def queryset_generator( queryset_IN, chunksize_IN = 1000 ):

    """
    Iterate over a Django Queryset ordered by the primary key
    
    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    
    Note that the implementation of the iterator does not support ordered query sets.
    
    Usage:
    
    my_queryset = queryset_iterator( MyItem.objects.all() )
    for item in my_queryset:
        item.do_something()
    
    """
    
    # declare variables
    last_pk = -1
    queryset = None
    current_pk = -1
    
    # is queryset non-None, larger than 0?
    if ( ( queryset_IN ) and ( len( queryset_IN ) > 0 ) ):    

        # if query set
        # order queryset by primary key, descending, to get the largest ID value.
        last_pk = queryset_IN.order_by('-pk')[0].pk
        
        # order queryset by primary key, ascending.
        queryset = queryset_IN.order_by('pk')
        
        # get first pk number
        current_pk = queryset[0].pk
        
        # make sure the pk is less than or equal the last value (want this to
        #    work for the one-record case, just as well as it does for the
        #    gazillion-record case).
        if ( current_pk <= last_pk ):
        
            # subtract 1, so that we include this first pk, as well.
            current_pk = current_pk - 1
    
            # continue to return stuff while the next pk is less than the last.
            while current_pk < last_pk:
            
                # filter the original queryset, getting all greater than current 
                for row in queryset.filter( pk__gt = current_pk )[:chunksize_IN]:
                
                    # record current pk
                    current_pk = row.pk
                    
                    # yield current row
                    yield row
                    
                #-- END loop over this chunk --#
                
                # clear memory.
                gc.collect()
                
            #-- END loop over chunks --#
            
        #-- END check to make sure original first pk is less than or equal to last --#
            
    #-- END check to see if anything in queryset --#
            
#-- END function queryset_generator() --#


def queryset_list_generator(queryset, listsize=10000, chunksize=1000):

    """
    Iterate over a Django Queryset ordered by the primary key and return a
    list of model objects of the size 'listsize'.
    This method loads a maximum of chunksize (default: 1000) rows in it's memory
    at the same time while django normally would load all rows in it's memory.
    In contrast to the queryset_iterator, it doesn't return each row on its own,
    but returns a list of listsize (default: 10000) rows at a time.
    
    Note that the implementation of the iterator does not support ordered query sets.
    """
    
    it = queryset_iterator(queryset, chunksize)
    i = 0
    row_list = []
    for row in it:
        i += 1
        row_list.append(row)
        if i >= listsize:
            yield row_list
            i = 0
            row_list = []
            
#-- END function queryset_list_generator() --#