# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2014 Jonathan Morgan

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

# imports

# python standard libraries
import datetime
import pprint
import six

# python_utilities
from python_utilities.dictionaries.dict_helper import DictHelper

class SummaryHelper( object ):

    '''
    This class encapsulates code for summarizing the details of a program's
       execution, including start and finish time, duration, and keeping track of
       counters that are incremented during execution.  Includes method to output
       a summary at the end, as a string, that can either be printed or logged.
    '''


    #============================================================================
    # Constants-ish
    #============================================================================


    # status constants
    STATUS_SUCCESS = "Success!"
    
    # standard labels
    LABEL_START_DT = "start_dt"
    LABEL_STOP_DT = "stop_dt"
    LABEL_DURATION_TD = "duration_td"
    
    # standard description text.
    DESC_START_DT = "Start time"
    DESC_STOP_DT = "End time"
    DESC_DURATION_TD = "Duration"
    
    # list of standard properties.
    STANDARD_PROP_LIST = [ LABEL_START_DT, LABEL_STOP_DT, LABEL_DURATION_TD ]


    #============================================================================
    # Instance variables
    #============================================================================


    # all properties are stored in dictionaries.  There is also an optional
    #    description dictionary, for use in outputting.
    m_prop_value_dict = {}
    m_prop_desc_dict = {}
    m_summary_string = ""


    #============================================================================
    # Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # initialize maps.
        self.m_prop_value_dict = {}
        self.m_prop_desc_dict = {}
        
        # initialize start_dt to now, end_dt and duration_td to None.
        self.set_start_time()
        self.set_prop_value( self.LABEL_STOP_DT, None )
        self.set_prop_value( self.LABEL_DURATION_TD, None )
        
        # add desc for start and stop times and duration.
        self.set_prop_desc( self.LABEL_START_DT, self.DESC_START_DT )
        self.set_prop_desc( self.LABEL_STOP_DT, self.DESC_STOP_DT )
        self.set_prop_desc( self.LABEL_DURATION_TD, self.DESC_DURATION_TD )
        
        # set summary string to empty string.
        self.m_summary_string = ""
        
    #-- END method __init__() --#


    #============================================================================
    # Instance methods
    #============================================================================


    def calculate_duration( self, *args, **kwargs ):
        
        '''
        Retrieves start and stop times from property map.  If start is missing,
           returns None.  If stop is missing, sets it to now, then uses that
           value.  subtracts start from stop to get a python timedelta, stores
           that in LABEL_DURATION_TD, and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_start_dt = None
        my_stop_dt = None
        my_duration_td = None
        
        # get start and stop.
        my_start_dt = self.get_prop_value( self.LABEL_START_DT )
        my_stop_dt = self.get_prop_value( self.LABEL_STOP_DT )
        
        # got a start time?
        if( ( my_start_dt ) and ( my_start_dt != None ) ):
        
            # yes.  Do we have a stop time?
            if ( ( my_stop_dt == None ) or ( type( my_stop_dt ) != datetime.datetime ) ):
            
                # no - set to now().
                my_stop_dt = self.set_stop_time()
                
            #-- END check to see if stop_dt present. --#
            
            # calculate difference.
            my_duration_td = my_stop_dt - my_start_dt
            
            # store it and set return value.
            value_OUT = self.set_prop_value( self.LABEL_DURATION_TD, my_duration_td )
            
        else:
        
            # no start time.  Return none.
            value_OUT = None
            
        #-- END check to see if start time. --#
        
        return value_OUT        
        
    #-- END method calculate_duration() --#


    def create_summary_string( self, item_prefix_IN = "- ", newline_IN = "\n", *args, **kwargs ):
        
        '''
        Accepts prefix and newline values.  Defaults to prefixing with hyphen,
           using "\n" for newline.  Loops over all properties in props dict.  For
           each, converts to string using str(), then looks for description text.
           Outputs name or desc and value for each to a string followed by the
           newline value.  Alwways concludes with start, stop time and duration.
           Stores string in m_summary_string, then returns summary string.
           
        Parameters:
        - item_prefix_IN - string item prefix.  Defaults to "- ".
        - newline_IN - string to put at the end of each line.  Defaults to "\n".
        '''
        
        # return reference
        value_OUT = ""
        
        # declare variables
        my_prop_dict = None
        my_desc_dict = None
        current_name = ""
        current_value = None
        current_desc = ""
        
        # get dictionaries
        my_prop_dict = self.m_prop_value_dict
        my_desc_dict = self.m_prop_desc_dict
        
        # loop over items in property dictionary.
        for current_name, current_value in my_prop_dict.items():
        
            # make sure this isn't one of our special properties.
            if ( current_name not in self.STANDARD_PROP_LIST ):
            
                # get description text.  Default to prop name.
                current_desc = self.get_prop_desc( current_name, current_name )
                
                # add to summary string.
                value_OUT += item_prefix_IN + current_desc + ": " + str( current_value ) + newline_IN
            
            #-- END check to limit to non-standard properties. --#
        
        #-- END loop over properties. --#
        
        # output standard properties.
        for current_name in self.STANDARD_PROP_LIST:
        
            # get value
            current_value = self.get_prop_value( current_name )
            
            # get description text.  Default to prop name.
            current_desc = self.get_prop_desc( current_name, current_name )
            
            # add to summary string.
            value_OUT += item_prefix_IN + current_desc + ": " + str( current_value ) + newline_IN
            
        #-- END loop over standard properties. --#
        
        # store off the summary string
        self.m_summary_string = value_OUT
        
        return value_OUT        
        
    #-- END method create_summary_string() --#


    def get_prop_desc( self, name_IN, default_IN = "", *args, **kwargs ):
    
        # return reference
        value_OUT = ""
        
        # use DictHelper
        value_OUT = DictHelper.get_dict_value( self.m_prop_desc_dict, name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_prop_desc --#

    
    def get_prop_value( self, name_IN, default_IN = None, *args, **kwargs ):
    
        # return reference
        value_OUT = None
        
        # use DictHelper
        value_OUT = DictHelper.get_dict_value( self.m_prop_value_dict, name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_prop_value --#

    
    def get_summary_string( self, *args, **kwargs ):
    
        # return reference
        value_OUT = ""
        
        # use DictHelper
        value_OUT = self.m_summary_string
        
        return value_OUT
    
    #-- END method get_summary_string --#

    
    def increment_prop_value( self, name_IN, value_IN = 1, *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as int, adds value_IN to it, then stores and
           returns the result.
        '''
        
        # return reference
        value_OUT = None
        
        # use DictHelper
        value_OUT = DictHelper.increment_int_dict_value( self.m_prop_value_dict, name_IN, value_IN )
        
        return value_OUT
        
    #-- END method increment_prop_value() --#


    def set_prop_desc( self, name_IN, value_IN, *args, **kwargs ):
        
        '''
        Accepts name, and value.  Stores value in our prop desc map, associated
           with the name passed in.  Returns the value.
        '''
        
        # return reference
        value_OUT = None
        
        # use DictHelper
        value_OUT = DictHelper.set_dict_value( self.m_prop_desc_dict, name_IN, value_IN )
        
        return value_OUT
        
    #-- END method set_prop_desc() --#


    def set_prop_value( self, name_IN, value_IN, *args, **kwargs ):
        
        '''
        Accepts name, and value.  Stores value in our prop value map, associated
           with the name passed in.  Returns the value.
        '''
        
        # return reference
        value_OUT = None
        
        # use DictHelper
        value_OUT = DictHelper.set_dict_value( self.m_prop_value_dict, name_IN, value_IN )
        
        return value_OUT
        
    #-- END method set_prop_value() --#


    def set_start_time( self, value_IN = None, *args, **kwargs ):
        
        '''
        Accepts optional start time datetime value.  Defaults to now() if no
           value passed in.  Stores start datetime.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_start_time = None
        
        # got a Date?
        if ( ( value_IN != None ) and ( type( value_IN ) == datetime.datetime ) ):

            # yes.  Use it.
            my_start_time = value_IN
        
        else:
        
            # no.  now.
            my_start_time = datetime.datetime.now()
        
        #-- END check for date passed in --#
        
        # use internal method
        value_OUT = self.set_prop_value( self.LABEL_START_DT, my_start_time )
        
        return value_OUT        
        
    #-- END method set_start_time() --#


    def set_stop_time( self, value_IN = None, *args, **kwargs ):
        
        '''
        Accepts optional stop time datetime value.  Defaults to now() if no
           value passed in.  Stores stop datetime.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_stop_time = None
        my_duration_td = None
        
        # got a Date?
        if ( ( value_IN != None ) and ( type( value_IN ) == datetime.datetime ) ):

            # yes.  Use it.
            my_stop_time = value_IN
        
        else:
        
            # no.  now.
            my_stop_time = datetime.datetime.now()
        
        #-- END check for date passed in --#
        
        # use internal method
        value_OUT = self.set_prop_value( self.LABEL_STOP_DT, my_stop_time )
        
        # calculate duration
        my_duration_td = self.calculate_duration()
        
        return value_OUT        
        
    #-- END method set_stop_time() --#


#-- END class SummaryHelper --#