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

class LoggingHelper( object ):

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
    m_logger_name = ""


    #============================================================================
    # Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # initialize variables
        self.m_logger = None
        self.m_logger_name = "python_utilities.logging.logging_helper"

    #-- END method __init__() --#


    #============================================================================
    # Instance methods
    #============================================================================


    def get_logger_name( self ):
    
        # return reference
        value_OUT = None
        
        # get value
        value_OUT = self.m_logger_name
                
        return value_OUT
    
    #-- END method get_logger_name --#

    
    def get_logger( self, logger_name_IN = "" ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        logger_name = ""
        logger_instance = None
        
        # get m_logger
        value_OUT = self.m_logger
        
        # got anything?
        if ( value_OUT is None ):
        
            # no.  Do we have an application string?
            if ( ( logger_name_IN is None ) or ( logger_name_IN == "" ) ):
            
                # no - see if there is one in instance.
                logger_name = self.get_logger_name()
            
            else:
            
                # yes - use it.
                logger_name = logger_name_IN
            
            #-- END check to see if app_name. --#
            
            #print( "logger name: " + logger_name )
            
            # make logger instance.
            if ( ( logger_name is None ) or ( logger_name == "" ) ):
            
                # no logger name.
                logger_instance = logging.getLogger()
                
            else:
            
                # there is a logger name.
                logger_instance = logging.getLogger( logger_name )
                
            #-- END check to see how we make a logger. --#
            
            # store the logger.
            self.set_logger( logger_instance )
            
            # get the logger.
            value_OUT = self.get_logger()
        
        #-- END check to see if logger initialized. --#
        
        return value_OUT
    
    #-- END method get_logger --#

    
    def set_logger_name( self, value_IN ):
        
        '''
        Accepts application name.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # store value.
        self.m_logger_name = value_IN
        
        # return it.
        value_OUT = self.get_logger_name()
        
        return value_OUT
        
    #-- END method set_logger_name() --#


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


#-- END class LoggingHelper --#