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

# import specific classes of helper for different types (mixed in below, so you
#     don't have to have the postgresql database installed to load MySQL and
#     vice versa).
#from python_utilities.database.MySQLdb_helper import MySQLdb_Helper
#from python_utilities.database.psycopg2_helper import psycopg2_Helper

class Database_Helper_Factory( object ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================

    # database types
    DATABASE_TYPE_MYSQLDB = "MySQLdb"
    DATABASE_TYPE_PSYCOPG2 = "psycopg2"
    DATABASE_TYPE_PYMYSQL = "PyMySQL"
    
    # defaults
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = -1

    #============================================================================
    # instance variables
    #============================================================================


    #============================================================================
    # class methods
    #============================================================================
    
    
    @classmethod
    def get_database_helper( cls,
                             database_type_IN = "",
                             db_host_IN = DEFAULT_HOST,
                             db_port_IN = DEFAULT_PORT,
                             db_username_IN = "",
                             db_password_IN = "",
                             db_database_IN = "",
                             *args,
                             **kwargs ):
    
        # return reference
        helper_OUT = None
    
        # declare variables
        if ( database_type_IN == cls.DATABASE_TYPE_MYSQLDB ):
        
            # return MySQL helper.
            from python_utilities.database.MySQLdb_helper import MySQLdb_Helper
            helper_OUT = MySQLdb_Helper( db_host_IN, db_port_IN, db_username_IN, db_password_IN, db_database_IN )

        elif ( database_type_IN == cls.DATABASE_TYPE_PSYCOPG2 ):            
        
            # return PostgreSQL psycopg2 helper.
            from python_utilities.database.psycopg2_helper import psycopg2_Helper
            helper_OUT = psycopg2_Helper( db_host_IN, db_port_IN, db_username_IN, db_password_IN, db_database_IN )
            
        elif ( database_type_IN == cls.DATABASE_TYPE_PYMYSQL ):            
        
            # return MySQL PyMySQL helper.
            from python_utilities.database.pymysql_helper import PyMySQL_Helper
            helper_OUT = PyMySQL_Helper( db_host_IN, db_port_IN, db_username_IN, db_password_IN, db_database_IN )
            
        else:
        
            # unknown type - return nothing.
            helper_OUT = None

        #-- END check to see what type has been requested. --#
        
        return helper_OUT
        
    #-- END method get_database_helper() --#
    

#-- END class Database_Helper_Factory --#