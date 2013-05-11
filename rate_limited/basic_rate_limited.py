'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/python_utilities.  If not, see
<http://www.gnu.org/licenses/>.
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# base python libraries
import time
import sys
import datetime

class BasicRateLimited( object ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "


    #============================================================================
    # instance variables
    #============================================================================


    # rate limiting
    do_manage_time = True
    rate_limit_in_seconds = 2
    request_start_time = None
    
    
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
        seconds_between_requests = -1
        request_start_dt = None
        current_dt = None
        difference_td = None
        difference_seconds = -1
        difference_microseconds = -1
        sleep_seconds = -1.0
        
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
        
        print( "In " + me + ": time elapsed = " + str( difference_seconds ) )

        # is difference greater than or equal to our second limit?
        if ( difference_seconds >= seconds_between_requests ):
        
            # yes - return True.
            value_OUT = True
            print( "In " + me + ": greater than " + str( seconds_between_requests ) + " seconds - OK to continue." )
            
        else:
            
            # no - subtract difference from 2.
            sleep_seconds = 2 - difference_seconds
            
            print( "In " + me + ": less than " + str( seconds_between_requests ) + " seconds - sleep for " + str( sleep_seconds ) + " seconds." )

            # sleep.
            time.sleep( sleep_seconds )
            
            # set value_OUT
            value_OUT = True
            
        #-- END check to see if we need to sleep. --#
        
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