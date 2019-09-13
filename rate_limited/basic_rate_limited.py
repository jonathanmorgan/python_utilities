# start to support python 3:
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
Usage:

For a class you want to be rate-limited:

- have that class import and extend `BasicRateLimited`.

    # import
    from python_utilities.rate_limited.basic_rate_limited import BasicRateLimited
    
    # class definition
    def class SampleClass( BasicRateLimited ):

- in that class's `__init__()` method, call the parent `__init__()` method, then set instance variable `rate_limit_in_seconds` to the minimum number of seconds you want between requests (can be a decimal).

    def __init__( self ):

        # call parent's __init__()
        super( ContextTextBase, self ).__init__()

        # declare variables
        
        # limit to no more than 4 per second
        self.rate_limit_in_seconds = 0.25
        
    #-- END method __init__() --#

- At the start of each transaction, call the `self.start_request()` method to let the code know you're starting a request.
- Once the request is done, call `continue_collecting = self.may_i_continue()` this method will block if you have to wait, will return true if it is OK to continue, will return False if some error occurred.
- In your control structure, always check the result of `may_i_continue()` before continuing.
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# base python libraries
import datetime
import sys
import time

# python utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper
# which extends: from python_utilities.logging.logging_helper import LoggingHelper

# object --> LoggingHelper --> ExceptionHelper --> BasicRateLimited
class BasicRateLimited( ExceptionHelper ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "


    #============================================================================
    # class variables
    #============================================================================


    # rate limiting - moved to __init__()
    #do_manage_time = True
    #rate_limit_in_seconds = 2
    #rate_limit_daily_limit = -1
    #request_start_time = None
    
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( BasicRateLimited, self ).__init__()

        # declare variables

        # rate limiting
        self.do_manage_time = True
        self.rate_limit_in_seconds = 2
        self.rate_limit_daily_limit = -1
        self.request_start_time = None

        # set logger name (for Logger parent class: (LoggingHelper -->
        #    BasicRateLimited).
        self.set_logger_name( "python_utilities.rate_limited.basic_rate_limited" )

    #-- END method __init__() --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def may_i_continue( self, last_transaction_dt_IN = None, *args, **kwargs ):
    
        '''
        Accepts the last datetime.datetime of a transaction to reddit.  Compares
           that to datetime.datetime.now().  If the difference is greater than
           2 seconds, then returns True.  If not, waits the time between the
           difference and 2 seconds and returns True.  Can't think of a reason to
           return False at the moment, but perhaps, in the future, this could be
           a semaphore, and so processes could loop waiting for True.
           
        Eventually, will change processing based on the value in do_manage_time -
           if True, assume we are the only process.  If False, check a separate
           ok_to_proceed flag, set by external manager, and only return True when
           that flag has been set on this instance.
           
        Note: this will fail if interval between request and now() is exactly 24
           hours (not checking day at the moment, just seconds and microseconds).
        ''' 
        
        # return reference
        value_OUT = False
        
        # declare variables
        me = "may_i_continue"
        my_logger = None
        am_i_managing_time = False
        seconds_between_requests = -1
        request_start_dt = None
        current_dt = None
        difference_td = None
        difference_seconds = -1
        difference_microseconds = -1
        sleep_seconds = -1.0
        
        # get logger.
        my_logger = self.get_logger()
        
        # first, check to see if do_manage_time is True.  If not, return True.
        am_i_managing_time = self.do_manage_time
        if ( am_i_managing_time == True ):
        
            # get rate limit - default is 2
            seconds_between_requests = self.rate_limit_in_seconds
            
            request_start_dt = self.request_start_time
            
            # do we have a nested start datetime?
            if ( request_start_dt == None ):
            
                # no - check argument.
                if ( ( last_transaction_dt_IN ) and ( last_transaction_dt_IN != None ) ):
                
                    # yes.  Use it.
                    request_start_dt = last_transaction_dt_IN
                    
                else:
                
                    # no - just grab now().
                    request_start_dt = datetime.datetime.now()
                    
                #-- END check to see if we have a datetime passed in. --#
                
            #-- END check to see if we have a nested request start time --#
                
            # get current date time.
            current_dt = datetime.datetime.now()
            
            # date math - substract current from last_request.
            difference_td = current_dt - request_start_dt
            
            # get difference in seconds
            difference_seconds = difference_td.seconds
            difference_microseconds = difference_td.microseconds
            
            # convert microseconds to seconds (divide by 1,000,000), add to
            #    difference_seconds.
            difference_seconds = difference_seconds + ( difference_microseconds / 1000000.0 )
            
            my_logger.info( "In " + me + ": time elapsed = " + str( difference_seconds ) )
    
            # is difference greater than or equal to our second limit?
            if ( difference_seconds >= seconds_between_requests ):
            
                # yes - return True.
                value_OUT = True
                my_logger.info( "In " + me + ": greater than " + str( seconds_between_requests ) + " seconds - OK to continue." )
                
            else:
                
                # no - subtract difference from seconds we need between requests.
                sleep_seconds = seconds_between_requests - difference_seconds
                
                my_logger.info( "In " + me + ": less than " + str( seconds_between_requests ) + " seconds - sleep for " + str( sleep_seconds ) + " seconds." )
    
                # sleep.
                time.sleep( sleep_seconds )
                
                # set value_OUT
                value_OUT = True
                
            #-- END check to see if we need to sleep. --#
            
        else:
        
            # flag to manage time is False - fine to continue anytime!
            value_OUT = True
            
        #-- END check to see if we are managing time. --#
        
        return value_OUT
    
    #-- END may_i_continue() --#
    
    
    def start_request( self, *args, **kwargs ):
    
        '''
        No parameters.  When invoked, stores the current date and time inside
           this instance as the request_start_dt, for use in subsequent call
           to may_i_continue(), to see if we are OK to continue.
        ''' 
        
        # store current date and time.
        self.request_start_time = datetime.datetime.now()
    
    #-- END start_request() --#


#-- END class BasicRateLimited. --#