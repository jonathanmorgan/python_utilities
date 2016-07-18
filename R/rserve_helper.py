# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

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

'''
Usage:
    Either make and store an instance of this in a class, or extend it.

More detailed documentation on using pyRserve:
- https://pythonhosted.org/pyRserve/manual.html

================================================================================
Code Sample:
================================================================================

# imports
import numpy
from python_utilities.R.rserve_helper import RserveHelper

# make instance (could also inherit from this class).
rserve_helper = RserveHelper()

# set connection properties, if desired
# rserve_helper.rserve_host = "localhost" # sometimes need this for windows.
# rserve_helper.rserve_port = 12345

# get connection
my_rserve_connection = rserve_helper.get_rserve_connection()

# initialize libraries you want to use in your session.
my_rserve_connection.eval( "library( irr )" )

# garbage data - two rows of 100 "1"s.
value_array = numpy.ones( ( 2, 100 ) )

# transpose for the function we are calling.
value_array_wide = numpy.transpose( value_array )

# R - store values in R.
my_rserve_connection.r.valueArrayWide = value_array_wide

# R - call irr::kripp.alpha()
kripp_alpha_result = my_rserve_connection.eval( "irr::kripp.alpha( valueArrayWide, method = \"nominal\" )" )
#print( str( kripp_alpha_result ) )
                    
# get alpha value from result.
R_kripp_alpha = kripp_alpha_result[ str( "value" ) ]

'''

# imports
import pyRserve

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.logging.logging_helper import LoggingHelper

