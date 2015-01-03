# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2015 Jonathan Morgan

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
    Either make and store an instance of this in a class, or extend it.
'''

# imports

# python standard libraries
import logging

class Logger( object ):

    '''
    This class encapsulates code for making, storing, and interacting with the
       standard python logging library.  It is very basic to start.  It is not
       intended to replace the logger that you get from logging.getLogger().  It
       is more an interface to programmatic configuration and use of logging.
    '''


    #============================================================================
    # Constants-ish
    #============================================================================


    #============================================================================
    # Instance variables
    #============================================================================


    # all properties are stored in dictionaries.  There is also an optional
    #    description dictionary, for use in outputting.
    m_logger = None
    m_application_name = ""


    #============================================================================
    # Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # initialize variables
        self.m_logger = None
        self.m_application_name = ""

    #-- END method __init__() --#


    #============================================================================
    # Instance methods
    #============================================================================


    def get_application_name( self ):
    
        # return reference
        value_OUT = None
        
        # get m_application_name
        value_OUT = self.m_application_name
                
        return value_OUT
    
    #-- END method get_application_name --#

    
    def get_logger( self, application_name_IN = "" ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        app_name = ""
        logger_instance = None
        
        # get m_logger
        value_OUT = self.m_logger
        
        # got anything?
        if ( value_OUT is None ):
        
            # no.  Do we have an application string?
            app_name = application_name_IN
            if ( ( app_name is None ) or ( app_name == "" ) ):
            
                # no - see if there is one in instance.
                app_name = self.get_application_name()
            
            #-- END check to see if app_name. --#
            
            # make logger instance.
            if ( ( app_name is None ) or ( app_name == "" ) ):
            
                # no app name.
                logger_instance = logging.getLogger()
                
            else:
            
                # there is an app name.
                logger_instance = logging.getLogger( app_name )
                
            #-- END check to see how we make a logger. --#
            
            # store the logger.
            self.set_logger( logger_instance )
            
            # get the logger.
            value_OUT = self.get_logger()
        
        #-- END check to see if logger initialized. --#
        
        return value_OUT
    
    #-- END method get_logger --#

    
    def set_logger( self, instance_IN ):
        
        '''
        Accepts logger.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store logger.
        self.m_logger = instance_IN
        
        # return it.
        value_OUT = self.m_logger
        
        return value_OUT
        
    #-- END method set_logger() --#


#-- END class Logger --#