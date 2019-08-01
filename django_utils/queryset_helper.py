# start to python 3 support:
from __future__ import unicode_literals

'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python_utilities is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/python_utilities.  If not, see
<http://www.gnu.org/licenses/>.
'''

'''
queryset_generator and queryset_list_generator based on:
https://gist.github.com/897894

Going forward, this is the main class for QuerySet helper methods, etc.
Need to refactor QueryFilterHelper so it contains a nested instance of this
    class calls methods here, so we only have one class that does this.
'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python standard libraries
import gc
import logging

class QuerySetHelper():

    '''
    This class requires the django application.  It contains methods for using
       values in parameters to add filters to Django QuerySets
    '''

    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #---------------------------------------------------------------------------


    # names of parameters
    PARAM_ORDER_BY = "order_by"

    # more specific parameters - date params
    PARAM_DATE_COLUMN = "date_column"
    PARAM_START_DATE = "start_date"
    PARAM_END_DATE = "end_date"

    # default values
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"

    # param for primary key =
    PARAM_PRIMARY_KEY_LIST = "primary_key_list"


    #---------------------------------------------------------------------------
    # ! ==> __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        self.m_queryset = None        

    #-- END constructor --#


    #---------------------------------------------------------------------------
    # ! ==> properties, in alphabetical order
    #---------------------------------------------------------------------------


    def get_queryset( self ):
    
        '''
        Returns QuerySet stored in internal instance variable.
        ''' 
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_queryset
        
        return value_OUT
    
    #-- END get_queryset() --#


    def set_queryset( self, value_IN ):
    
        '''
        Accepts and stores QuerySet in internal instance variable.
        ''' 
        
        # return reference
        self.m_queryset = value_IN
    
    #-- END set_queryset() --#


    queryset = property( get_queryset, set_queryset )


    #---------------------------------------------------------------------------
    # ! ==> class methods, in alphabetical order
    #---------------------------------------------------------------------------


    @classmethod
    def is_queryset_evaluated( cls, queryset_IN, *args, **kwargs ):
    
        """
        Checks if queryset_IN._result_cache is None.  If None, not evaluated,
            returns False.  If not None, has been evaluated, returns true.
        """

        # return reference
        is_evaluated_OUT = None
        
        # declare variables
        
        # make sure QuerySet is not None
        if ( queryset_IN is not None ):
        
            # check if _result_cache is None
            if ( queryset_IN._result_cache is None ):
            
                # it is None - not yet evaluated
                is_evaluated_OUT = False
        
            else:
        
                # not None, so has been evaluated.
                is_evaluated_OUT = True
    
            #-- END check to see if _result_cache --#
            
        else:
        
            print( "ERROR - no QuerySet passed in ( {} )".format( queryset_IN ) )
            
        #-- END check to see if QuerySet passed in. --#
        
        return is_evaluated_OUT
                
    #-- END function is_queryset_evaluated() --#
    
    
    @classmethod
    def queryset_generator( cls, queryset_IN, chunksize_IN = 1000 ):
    
        """
        Iterate over a Django Queryset ordered by the primary key
        
        This method loads a maximum of chunksize (default: 1000) rows in it's
        memory at the same time while django normally would load all rows in it's
        memory. Using the iterator() method only causes it to not preload all the
        classes.
        
        Note that the implementation of the iterator does not support ordered query sets.
        
        Usage:
        
        my_queryset = QuerySetHelper.queryset_generator( MyItem.objects.all() )
        
        # loop as normal - no need to keep coming back for more chunks of 1000...
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
    
    
    @classmethod
    def queryset_list_generator( cls, queryset, listsize=10000, chunksize=1000):
    
        """
        Iterate over a Django Queryset ordered by the primary key and return a
        list of model objects of the size 'listsize'.
        This method loads a maximum of chunksize (default: 1000) rows in memory
        while django normally would load all rows into memory.  In contrast to
        the queryset_generator, it doesn't return each row on its own, but
        returns a list of listsize (default: 10000) rows at a time.
        
        Note that the implementation of the iterator does not support ordered
        query sets.
        """
        
        it = queryset_generator(queryset, chunksize)
        i = 0
        row_list = []

        for row in it:
            
            i += 1
            row_list.append(row)
            
            if i >= listsize:
                
                yield row_list
                i = 0
                row_list = []
                
            #-- END check to see if we have reached our list size --#
        
        #-- END loop over queryset iterator --#
        
    #-- END function queryset_list_generator() --#
    
        
    #---------------------------------------------------------------------------
    # ! ==> instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def add_date_filter( self, date_field_name_IN, start_date_IN, end_date_IN ):
    
        '''
        Accepts name of date field we want to filter, and optional start and end
           dates.  Depending on which date values are passed in, creates a date
           filter on column name in date_field_name_IN and appends it to the
           nested QuerySet, then updates the nested QuerySet instance so it
           points to the updated QuerySet and also returns the new QuerySet.
           
        Preconditions: assumes that there is a QuerySet nested in the instance.
        
        Postconditions: replaces existing QuerySet with newly filtered one at
           conclusion of execution.
           
        Parameters:
        - date_field_name_IN - String field name of date field we are filtering on.
        - start_date_IN - datetime.datetime instance that contains the start date and time from which we want to start filtering.  If empty, does not specify a start date.
        - end_date_IN - datetime.datetime instance that contains the end date and time at which we want to end filtering.  If empty, goes to present.           

        Returns:
        - QuerySet - updated QuerySet, also stored in the instance.
        '''
        
        # return reference
        queryset_OUT = None
        
        # Declare variables
        my_queryset = None
        
        # make sure we have a QuerySet.
        my_queryset = self.queryset
        
        # got a queryset?
        if ( my_queryset ):
            
            # make sure we have a field name and either a start or an end date.
            if ( ( date_field_name_IN ) and ( ( start_date_IN ) or ( end_date_IN ) ) ):
        
                # got both dates?
                if ( ( start_date_IN ) and ( end_date_IN ) ):
                
                    # yes - do a range.
                    #writeup_queryset = writeup_queryset.filter( createtime__range = ( start_date_IN, end_date_IN ) )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__range" ] = ( start_date_IN, end_date_IN )
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                elif ( start_date_IN ):
                
                    # just start date - do gte
                    #writeup_queryset = writeup_queryset.filter( createtime__gte = start_date_IN )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__gte" ] = start_date_IN
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                elif ( end_date_IN ):
                
                    # just end date - do lte
                    #writeup_queryset = writeup_queryset.filter( createtime__lte = end_date_IN )
                    filter_params = {}
                    filter_params[ date_field_name_IN + "__lte" ] = end_date_IN
                    my_queryset = my_queryset.filter( **filter_params )
                    
                    # store updated QuerySet
                    self.queryset = my_queryset
                    
                #-- END conditional over date range values.
                
            #-- END check to see if we have enough info. to filter. --#
        
        #-- END check to see if we have a queryset --#

        # return it also
        queryset_OUT = self.queryset
        
        return queryset_OUT
    
    #-- END add_date_filter() --#


    def add_pk_filter( self, primary_key_list_IN ):
    
        '''
        Accepts primary key value.  Adds filter condition to filter based on
           primary key list passed in.  If single value, adds "pk = ".  If list,
           adds "pk__in=[]" filter.
           
        Preconditions: assumes that there is a QuerySet nested in the instance.
        
        Postconditions: replaces existing QuerySet with newly filtered one at
           conclusion of execution.
           
        Parameters:
        - primary_key_list_IN - List of primary key values that we want to use to filter the nested QuerySet.  If empty list or None passed in, does nothing.

        Returns:
        - QuerySet - updated QuerySet, also stored in the instance.
        '''
        
        # return reference
        queryset_OUT = None
        
        # Declare variables
        my_queryset = None
        my_key_value = -1
        
        # make sure we have a QuerySet.
        my_queryset = self.queryset
        if ( my_queryset ):
        
            # Got a list?       
            if ( ( primary_key_list_IN ) and ( len( primary_key_list_IN ) > 0 ) ):
                
                # one key or more than one key?
                if ( len( primary_key_list_IN ) == 1 ):
                    
                    # just one.  Get value, add "pk = ".
                    my_key_value = primary_key_list_IN[ 0 ]
                    
                    my_queryset = my_queryset.filter( pk = my_key_value )
                    
                else:
                
                    # more than one.  Do "pk__in = "
                    my_queryset = my_queryset.filter( pk__in = primary_key_list_IN )
                    
                #-- END check to see if one or more than one ID. --#
            
                # only update nested QuerySet if we actually changed something.
                self.queryset = my_queryset
 
            #-- END check to see if we have enough info. to filter. --#
            
        #-- END check to make sure we have a QuerySet.
        
        # return it also
        queryset_OUT = self.queryset
        
        return queryset_OUT
    
    #-- END add_pk_filter() --#


    def configure_query_set( self, param_hash_IN ):
    
        '''
        Accepts a parameter hash that contains a QuerySet instance, an optional
           date column name and start and/or end date, and an optional order_by
           list.  Applies the filter, sort, and order by parameters to the
           QuerySet passed in, then returns the QuerySet.
        
        Params (stored in a param hash):
        - date_column_name_IN - String name of date column we want to filter on.
        - start_date_IN - datetime.datetime instance that contains the start date and time from which we want to start counting.  If empty, does not specify a start date.
        - end_date_IN - datetime.datetime instance that contains the end date and time at which we want to end counting.  If empty, goes to present.
        - order_by_IN - order_by items to pass to django order_by method.
        
        Returns:
        - QuerySet - QuerySet instance of writeups that fit parameters.
        '''
        
        # return reference
        value_OUT = -1
        
        # declare variables
        primary_key_list_IN = None
        date_column_name_IN = ""
        start_date_IN = None
        end_date_IN = None
        order_by_IN = None
        writeup_queryset = None
        filter_params = None
        
        # check for input parameters
        if ( param_hash_IN ):
        
            # got something.  See if there are parameters inside.
            # primary key list
            if ( QueryFilterHelper.PARAM_PRIMARY_KEY_LIST in param_hash_IN ):
            
                # we have a date column name.
                primary_key_list_IN = param_hash_IN[ QueryFilterHelper.PARAM_PRIMARY_KEY_LIST ]
                
            #-- END check to see if date column name --#            
            
            # date column
            if ( QueryFilterHelper.PARAM_DATE_COLUMN in param_hash_IN ):
            
                # we have a date column name.
                date_column_name_IN = param_hash_IN[ QueryFilterHelper.PARAM_DATE_COLUMN ]
                
            #-- END check to see if date column name --#
            
            # start date
            if ( QueryFilterHelper.PARAM_START_DATE in param_hash_IN ):
            
                # we have a start date.
                start_date_IN = param_hash_IN[ QueryFilterHelper.PARAM_START_DATE ]
                
            #-- END check for start date --#
        
            # end date.
            if ( QueryFilterHelper.PARAM_END_DATE in param_hash_IN ):
            
                # we have a end date.
                end_date_IN = param_hash_IN[ QueryFilterHelper.PARAM_END_DATE ]
                
            #-- END check for end date --#
            
            # order by
            if ( QueryFilterHelper.PARAM_ORDER_BY in param_hash_IN ):
                
                # we have an order-by list
                order_by_IN = param_hash_IN[ QueryFilterHelper.PARAM_ORDER_BY ]
                
            #-- END check for order by parameter --#

        #-- END check for input parameters --#
        
        # filter on start or end dates?
        self.add_date_filter( date_column_name_IN, start_date_IN, end_date_IN )
        
        # got a PK list?
        if ( primary_key_list_IN ):
            
            self.add_pk_filter( primary_key_list_IN )
            
        #-- END check to see if need to filter on primary key. --#
        
        # got an order_by?
        if ( order_by_IN ):
            
            # yes, we have one - process it.
            self.set_order_by( order_by_IN )
            
        #-- END check to see if we have an order by. --#
        
        # return query set.
        value_OUT = self.queryset
        
        return value_OUT        
    
    #-- END configure_query_set() method --#


    def is_evaluated( self, *args, **kwargs ):
    
        """
        Checks if queryset_IN._result_cache is None.  If None, not evaluated,
            returns False.  If not None, has been evaluated, returns true.
        """

        # return reference
        is_evaluated_OUT = None
        
        # declare variables
        my_queryset = None
        
        # make sure QuerySet is not None
        my_queryset = self.get_queryset()
        if ( my_queryset is not None ):
        
            # check if _result_cache is None
            is_evaluated_OUT = self.is_queryset_evaluated( my_queryset )

        else:
        
            print( "ERROR - no QuerySet ( {} )".format( my_queryset ) )
            
        #-- END check to see if QuerySet passed in. --#
        
        return is_evaluated_OUT
                
    #-- END function is_queryset_evaluated() --#
    
    
    def set_order_by( self, order_by_list_IN ):
    
        '''
        Accepts List of string order by directives that we want to place on the
           nested QuerySet.  Adds them in the order they are listed in the List.
           For more details, see:
           http://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
           If empty list or None passed in, clears out the order_by.
           
        Preconditions: assumes that there is a QuerySet nested in the instance.
        
        Postconditions: replaces existing QuerySet with newly ordered one at
           conclusion of execution.
           
        Parameters:
        - order_by_list_IN - List of string order by directives that we want to place on the nested QuerySet, in the order we want them.  If empty list or None passed in, clears out the order_by.

        Returns:
        - QuerySet - updated QuerySet, also stored in the instance.
        '''
        
        # return reference
        queryset_OUT = None
        
        # Declare variables
        my_queryset = None
        
        # make sure we have a QuerySet.
        my_queryset = self.queryset
        if ( my_queryset ):
        
            # Got a list?       
            if ( ( order_by_list_IN ) and ( len( order_by_list_IN ) > 0 ) ):
        
                # add the order_by values.
                my_queryset = my_queryset.order_by( *order_by_list_IN )
                
            else:
            
                # nothing passed in, so empty out order_by.
                my_queryset = my_queryset.order_by()
                    
            #-- END check to see if we have enough info. to filter. --#
            
            self.queryset = my_queryset
            
        #-- END check to make sure we have a QuerySet.
        
        # return it also
        queryset_OUT = self.queryset
        
        return queryset_OUT
    
    #-- END set_order_by() --#


#-- END class QuerySetHelper --#


def queryset_generator( queryset_IN, chunksize_IN = 1000 ):

    """
    Calls the class method of the same name in QuerySetHelper.  See that method
        for more documentation.
    """
    
    return QuerySetHelper.queryset_generator( queryset_IN, chunksize_IN )
            
#-- END function queryset_generator() --#


def queryset_list_generator(queryset, listsize=10000, chunksize=1000):

    """
    Calls the class method of the same name in QuerySetHelper.  See that method
        for more documentation.
    """
    
    return QuerySetHelper.queryset_list_generator( queryset, listsize, chunksize )
            
#-- END function queryset_list_generator() --#