class RserveHelper( ExceptionHelper ):

    '''
    This class encapsulates code for making, storing, and interacting with an R
        server running the Rserve add-on.
    '''


    #============================================================================
    # Constants-ish
    #============================================================================


    # logging
    LOGGER_NAME = "python_utilities.R.rserve_helper.RserveHelper"
    
    # Rserve connection information
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 6311


    #============================================================================
    # NOT Instance variables
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #============================================================================


    # all properties are stored in dictionaries.  There is also an optional
    #    description dictionary, for use in outputting.
    #m_logger = None
    #m_logger_name = ""


    #============================================================================
    # Class methods
    #============================================================================


    @classmethod
    def clean_up_rserve_connection( cls, connection_IN, do_shutdown_server_IN = False ):
    
        # declare variables

        # shutdown server?
        if ( do_shutdown_server_IN == True ):
        
            # yes.
            connection_IN.shutdown()
            
        #-- END check to see if we shutdown server. --#

        # close connection.
        connection_IN.close()
        
    #-- END class method clean_up_rserve_connection() --#    


    @classmethod
    def create_rserve_connection( cls, host_IN = None, port_IN = None ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        got_host = False
        my_host = ""
        got_port = False
        my_port = -1

        # make Rserve Connection instance.
        
        # got a host?
        if ( ( host_IN is not None ) and ( host_IN != "" ) ):
        
            # yes
            my_host = host_IN
            got_host = True
            
        else:
        
            # no
            my_host = cls.DEFAULT_HOST
            got_host = False
            
        #-- END check to see if we have a host. --#

        # got a port?
        if ( ( port_IN is not None ) and ( port_IN != "" ) and ( port_IN > 0 ) ):
        
            # yes
            my_port = port_IN
            got_port = True
            
        else:
        
            # no
            my_port = cls.DEFAULT_PORT
            got_port = False
            
        #-- END check to see if we have a host. --#
        
        # do we have either a host or a port?
        if ( ( got_host == True ) or ( got_port == True ) ):
        
            # we do.  Include in connect() call.
            value_OUT = pyRserve.connect( host = my_host, port = my_port )
            
        else:
        
            # no.  Just call connect().
            value_OUT = pyRserve.connect()
            
        #-- END check to see if host or port. --#
        
        return value_OUT
    
    #-- END class method create_rserve_connection() --#    


    #============================================================================
    # Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # call parent __init__()
        super( RserveHelper, self ).__init__()
        
        # logging
        self.set_logger_name( self.LOGGER_NAME )
        
        # initialize variables
        self.rserve_connection = None
        self.rserve_host = ""
        self.rserve_port = ""

    #-- END method __init__() --#


    #============================================================================
    # Instance methods
    #============================================================================


    def close_rserve_connection( self ):
    
        # declare variables
        my_connection = None
    
        # get connection
        my_connection = self.get_rserve_connection()
    
        # don't remove, just clean up.  This lets us re-connect later.
        self.clean_up_rserve_connection( my_connection, do_shutdown_server_IN = False )
        
    #-- END method close_rserve_connection() --#

    
    def clear_rserve_connection( self, do_shutdown_server_IN = False ):
    
        # declare variables
        my_connection = None
    
        # get connection
        my_connection = self.get_rserve_connection()
    
        # clean up.
        self.clean_up_rserve_connection( my_connection, do_shutdown_server_IN = do_shutdown_server_IN )
        
        # None out the connection holder.
        self.set_rserve_connection( None )
        
    #-- END method clear_rserve_connection() --#

    
    def get_rserve_connection( self ):
    
        # return reference
        instance_OUT = None
        
        # declare variables
        my_host = ""
        my_port = -1
        rserve_connection_instance = None
        is_connection_closed = False
        
        # get m_logger
        value_OUT = self.rserve_connection
        
        # got anything?
        if ( value_OUT is None ):
        
            # no.  Do we have a host string?
            my_host = self.get_rserve_host()
            if ( ( my_host is None ) or ( my_host == "" ) ):
            
                # no - set to None
                my_host = None            

            #-- END check to see if host. --#
            
            # And do we have a port?
            my_port = self.get_rserve_port()
            if ( ( my_port is None ) or ( my_port == "" ) or ( my_port <= 0 ) ):
            
                # no - set to None
                my_port = None            

            #-- END check to see if port. --#
            
            # make a connection instance.
            rserve_connection_instance = self.create_rserve_connection( my_host, my_port )
            
            # store the connection.
            self.set_rserve_connection( rserve_connection_instance )
            
            # get the connection (sanity check).
            value_OUT = self.get_rserve_connection()
        
        else:
        
            # yes.  Is it open?
            is_connection_closed = value_OUT.isClosed
            if ( is_connection_closed == True ):
            
                # closed - re-open (connect() uses previous properties).
                value_OUT.connect()
                
            #-- END check to see if connection is closed. --#
        
        #-- END check to see if connection already initialized. --#
        
        return value_OUT
    
    #-- END method get_rserve_connection --#

    
    def get_rserve_host( self ):
    
        # return reference
        value_OUT = None
        
        # get value
        value_OUT = self.rserve_host
                
        return value_OUT
    
    #-- END method get_rserve_host --#

    
    def get_rserve_port( self ):
    
        # return reference
        value_OUT = None
        
        # get value
        value_OUT = self.rserve_port
                
        return value_OUT
    
    #-- END method get_rserve_port --#

    
    def set_rserve_connection( self, instance_IN ):
        
        '''
        Accepts pyRserve connection instance.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store logger.
        self.rserve_connection = instance_IN
        
        # return it.
        value_OUT = self.rserve_connection
        
        return value_OUT
        
    #-- END method set_rserve_connection() --#


    def set_rserve_host( self, value_IN ):
        
        '''
        Accepts application name.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # store value.
        self.rserve_host = value_IN
        
        # return it.
        value_OUT = self.get_rserve_host()
        
        return value_OUT
        
    #-- END method set_rserve_host() --#


    def set_rserve_port( self, value_IN ):
        
        '''
        Accepts application name.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # store value.
        self.rserve_port = value_IN
        
        # return it.
        value_OUT = self.get_rserve_port()
        
        return value_OUT
        
    #-- END method set_rserve_port() --#


#-- END class LoggingHelper --#
