# start to python 3 support:
from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

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

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper

class DjangoViewHelper( object ):
    

    #============================================================================
    # Constants-ish
    #============================================================================


    DEBUG = False
    LOGGER_NAME = "python_utilities.django_utils.django_view_helper"


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def get_request_data( cls, request_IN ):
    
        '''
        Accepts django request.  Based on method, grabs the container for incoming
            parameters and returns it:
            - for method "POST", returns request_IN.POST
            - for method "GET", returns request_IN.GET
        '''
        
        # return reference
        request_data_OUT = None
    
        # do we have input parameters?
        if ( request_IN.method == 'POST' ):
    
            request_data_OUT = request_IN.POST
            
        elif ( request_IN.method == 'GET' ):
        
            request_data_OUT = request_IN.GET
            
        #-- END check to see request type so we initialize form correctly. --#
        
        return request_data_OUT
        
    #-- END function get_request_data() --#


    @classmethod
    def output_debug( cls, message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "", debug_flag_IN = None ):
        
        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''
        
        # declare variables
        my_debug_flag = False
        my_logger_name = ""
        
        if ( debug_flag_IN is None ):
        
            my_debug_flag = cls.DEBUG
            
        else:
        
            my_debug_flag = debug_flag_IN
        
        #-- END check to see if debug flag. --#
    
        # only print if debug is on.
        if ( my_debug_flag == True ):
        
            # got a logger name?
            my_logger_name = cls.LOGGER_NAME
            if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
            
                # use logger name passed in.
                my_logger_name = logger_name_IN
                
            #-- END check to see if logger name --#

            # call method in LoggingHelper.
            LoggingHelper.output_debug( message_IN,
                                        method_IN = method_IN,
                                        indent_with_IN = indent_with_IN,
                                        logger_name_IN = my_logger_name )
        
        #-- END check to see if debug is on --#
    
    #-- END method output_debug() --#

#-- END class DjangoViewHelper --#