from __future__ import unicode_literals

'''
Copyright 2013 Jonathan Morgan

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
This is an abstract class that implements most of the functionality of a database
    helper that can be implemented relatively easily for any database that
    supports the Python DB API.

Usage Example:

# import
from python_utilities.database.database_helper_factory import Database_Helper_Factory

# configure database helper
db_host = "localhost"
db_port = 5432
db_username = "<username>"
db_password = "<password>"
db_database = "<database_name>"

# get instance of mysqldb helper
db_helper = Database_Helper_Factory.get_database_helper( Database_Helper_Factory.DATABASE_TYPE_MYSQLDB, db_host, db_port, db_username, db_password, db_database )

# get connection (if you write to database, you need to commit with connection object).
db_connection = db_helper.get_connection()

# get cursor (opens connection if one not already open).
db_read_cursor = db_helper.get_cursor()

# make select statement
sql_string = "SELECT * FROM django_reference_data_reference_domain ORDER BY domain_name ASC;"

# execute it.
db_read_cursor.execute( sql_string )

# get number of domains.
result_count = int( db_read_cursor.rowcount )

# loop.
domain_counter = 0
for i in range( result_count ):

    # increment counter
    domain_counter += 1

    # get row.
    current_row = db_read_cursor.fetchone()
    
    # get values (default is to return rows as hashes of column name to value).
    current_domain_name = current_row[ 'domain_name' ]
    current_use_count = current_row[ 'use_count' ]
    
    # print
    print( "Domain: " + current_domain_name + " used " + str( current_use_count ) + " times." )
    
#-- END loop over domains. --#

# close everything down.
db_helper.close()
'''

# imports
import sys

# abstract classes
from abc import ABCMeta
from abc import abstractmethod

# database package?

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper

