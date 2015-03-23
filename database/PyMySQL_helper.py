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
Example:

# get instance of mysqldb helper

# import
from python_utilities.database.database_helper_factory import Database_Helper_Factory

# configure database helper
db_host = "localhost"
db_port = 3306
db_username = "<username>"
db_password = "<password>"
db_database = "<database_name>"

# get instance of mysqldb helper
#db_helper = PyMySQL_Helper( db_host, db_port, db_username, db_password, db_database )
db_helper = Database_Helper_Factory.get_database_helper( Database_Helper_Factory.DATABASE_TYPE_PYMYSQL, db_host, db_port, db_username, db_password, db_database )

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

# mysql package
import pymysql

# python utilities - import parent abstract class from this package.
import python_utilities.database.database_helper

class PyMySQL_Helper( python_utilities.database.database_helper.Database_Helper ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================

    # cursor types
    CURSOR_TYPE_DICT = "dict"
    CURSOR_TYPE_ARRAY = "array"

    # defaults
    #DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 3306

    #============================================================================
    # instance variables
    #============================================================================

    # database connection variables
    #db_host = "localhost"
    #db_port = 3306
    #db_username = ""
    #db_password = ""
    #db_database = ""
    
    # variables to hold connection, list of cursors created.
    #database_connection = None
    #cursor_list = []
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    # parent class
    #def __init__( self, db_host_IN = DEFAULT_HOST, db_port_IN = DEFAULT_PORT, db_username_IN = "", db_password_IN = "", db_database_IN = "" ):
        

    #---------------------------------------------------------------------------
    # __del__() method
    #---------------------------------------------------------------------------

    
    # parent class
    #def __del__( self ):


    #============================================================================
    # instance methods
    #============================================================================
    
    
    # parent class
    #def get_connection( self, *args, **kwargs ):
    
    
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
        '''
    
        # return reference
        cursor_OUT = None
        
        # declare variables
        my_connection = None
        
        # get connection.
        my_connection = self.get_connection()
        
        # got something?
        if ( ( my_connection ) and ( my_connection != None ) ):
        
            # yes.  Use it to create cursor. Do we want dict?
            if ( cursor_type_IN == self.CURSOR_TYPE_DICT ):
            
                # yes. create cursor that maps column names to values.
                cursor_OUT = my_connection.cursor( pymysql.cursors.DictCursor )
            
            else:
            
                # no.  Plain old cursor.
                cursor_OUT = my_connection.cursor()
            
            #-- END check to see if we want dictionary cursor --#
            
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
    
    
    def open_connection( self, *args, **kwargs ):
    
        '''
        Uses connection information inside this instance to open a database
            connection.  If there is a problem, might throw an exception, or
            might return None.
            
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
        connection_OUT = pymysql.connect( host = my_host, port = my_port, user = my_username, passwd = my_password, db = my_database )
        
        return connection_OUT
    
    #-- END method open_connection() --#
    
    
    # parent class
    #def close( self, *args, **kwargs ):


#-- END class MySQLdb_Helper --#