class Database_Helper( object ):


    #============================================================================
    # Declare abstract!
    #============================================================================
    
    
    __metaclass__ = ABCMeta
    

    #============================================================================
    # CONSTANTS-ish
    #============================================================================

    # cursor types
    CURSOR_TYPE_DICT = "dict"
    CURSOR_TYPE_ARRAY = "array"
    
    # defaults
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = -1

    #============================================================================
    # instance variables
    #============================================================================

    # database connection variables
    db_host = DEFAULT_HOST
    db_port = DEFAULT_PORT
    db_username = ""
    db_password = ""
    db_database = ""
    
    # variables to hold connection, list of cursors created.
    database_connection = None
    cursor_list = []
    
    # exception handling
    m_exception_helper = ExceptionHelper()
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self, db_host_IN = DEFAULT_HOST, db_port_IN = DEFAULT_PORT, db_username_IN = "", db_password_IN = "", db_database_IN = "" ):
        
        '''
        Constructor
        '''
        
        # instance variables
        self.db_host = db_host_IN
        self.db_port = db_port_IN
        self.db_username = db_username_IN
        self.db_password = db_password_IN
        self.db_database = db_database_IN
        
        # clear connection and cursor list.
        self.db_connection = None
        self.cursor_list = []
        
    #-- END constructor --#


    #---------------------------------------------------------------------------
    # __del__() method
    #---------------------------------------------------------------------------

    
    def __del__( self ):
        
        '''
        Destructor
        '''
        
        # close everything.
        self.close()
                
    #-- END Destructor --#


    #============================================================================
    # class methods
    #============================================================================
    
    
    @classmethod
    def process_exception( cls, exception_IN = None, message_IN = "", print_details_IN = True, *args, **kwargs ):
    
        # return reference
        status_OUT = ""
    
        # declare variables
        exception_helper = None
        exception_message = ""
        exception_status = ""

        # Get exception helper class.
        exception_helper = cls.m_exception_handler
                                
        # process the exception
        exception_message = message_IN
        exception_status = exception_helper.process_exception( exception_IN = exception_IN, message_IN = exception_message, print_details_IN = print_details_IN )
        
        # set status to description of exception
        status_OUT = exception_helper.last_exception_details
        
        return status_OUT
        
    #-- END method process_exception() --#
        
        
    #============================================================================
    # instance methods
    #============================================================================
    
    
    def get_connection( self, *args, **kwargs ):
    
        '''
        Tries to retrieve already-opened connection.  If one not present, creates
            one, stores it, then returns it.
            
        Preconditions: Assumes that all of the needed connection information for
            the database is stored in this instance.
        '''
    
        # return reference
        connection_OUT = None
        
        # declare variables
        new_connection = None
        
        # got a connection already?
        if ( ( self.db_connection ) and ( self.db_connection != None ) ):
        
            # yes.  Return it.
            connection_OUT = self.db_connection
            
        else:
        
            # no.  Open one, then return it.
            new_connection = self.open_connection()
            
            # store the connection.
            self.db_connection = new_connection
            
            # then, as a sanity check, return what is in self.db_connection.
            connection_OUT = self.db_connection
        
        #-- END check to see if database connection. --#
        
        return connection_OUT
    
    #-- END method get_connection() --#
    
    
    def get_cursor( self, cursor_type_IN = CURSOR_TYPE_DICT, *args, **kwargs ):
    
        '''
        Accepts optional cursor type ("dict" if you want column names mapped to
            values, "array" if you want the position of the column in the SQL
            statement to map to the value - Defaults to "dict"), uses connection
            information in this instance to connect to database if no connection,
            uses connection to create and return a cursor.
            
        Preconditions: Assumes that all of the needed connection information for
            the database is stored in this instance.  

        Postconditions: Adds cursor to list of cursors handed out by this
            instance, so it can make sure they are all closed on close().
            
        Inheritance: If you want more nuanced options based on database type,
            override this method in child class.  For example, you have to do
            something special to get map of column names to values in mysql.
        '''
    
        # return reference
        cursor_OUT = None
        
        # declare variables
        my_connection = None
        
        # get connection.
        my_connection = self.get_connection()
        
        # got something?
        if ( ( my_connection ) and ( my_connection != None ) ):
        
            # yes - get cursor.
            cursor_OUT = my_connection.cursor()

            # got a cursor?
            if ( ( cursor_OUT ) and ( cursor_OUT != None ) ):
            
                # yes.  Add it to list.
                self.cursor_list.append( cursor_OUT )
            
            #-- END check to see if cursor. --#
            
        else:
        
            # no connection, so no cursor.
            cursor_OUT = None
        
        #-- END check to see if we have a connection --#
        
        return cursor_OUT
    
    #-- END method get_cursor() --#
    
    
    @abstractmethod
    def open_connection( self, *args, **kwargs ):
    
        '''
        Uses connection information inside this instance to open a database
            connection.  If there is a problem, might throw an exception, or
            might return None.
            
        *** This must be implemented in child class. ***
            
        Preconditions: Assumes that all of the needed connection information for
            the database is stored in this instance.
        '''
        
        # return reference
        connection_OUT = None
        
        # declare variables
        my_host = ""
        my_port = ""
        my_username = ""
        my_password = ""
        my_database = ""
        
        # get values
        my_host = self.db_host
        my_port = self.db_port
        my_username = self.db_username
        my_password = self.db_password
        my_database = self.db_database
        
        # use them to create a connection.  For now, no error checking.  If it
        #     gets screwed up because the object isn't initialized right, calling
        #     program will figure it out pretty quickly.
        # connection_OUT = MySQLdb.connect( host = my_host, port = my_port, user = my_username, passwd = my_password, db = my_database )
        
        return connection_OUT
    
    #-- END method open_connection() --#
    
    
    def close( self, *args, **kwargs ):
    
        '''
        Loops over all cursors, calling close in a try in case they are already
            closed, then checks for nested connection, does the same.
        '''
    
        #return reference
        status_OUT = ""
        
        # declare variables
        me = "close"
        cursor_count = -1
        current_cursor = None
        status_append = ""
    
        # check if there are cursors.
        if ( len ( self.cursor_list ) > 0 ):
        
            # there are - loop over them.
            cursor_count = 0
            for current_cursor in self.cursor_list:
            
                # try to close cursor.
                cursor_count += 1
                try:
                
                    # close cursor
                    current_cursor.close()
                
                except Exception as e:
                
                    # error closing cursor.

                    # process the exception
                    exception_message = "In " + me + ": cursor " + str( cursor_count ) + " threw exception on close()."
                    exception_status = cls.process_exception( exception_IN = e, message_IN = exception_message, print_details_IN = True )
                    
                    # set status to description of exception
                    status_OUT = status_OUT + status_append + exception_status
                    status_append = "; "

                    # send email to let me know this crashed?

                    # throw exception?
                    #raise( e )

                #-- END try/except for closing cursor --#
            
            #-- END loop over cursors --#
            
            # all are closed.  Empty out list.
            self.cursor_list = []
        
        #-- END check for cursors. --#
        
        # got a connection?
        if ( ( self.db_connection ) and ( self.db_connection != None ) ):
    
            # yes - try to close connection.
            try:
            
                # close cursor
                self.db_connection.close()
            
            except Exception as e:
            
                # error closing cursor.

                # process the exception
                exception_message = "In " + me + ": connection threw exception on close()."
                exception_status = cls.process_exception( exception_IN = e, message_IN = exception_message, print_details_IN = True )
                
                # set status to description of exception
                status_OUT = status_OUT + status_append + exception_status
                status_append = "; "

                # send email to let me know this crashed?

                # throw exception?
                #raise( e )

            #-- END try/except for closing cursor --#
            
            # empty out connection variable.
            self.db_connection = None

        #-- END check to see if database connection. --#
        
        return status_OUT

    #-- END close() method --#
    

#-- END class Database_Helper --#