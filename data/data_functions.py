import calendar
import datetime
import numpy
import pandas
import psycopg2
import psycopg2.extras
import six
import sys
import traceback

#==============================================================================#
# Constants-ish
#==============================================================================#


JOIN_COLUMN_SOURCE_NAME = "source_name"
JOIN_COLUMN_DEST_NAME = "dest_name"


#==============================================================================#
# functions
#==============================================================================#


def clean_up_sas_strings( df_IN = None ):

    '''
    When pandas imports SAS files, it stores string values as "b'<value>'" (must just be calling
        str function...).  This function loops over all columns, and for any that are of type
        "object", cleans up that garbage, leaving a normal string value in its place.

    Accepts a pandas DataFrame.  Cleans up values in all "object" columns.
        Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    df_length = -1
    column_to_type_series = None
    column_name = ""
    data_type = None
    data_type_name = ""
    binary_string_regex = r"^b'(.*)'$"
    temp_series = None

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # length of DataFrame
        df_length = len( df_IN )
        print( "DataFrame size = " + str( df_length ) )

        # get data types of columns.
        column_to_type_series = df_IN.dtypes

        # loop.
        for column_name, data_type in column_to_type_series.iteritems():

            # get name of data type.
            data_type_name = str( data_type )

            print( "- column name = " + str( column_name ) + "; data type = " + str( data_type_name ) )

            # is it an "object"?
            if ( data_type_name == "object" ):

                print( "----> column name = " + str( column_name ) + " = " + str( data_type_name ) + "!" )

                # yes.  First, explicitly convert to string (it is a binary string to start).
                df_IN.loc[ :, column_name ] = df_IN[ column_name ].astype( 'str' )

                # replace all rows that contain "nan" with ""
                df_IN[ column_name ].replace( to_replace = "nan", value = "", inplace = True )

                # For all values that start with "b'" and end with "'", strip
                #     that stuff off.
                df_IN[ column_name ].replace( to_replace = binary_string_regex, value = r"\1", regex = True, inplace = True )

            #-- END check to see if data type is "object". --#

        #-- END loop over data types. --#

        # place DataFrame in return reference.
        df_OUT = df_IN

    else:

        # no DataFrame passed in.  For shame.
        print( "ERROR - no DataFrame passed in.  Nothing to do." )

        df_OUT = None

    #-- END check to make sure DataFrame passed in. --#

    return df_OUT

#-- END function clean_up_sas_strings() --#

print( "Function clean_up_sas_strings() declared at " + str( datetime.datetime.now() ) )


def convert_sas_dates( df_IN = None, column_name_IN = None, output_column_name_IN = None ):

    '''
    Accepts a DataFrame and the name of a column within that DataFrame that contains
        SAS date values.  Converts the values in that column from being days from
        1960-01-01 to a standard date, in place in the DataFrame.  Returns the
        DataFrame.
    '''

    # return reference
    df_OUT = None
    output_column_name = None

    df_OUT = df_IN

    # got a column name?
    if ( column_name_IN is not None ):

        # is output column name also specified?
        if ( output_column_name_IN is not None ):

            # yes, use it.
            output_column_name = output_column_name_IN

        else:

            # no, just output in place.
            output_column_name = column_name_IN

        #-- END check to see if output column name specified. --#

        # convert values to date.
        df_OUT[ output_column_name ] = pandas.to_timedelta( df_OUT[ column_name_IN ], unit = 'D') + pandas.Timestamp( '1960-01-01' )

    else:

        print( "ERROR - no column name passed in, can't convert SAS dates." )

    #-- END check to see if column name --#

    return df_OUT

#-- END function convert_sas_dates() --#

print( "Function convert_sas_dates() declared at " + str( datetime.datetime.now() ) )


def create_db_sample_csv( table_name_IN, engine_IN, sample_size_IN = 10000, output_file_path_IN = None, encoding_IN = "utf-8" ):

    '''
    Accepts table name, SQLAlchemy engine, and optional sample size.
        Selects a random sample of size sample_size_IN from table whose
        name is passed in, and then outputs it to either a default file
        name of "<table_name_IN>-sample.csv" in the current directory, or
        a custom path if one is passed in output_file_path_IN.
        Returns the sample DataFrame
    '''

    # return reference
    df_OUT = None

    # declare variables
    table_name = ""
    sql_string = ""
    sample_df = None
    sample_size = -1
    csv_file_name = ""

    # set table name and sample size
    table_name = table_name_IN
    sample_size = sample_size_IN

    # set up query
    sql_string = "SELECT *"
    sql_string += " FROM " + table_name
    sql_string += " ORDER BY random()"
    sql_string += " LIMIT " + str( sample_size )
    sql_string += ";"

    # import results of query in to pandas
    sample_df = pandas.read_sql( sql_string, con = engine_IN )
    sample_df.head()

    # write to CSV file - set file name
    if ( ( output_file_path_IN is not None ) and ( output_file_path_IN != "" ) ):

        # use path passed in
        csv_file_name = output_file_path_IN

    else:

        # use default
        csv_file_name = table_name + "-sample.csv"

    #-- END check to see if output file path passed in. --#

    # write to CSV file
    sample_df.to_csv( csv_file_name, index = False, encoding = encoding_IN )

    print( "File \"" + csv_file_name + "\" created at " + str( datetime.datetime.now() ) )

    df_OUT = sample_df

    return df_OUT

#-- END function create_db_sample_csv() --#

print( "Function create_db_sample_csv() declared at " + str( datetime.datetime.now() ) )


def is_integer( float_value_IN, is_nan_int_IN = True ):

    # return reference
    is_integer_OUT = False

    # declare variables
    numpy_float = None
    value_as_string = ""
    value_as_float = None
    value_as_int = None
    value_as_float_again = None

    # NaN?
    numpy_float = numpy.float64( float_value_IN )
    if ( ( numpy_float.dtype == float ) and ( numpy.isnan( numpy_float ) == True ) ):

        # NaN - Do we count NaN as an int?
        is_integer_OUT = is_nan_int_IN

    else:

        # convert to string, then to float, int, and back to float.
        value_as_string = str( float_value_IN )
        #print( "Value = \"" + value_as_string + "\"" )

        value_as_float = float( value_as_string )
        #print( "Value as float = \"" + str( value_as_float ) + "\"" )

        value_as_int = int( value_as_float )
        #print( "Value as int = \"" + str( value_as_int ) + "\"" )

        value_as_float_again = float( value_as_int )
        #print( "Value as float again = \"" + str( value_as_float_again ) + "\"" )

        # check if floats are equal
        if( value_as_float == value_as_float_again ):

            # yes - integer
            is_integer_OUT = True

        else:

            # no - not integer.
            is_integer_OUT = False

        #-- END check to see if is integer. --#

    #-- END check to see if NaN --#

    return is_integer_OUT

#-- END function is_integer() --#

print( "Function is_integer() declared at " + str( datetime.datetime.now() ) )


def clean_up_floats( df_IN = None, convert_nan_to_IN = -999999 ):

    '''
    Checks float columns

    Accepts a pandas DataFrame.  Cleans up values in all "object" columns.
        Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    df_length = -1
    column_to_type_series = None
    column_name = ""
    data_type = None
    data_type_name = ""
    temp_series = None
    value_count = -1

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # length of DataFrame
        df_length = len( df_IN )
        print( "DataFrame size = " + str( df_length ) )

        # get data types of columns.
        column_to_type_series = df_IN.dtypes

        # loop.
        for column_name, data_type in column_to_type_series.iteritems():

            # get name of data type.
            data_type_name = str( data_type )

            print( "- column name = " + str( column_name ) + "; data type = " + str( data_type_name ) )

            # is it an "object"?
            if ( data_type_name == "float64" ):

                # check to see if all values are integers.
                temp_series = df_IN[ column_name ].map( is_integer )

                # Any False?
                value_list = list( temp_series.drop_duplicates() )
                if ( False not in value_list ):

                    print( "----> column name = " + str( column_name ) + " = " + str( data_type_name ) + ", is an int!" )

                    # no.  Convert column to integer.  Convert NaN to -1...
                    df_IN.loc[ :, column_name ] = df_IN[ column_name ].fillna( convert_nan_to_IN )

                    # then store column astype( int ).
                    df_IN.loc[ :, column_name ] = df_IN[ column_name ].astype( 'int' )

                else:

                    # non-integer values.  Do nothing.
                    print( "----> column name = " + str( column_name ) + " = " + str( data_type_name ) + ", is NOT an int!" )

                #-- END check to see if

            #-- END check to see if data type is "object". --#

        #-- END loop over data types. --#

        # place DataFrame in return reference.
        df_OUT = df_IN

    else:

        # no DataFrame passed in.  For shame.
        print( "ERROR - no DataFrame passed in.  Nothing to do." )

        df_OUT = None

    #-- END check to make sure DataFrame passed in. --#

    return df_OUT

#-- END function clean_up_sas_strings() --#

print( "Function clean_up_floats() declared at " + str( datetime.datetime.now() ) )


def output_members( object_IN ):

    # declare variables
    property_list = None
    current_property = None
    property_name = None
    property_value = None

    property_list = inspect.getmembers( object_IN )
    for property in property_list:

        property_name = property[ 0 ]
        property_value = property[ 1 ]

        print( "- property " + str( property_name ) + " = " + str( property_value ) )

    #-- END loop over property list --#

#-- END function output_members() --#

print( "Function output_members() declared at " + str( datetime.datetime.now() ) )


def column_names_replace( df_IN, find_IN, replace_IN ):

    '''
    Accepts a pandas DataFrame.  Finds all column names that contain find_IN.  if found,
        replaces find_IN with replace_IN. Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    me = "column_names_replace"
    column_name_list = None
    rename_map = None
    original_name = ""
    replaced_name = ""

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # Create dictionary that maps original column names to that same name in all lower-case.
        rename_map = {}

        # get list of column names
        column_name_list = list( df_IN.columns )

        # loop over column names
        for original_name in column_name_list:

            # look for find_IN in name.
            if ( find_IN in original_name ):

                # find_IN is present. Replace.
                replaced_name = original_name.replace( find_IN, replace_IN )

                print( "In {}(): Found match for \"{}\" - \"{}\" - replacing with \"{}\"".format( me, find_IN, original_name, replaced_name ) )

                # add to rename map
                rename_map[ original_name ] = replaced_name

            #-- END check to see if find_IN is in original_name --#

        #-- END loop over column names --#

        # rename columns in DataFrame
        df_IN.rename( columns = rename_map, inplace = True )

        # place the DataFrame in the return reference.
        df_OUT = df_IN

    else:

        # nothing passed in.  For shame.
        print( "In {}(): ERROR - no DataFrame passed in.  Nothing to do.".format( me ) )

        df_OUT = None

    #-- END check to see if DataFrame passed in. --#

    return df_OUT

#-- END function column_names_replace() --#

print( "Function column_names_replace() declared at " + str( datetime.datetime.now() ) )


def column_names_replace_prefix( df_IN, find_IN, replace_IN ):

    '''
    Accepts a pandas DataFrame.  Finds all column names that start with find_IN.  if Converts all column names to lower case.
        Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    me = "column_names_replace_prefix"
    column_name_list = None
    rename_map = None
    original_name = ""
    starts_with_prefix = None
    replaced_name = ""

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # Create dictionary that maps original column names to that same name in all lower-case.
        rename_map = {}

        # get list of column names
        column_name_list = list( df_IN.columns )

        # loop over column names
        for original_name in column_name_list:

            # look for find_IN at beginning of name.
            starts_with_prefix = original_name.startswith( find_IN )
            if ( starts_with_prefix == True ):

                # find_IN is prefix. Replace that first occurrence (and no more).
                replaced_name = original_name.replace( find_IN, replace_IN, 1 )

                print( "In {}(): Found match for prefix \"{}\" - \"{}\" - replacing with \"{}\"".format( me, find_IN, original_name, replaced_name ) )

                # add to rename map
                rename_map[ original_name ] = replaced_name

            #-- END check to see if find_IN is in original_name --#

        #-- END loop over column names --#

        # rename columns in DataFrame
        df_IN.rename( columns = rename_map, inplace = True )

        # place the DataFrame in the return reference.
        df_OUT = df_IN

    else:

        # nothing passed in.  For shame.
        print( "In {}(): ERROR - no DataFrame passed in.  Nothing to do.".format( me ) )

        df_OUT = None

    #-- END check to see if DataFrame passed in. --#

    return df_OUT

#-- END function column_names_replace_prefix() --#

print( "Function column_names_replace_prefix() declared at " + str( datetime.datetime.now() ) )


def column_names_to_lower_case( df_IN ):

    '''
    Postgresql works best when all column names are lower case.  Here is a function
        to convert all column names in a pandas DataFrame to lower case.

    Accepts a pandas DataFrame.  Converts all column names to lower case.
        Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    column_name_list = None
    rename_map = None
    original_name = ""
    name_lower = ""

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # Create dictionary that maps original column names to that same name in all lower-case.
        rename_map = {}

        # get list of column names
        column_name_list = list( df_IN.columns )

        # loop over column names
        for original_name in column_name_list:

            # convert to all lower case.
            name_lower = original_name.lower()

            # add to rename map
            rename_map[ original_name ] = name_lower

        #-- END loop over column names --#

        # rename columns in DataFrame
        df_IN.rename( columns = rename_map, inplace = True )

        # place the DataFrame in the return reference.
        df_OUT = df_IN

    else:

        # nothing passed in.  For shame.
        print( "ERROR - no DataFrame passed in.  Nothing to do." )

        df_OUT = None

    #-- END check to see if DataFrame passed in. --#

    return df_OUT

#-- END function column_names_to_lower_case() --#

print( "Function column_names_to_lower_case() declared at " + str( datetime.datetime.now() ) )

def list_primary_key_columns( table_name_IN = None,
                              cursor_IN = None,
                              schema_IN = None ):

    '''
    Accepts table name and cursor.  Queries for primary key columns for the
        table whose name was passed in, returns a list of the names of the
        columns that make up the table's primary key, else an empty list if
        no primary key present.
    '''

    # return reference
    pk_list_OUT = []

    # declare variables
    sql_string = ""
    row_count = -1
    current_row = None
    column_name = ""
    column_dtype = ""

    # init
    table_of_interest = table_name_IN

    # got a cursor?
    if ( cursor_IN is not None ):

        # got a table name?
        if ( ( table_name_IN is not None ) and ( table_name_IN != "" ) ):

            # build query
            sql_string = "SELECT a.attname AS a_att_name, format_type( a.atttypid, a.atttypmod ) AS data_type"
            sql_string += " FROM pg_index i"
            sql_string += " JOIN pg_attribute a ON a.attrelid = i.indrelid"
            sql_string += "     AND a.attnum = ANY( i.indkey )"
            sql_string += " WHERE i.indrelid = '"
            if ( schema_IN is not None ):
                sql_string += schema_IN + "."
            #-- END check to see if schema --#
            sql_string += str( table_name_IN ) + "'::regclass"
            sql_string += "     AND i.indisprimary;"

            # execute query
            cursor_IN.execute( sql_string )

            # first, see how many?
            row_count = cursor_IN.rowcount
            print( "Found " + str( row_count ) + " primary key fields for table \"" + table_name_IN + "\", schema \"" + str( schema_IN ) + "\"." )

            # output results
            for current_row in cursor_IN:

                # get values
                column_name = current_row[ "a_att_name" ]
                column_dtype = current_row[ "data_type" ]

                # add to list
                pk_list_OUT.append( ( column_name, column_dtype ) )

                # output
                print( "- Foreign key: column name = \"" + str( column_name ) + "\"; type = \"" + str( column_dtype ) + "\"" )

            #-- END loop over foreign key fields --#

        else:

            print( "You must provide a database table name." )
            pk_list_OUT = []

        #-- END check to make sure table name passed in. --#

    else:

        print( "You must provide a database cursor." )
        pk_list_OUT = []

    #-- END check to see if cursor. --#

    return pk_list_OUT

#-- END function list_primary_key_columns() --#

print( "Function list_primary_key_columns() declared at " + str( datetime.datetime.now() ) )

def add_primary_key( table_name_IN = None,
                     cursor_IN = None,
                     column_name_IN = "id",
                     pk_type_IN = "BIGSERIAL",
                     schema_IN = None ):

    '''
    Accepts table name and cursor.  Queries for primary key columns for the
        table whose name was passed in.  If one or more columns present, does
        nothing.  If no primary key, creates one with a default column name of
        "id".
    '''

    # return reference
    pk_list_OUT = []

    # declare variables
    me = "add_primary_key"
    pk_list = []
    pk_count = -1
    sql_string = ""

    # init
    table_of_interest = table_name_IN

    # got a cursor?
    if ( cursor_IN is not None ):

        # got a table name?
        if ( ( table_name_IN is not None ) and ( table_name_IN != "" ) ):

            # does the ildoc_admit table have a primary key?
            pk_list = list_primary_key_columns( table_name_IN, cursor_IN, schema_IN )
            pk_count = len( pk_list )
            print( "====> PK count = " + str( pk_count ) + " ( PK list = " + str( pk_list ) + " )" )

            # No primary key.  Add auto-incrementing bigint PK (BIGSERIAL PRIMARY KEY) named "id".
            #     For column data type:
            #     - bigint = BIGSERIAL
            #     - int = SERIAL
            if ( pk_count == 0 ):

                # no primary keys.  Add one named "id"
                sql_string = "ALTER TABLE "
                if ( schema_IN is not None ):
                    sql_string += schema_IN + "."
                #-- END check to see if schema_IN --#
                sql_string += table_name_IN + " ADD COLUMN " + column_name_IN + " " + pk_type_IN + " PRIMARY KEY;"
                print( "========> Adding Primary Key: " + str( sql_string ) )

                # execute query
                cursor_IN.execute( sql_string )

                # does the table have a primary key?
                pk_list = list_primary_key_columns( table_name_IN, cursor_IN, schema_IN )
                pk_count = len( pk_list )
                print( "========> After adding PK: PK count = " + str( pk_count ) + " ( PK list = " + str( pk_list ) + " )" )

            #-- END check to see if no existing primary key. --#

        else:

            print( "In " + me + "(): You must provide a database table name." )

        #-- END check to make sure table name passed in. --#

    else:

        print( "In " + me + "(): You must provide a database cursor." )

    #-- END check to see if cursor. --#

    return pk_list_OUT

#-- END function add_primary_key() --#

print( "Function add_primary_key() declared at " + str( datetime.datetime.now() ) )

def get_distinct_df_column_values( df_IN, column_name_IN, is_verbose_IN = False ):

    # return reference
    value_list_OUT = []

    # declare variables
    unique_values = None
    unique_value = None

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # got a column name?
        if ( ( column_name_IN is not None ) and ( column_name_IN != "" ) ):

            # Check out unique values.
            unique_values = df_IN[ column_name_IN ].unique()
            for unique_value in unique_values:

                if ( is_verbose_IN == True ):
                    print( "- " + str( unique_value ) )
                #-- END check to see if verbose --#

                # add value to list.
                value_list_OUT.append( unique_value )

            #-- END loop over unique values in column --#

        else:

            print( "ERROR - no column name passed in, so don't know which column to process." )
            value_list_OUT = None

    else:

        # nothing passed in.  For shame.
        print( "ERROR - no DataFrame passed in.  Nothing to do." )
        value_list_OUT = None

    #-- END check to see if DataFrame passed in. --#

    return value_list_OUT

#-- END function get_distinct_df_column_values --#

print( "Function get_distinct_df_column_values() declared at " + str( datetime.datetime.now() ) )

def get_distinct_values( cursor_IN, table_name_IN, column_name_IN, schema_name_IN = None ):

    # return reference
    value_list_OUT = []

    # declare variables
    sql_string = ""
    current_row = None
    column_value = None
    value_count = -1

    # print current column name
    print( "DISTINCT values for column \"" + schema_name_IN + "." + table_name_IN + "." + column_name_IN + "\":" )

    # build query to get distinct values
    sql_string = "SELECT " + column_name_IN + ", COUNT( " + column_name_IN + " ) as value_count"
    sql_string += " FROM "
    if ( ( schema_name_IN is not None ) and ( schema_name_IN != "" ) ):
        sql_string += schema_name_IN + "."
    #-- END check to see if schema name passed in --#
    sql_string += table_name_IN
    sql_string += " GROUP BY " + column_name_IN
    sql_string += " ORDER BY " + column_name_IN + ";"

    # execute the query
    cursor_IN.execute( sql_string )

    # loop over and output the results
    for current_row in cursor_IN:

        # get values
        column_value = current_row[ column_name_IN ]
        value_count = current_row[ "value_count" ]

        # add value to list.
        value_list_OUT.append( column_value )

        # print out the value
        print( "- " + str( column_value ) + " ( occurs " + str( value_count ) + " )" )

    #-- END loop over column values --#

    return value_list_OUT

#-- END function get_distinct_values --#

print( "Function get_distinct_values() declared at " + str( datetime.datetime.now() ) )

def provide_access_to( name_IN = None,
                       role_IN = None,
                       type_IN = "TABLE",
                       cursor_IN = None,
                       privilege_list_IN = None,
                       schema_IN = None ):

    # return reference
    status_list_OUT = []

    # declare variables
    privilege_string = ""
    sql_string = ""

    if ( ( privilege_list_IN is not None ) and ( len( privilege_list_IN ) > 0 ) ):
        privilege_string = ", ".join( privilege_list_IN )
    else:
        privilege_string = "ALL PRIVILEGES"
    #-- END creation of privilege string --#

    # print current column name
    print( "GRANTing " + str( role_IN ) + " " + privilege_string + " ON " + str( type_IN ) + " " + str( name_IN ) )

    # build query to get distinct values
    sql_string = "GRANT " + privilege_string
    sql_string += " ON " + type_IN
    sql_string += " "
    if ( schema_IN is not None ):
        sql_string += schema_IN + "."
    #-- END check to see if schema specified. --#
    sql_string += name_IN
    sql_string += " TO " + role_IN
    sql_string += ";"

    # execute the query
    cursor_IN.execute( sql_string )

    return status_list_OUT

#-- END function provide_access_to --#

print( "Function provide_access_to() declared at " + str( datetime.datetime.now() ) )

def change_table_owner( name_IN, role_IN, cursor_IN = None, schema_IN = None ):

    # return reference
    status_list_OUT = []

    # declare variables
    sql_string = ""

    # print current column name
    print( "ALTERing TABLE so " + str( role_IN ) + " is OWNER of " + str( name_IN ) )

    # build query to get distinct values
    sql_string = "ALTER TABLE"

    # table name
    sql_string += " "
    if ( schema_IN is not None ):
        sql_string += schema_IN + "."
    #-- END check to see if schema passed in --#
    sql_string += name_IN

    # new owner
    sql_string += " OWNER TO " + role_IN
    sql_string += ";"

    print( "==> " + sql_string )

    # execute the query
    cursor_IN.execute( sql_string )

    return status_list_OUT

#-- END function change_table_owner --#

print( "Function change_table_owner() declared at " + str( datetime.datetime.now() ) )


def create_column( column_name_IN = None,
                   table_name_IN = None,
                   schema_IN = "public",
                   column_type_IN = "text",
                   cursor_IN = None ):

    '''
    Accepts column name, table name, and optional schema (defaults to "public") and
        column type (defaults to "text").  Checks to see if column exists with that name.
        If not, creates one to specs passed in.  If errors, returns detailed messages in
        status list.
    Postconditions: Does not commit transaction.  You must do that outside after the call returns.
    '''

    # return reference
    status_list_OUT = []

    # declare variables
    sql_string = ""
    current_row = None
    existing_count = -1
    schema_name = ""
    table_name = ""
    new_column_name = ""
    new_column_type = ""
    status_message = ""


    # Do we have a column name?
    if ( ( column_name_IN is not None ) and ( column_name_IN != "" ) ):

        # Do we have a table name?
        if ( ( table_name_IN is not None ) and ( table_name_IN != "" ) ):
            # check to see if column already exists

            # SQL string to select columns in table.
            sql_string = "SELECT COUNT( * ) AS existing_count"
            sql_string += " FROM information_schema.columns"
            sql_string += " WHERE table_schema = '" + schema_IN + "'"
            sql_string += "     AND table_name = '" + table_name_IN + "'"
            sql_string += "     AND column_name = '" + column_name_IN + "'"
            sql_string += ";"

            # execute the query
            cursor_IN.execute( sql_string )

            # get the count
            current_row = cursor_IN.fetchone()
            existing_count = current_row[ "existing_count" ]

            # already exists?
            if ( existing_count == 0 ):

                # no - create column.

                # set up values
                schema_name = schema_IN
                table_name = table_name_IN
                new_column_name = column_name_IN
                new_column_type = column_type_IN

                # create SQL
                sql_string = "ALTER TABLE " + schema_name + "." + table_name + " ADD COLUMN " + new_column_name + " " + new_column_type + ";"

                # run SQL
                cursor_IN.execute( sql_string )

                # commit outside...
                #connection.commit()

                print( "====> " + str( sql_string ) + " completed at " + str( datetime.datetime.now() ) )

            else:

                status_message = "Column named \"" + column_name_IN + "\" already exists in " + schema_IN + "." + table_name_IN + ".  Could not create."
                status_list_OUT.append( status_message )

            #-- END check to see if column already exists. --#

        else:

            status_message = "No table name provided - can't create column named \"" + column_name_IN + "\"."
            status_list_OUT.append( status_message )

        #-- END check to see if table name --#

    else:

        status_message = "No column name provided - can't create."
        status_list_OUT.append( status_message )

    #-- END check to see if column name --#

    return status_list_OUT

#-- END function create_column --#

print( "Function create_column() declared at " + str( datetime.datetime.now() ) )


def populate_date_column( column_name_IN = None,
                          table_name_IN = None,
                          schema_IN = "public",
                          year_column_IN = None,
                          month_column_IN = None,
                          day_column_IN = None,
                          date_column_IN = None,
                          date_parse_format_IN = None,
                          default_day_IN = None,
                          where_clause_IN = "",
                          cursor_IN = None,
                          min_year_IN = 1900,
                          max_year_IN = 2050 ):

    '''
    Accepts:
    - table info: column name, table name, and optional schema (defaults to "public").
    - date information, either:

        - year_column_IN, month_column_IN, day_column_IN - date parts to combine to create date
        - date_column_IN and date_parse_format_IN - full date string column plus parse format string, so date can be parsed from string and then values placed in date column.
    - default_day_IN - optional default day value in case you just have month and year values.
        column type (defaults to "text").

    Checks if year, month, and day columns, uses values from them to populate column whose name
        was passed in.  If date column and parse string, parses date, uses date parts from it to
        populate column whose name was passed in.  If errors, returns detailed messages in
        status list.

    Postconditions: Does not commit transaction.  You must do that outside after the call returns.
    '''

    # return reference
    status_list_OUT = []

    # declare variables
    sql_string = ""
    current_row = None
    existing_count = -1
    schema_name = ""
    table_name = ""
    new_column_name = ""
    new_column_type = ""
    status_message = ""
    where_clause = ""
    leap_year_list = []

    # Do we have a column name?
    if ( ( column_name_IN is not None ) and ( column_name_IN != "" ) ):

        # Do we have a table name?
        if ( ( table_name_IN is not None ) and ( table_name_IN != "" ) ):

            # WHERE clause passed in?
            if ( ( where_clause_IN is not None ) and ( where_clause_IN != "" ) ):

                # WHERE clause passed in - use it!
                where_clause = where_clause_IN

            #-- END check to see if custom WHERE clause --#

            # got date part column names?
            if ( ( ( year_column_IN is not None ) and ( year_column_IN != "" ) )
                 and ( ( month_column_IN is not None ) and ( month_column_IN != "" ) )
                 and ( ( ( day_column_IN is not None ) and ( day_column_IN != "" ) ) or ( default_day_IN is not None ) ) ):

                # we have date part column names.  Use them.

                # well, not so fast...  First make a list of leap years and
                #     non-leap years between min and max years.
                for year in range( min_year_IN, max_year_IN + 1 ):

                    # is it a leap year?
                    is_leap_year = calendar.isleap( year )
                    if ( is_leap_year == True ):

                        # it is a leap year - add it to the list.
                        leap_year_list.append( str( year ) )

                    #-- END check to see if leap year --#

                #-- END loop over years.

                # UPDATE
                sql_string = "UPDATE " + schema_IN + "." + table_name_IN
                sql_string += " SET " + column_name_IN + " = MAKE_DATE( "
                sql_string += "CAST( " + year_column_IN + " AS integer ), "
                sql_string += "CAST( " + month_column_IN + " AS integer ), "

                # got day column?
                if ( ( day_column_IN is not None ) and ( day_column_IN != "" ) ):
                    # yes - use it
                    sql_string += "CAST( " + day_column_IN + " AS integer )"
                else:
                    # no - use default value
                    sql_string += default_day_IN
                #-- END check to see if day column. --#

                sql_string += " )"

                # WHERE clause?
                if ( ( where_clause is None ) or ( where_clause == "" ) ):

                    # build WHERE clause
                    where_clause = "WHERE"

                    # check for empty or invalid for each of the parts.

                    # year
                    where_clause += " ( ( " + year_column_IN + " IS NOT NULL )"
                    where_clause += " AND ( CAST( " + year_column_IN + " AS integer ) >= " + str( min_year_IN ) + " )"
                    where_clause += " AND ( CAST( " + year_column_IN + " AS integer ) <= " + str( max_year_IN ) + " ) )"

                    # got a day column?
                    if ( ( day_column_IN is not None ) and ( day_column_IN != "" ) ):

                        # yes - check it in concert with month column

                        # START subset 1
                        where_clause += " AND ("

                        # subset 1-1
                        where_clause += " ( " + month_column_IN + " IS NOT NULL )"

                        # subset 1-2
                        where_clause += " AND ( " + day_column_IN + " IS NOT NULL )"

                        # subset 1-3
                        where_clause += " AND ( CAST( " + day_column_IN + " AS integer ) > 0 )"

                        # START subset 1-4
                        where_clause += " AND ( "

                        # subset 1-4-1 - "30 days have September, April, June, and November..."
                        where_clause += " ( ( CAST( " + month_column_IN + " AS integer ) IN ( 4, 6, 9, 11 ) ) AND ( CAST( " + day_column_IN + " AS integer ) <= 30 ) )"

                        # subset 1-4-2 - "...All the rest have 31..."
                        where_clause += " OR ( ( CAST( " + month_column_IN + " AS integer ) IN ( 1, 3, 5, 7, 8, 10, 12 ) ) AND ( CAST( " + day_column_IN + " AS integer ) <= 31 ) )"

                        # START subset 1-4-3 - "...Except February.  It has 28, or 29 in a leap year.
                        where_clause += " OR ("

                        # subset 1-4-3-1 - February...
                        where_clause += " ( ( CAST( " + month_column_IN + " AS integer ) = 2 )"

                        # ...leap year...
                        where_clause += " AND ( CAST( " + year_column_IN + " AS integer ) IN ( " + ", ".join( leap_year_list ) + " ) )"
                        # ...and 29 or less.
                        where_clause += " AND ( CAST( " + day_column_IN + " AS integer ) <= 29 ) )"

                        # subset 1-4-3-2 - February...
                        where_clause += " OR ( ( CAST( " + month_column_IN + " AS integer ) = 2 )"

                        # ...not leap year...
                        where_clause += " AND ( CAST( " + year_column_IN + " AS integer ) NOT IN ( " + ", ".join( leap_year_list ) + " ) )"
                        # ...and 29 or less.
                        where_clause += " AND ( CAST( " + day_column_IN + " AS integer ) <= 28 ) )"

                        # END subset 1-4-3
                        where_clause += " )"

                        # END subset 1-4
                        where_clause += " )"

                        # END subset 1
                        where_clause += " )"

                    else:

                        # month
                        where_clause += " AND ( ( " + month_column_IN + " IS NOT NULL )"
                        where_clause += " AND ( CAST( " + month_column_IN + " AS integer ) > 0 )"
                        where_clause += " AND ( CAST( " + month_column_IN + " AS integer ) <= 12 ) )"

                    #-- END check to see if day column. --#

                #-- END check to see if WHERE clause passed in. --#

                if ( where_clause != "" ):
                    sql_string += " " + where_clause
                #-- END check to see if where clause --#

                sql_string += ";"

            # got date and parse pattern?
            elif ( ( ( date_column_IN is not None ) and ( date_column_IN != "" ) )
                and ( ( date_parse_format_IN is not None ) and ( date_parse_format_IN != "" ) ) ):

                # we are to parse, rather than use date parts.

                # UPDATE
                sql_string = "UPDATE " + table_name_IN
                sql_string += " SET " + column_name_IN + " = TO_DATE( "
                sql_string += "CAST( " + date_column_IN + " AS text ), "
                sql_string += "'" + date_parse_format_IN + "'"
                sql_string += " )"

                # WHERE clause
                if ( ( where_clause is None ) or ( where_clause == "" ) ):

                    # build WHERE clause
                    where_clause = "WHERE"

                    # check for empty or invalid date string column.
                    where_clause += " ( " + date_column_IN + " IS NOT NULL ) AND ( CAST( " + date_column_IN + " AS text ) != "" )"

                #-- END check to see if WHERE clause passed in. --#

                # WHERE clause?
                if ( where_clause != "" ):
                    sql_string += " " + where_clause
                #-- END check to see if where clause --#

                sql_string += ";"

            else:

                status_message = "Didn't have either date parts or a date string column and parse format, so could not set date."
                status_list_OUT.append( status_message )

            #-- END check to see if we have what we need to set date. --#

            # got SQL?
            if ( ( sql_string is not None ) and ( sql_string != "" ) ):

                print( "SQL: " + sql_string )

                # run SQL
                cursor_IN.execute( sql_string )
                #pgsql_connection.commit()

                print( "UPDATEd at " + str( datetime.datetime.now() ) )

            else:

                status_message = "No SQL.  Strange and unexpected.  Error."
                status_list_OUT.append( status_message )

            #-- END check to see if SQL --#

        else:

            status_message = "No table name provided - can't populate column named \"" + column_name_IN + "\"."
            status_list_OUT.append( status_message )

        #-- END check to see if table name --#

    else:

        status_message = "No column name provided - can't populate."
        status_list_OUT.append( status_message )

    #-- END check to see if column name --#

    return status_list_OUT

#-- END function populate_date_column --#

print( "Function populate_date_column() declared at " + str( datetime.datetime.now() ) )


def create_fk( from_table_name_IN = None,
               from_column_name_IN = None,
               to_table_name_IN = None,
               to_column_name_IN = "id",
               cursor_IN = None,
               add_column_IN = True,
               from_schema_name_IN = None,
               to_schema_name_IN = None ):

    '''
    Create ALTER TABLE statements to add foreign key from table and column passed in to
        to table and column passed in, using connection passed in.
    '''

    # return reference
    status_list_OUT = []

    # declare variables
    sql_string = ""
    from_schema_name = ""
    from_table_name = ""
    from_column_name = ""
    to_schema_name = ""
    to_table_name = ""
    to_column_name = ""

    # initialize
    from_schema_name = from_schema_name_IN
    from_table_name = from_table_name_IN
    from_column_name = from_column_name_IN
    to_schema_name = to_schema_name_IN
    to_table_name = to_table_name_IN
    to_column_name = to_column_name_IN

    # All names are required.

    # "from" table name
    if ( ( from_table_name is not None ) and ( from_table_name != "" ) ):

        # "from" column name
        if ( ( from_column_name is not None ) and ( from_column_name != "" ) ):

            # "to" table name
            if ( ( to_table_name is not None ) and ( to_table_name != "" ) ):

                # "to" column name
                if ( ( to_column_name is not None ) and ( to_column_name != "" ) ):

                    # add column?
                    if ( add_column_IN == True ):

                        # First, add a bigint(eger) column.
                        sql_string = "ALTER TABLE "
                        if ( ( from_schema_name is not None ) and ( from_schema_name != "" ) ):
                            sql_string += from_schema_name + "."
                        #-- END check for from_schema_name --#
                        sql_string += from_table_name
                        sql_string += " ADD COLUMN " + from_column_name + " bigint"
                        sql_string += ";"
                        print( "DEBUG - add column SQL: " + sql_string )
                        cursor_IN.execute( sql_string )

                    #-- END check to see if we add column. --#

                    # then, add the REFERENCES CONSTRAINT.
                    sql_string = "ALTER TABLE "
                    if ( ( from_schema_name is not None ) and ( from_schema_name != "" ) ):
                        sql_string += from_schema_name + "."
                    #-- END check for from_schema_name --#
                    sql_string += from_table_name
                    sql_string += " ADD CONSTRAINT " + from_table_name + "_to_" + to_table_name + "_fk"
                    sql_string += " FOREIGN KEY ( " + from_column_name + " )"
                    sql_string += " REFERENCES "
                    if ( ( to_schema_name is not None ) and ( to_schema_name != "" ) ):
                        sql_string += to_schema_name + "."
                    #-- END check for to_schema_name --#
                    sql_string += to_table_name + "( " + to_column_name + " )"
                    sql_string += ";"
                    print( "DEBUG - REFERENCES CONSTRAINT SQL: " + sql_string )
                    cursor_IN.execute( sql_string )

                    print( "Foreign key \"" + str( from_column_name ) + "\" from table \"" + str( from_table_name ) + "\" to \"" + to_table_name + "." + to_column_name + "\" created at " + str( datetime.datetime.now() ) )

                else:

                    # ERROR - no to column name passed in.
                    status_list_OUT.append( "No \"to\" column name passed in, so can't add foreign key from \"" + str( from_table_name ) + "." + str( from_column_name ) + "\" to table \"" + str( to_table_name ) + "\"." )

                #-- END check to see if table name. --#

            else:

                # ERROR - no to table name passed in.
                status_list_OUT.append( "No \"to\" table name passed in, so can't add foreign key from \"" + str( from_table_name ) + "." + str( from_column_name ) + "\"." )

            #-- END check to see if table name. --#

        else:

            # ERROR - no from column name passed in.
            status_list_OUT.append( "No \"from\" column name passed in, so can't add foreign key from table \"" + str( from_table_name ) + "\"." )

        #-- END check to see if table name. --#

    else:

        # ERROR - no from table name passed in.
        status_list_OUT.append( "No \"from\" table name passed in, so can't add foreign key." )

    #-- END check to see if table name. --#

    return status_list_OUT

#-- END function create_fk --#

print( "Function create_fk() declared at " + str( datetime.datetime.now() ) )


def create_person_fk( table_name_IN = None,
                      cursor_IN = None,
                      column_name_IN = "person_id",
                      schema_name_IN = None ):

    '''
    Create ALTER TABLE statements to add foreign key person_id to database table
        whose name is passed in.
    '''

    # return reference
    status_list_OUT = []

    # declare variables
    table_name = ""
    column_name = ""

    # initialize
    table_name = table_name_IN
    column_name = column_name_IN

    # call create_fk()
    status_list_OUT = create_fk( from_table_name_IN = table_name,
                                 from_column_name_IN = column_name,
                                 to_table_name_IN = "person",
                                 to_column_name_IN = "id",
                                 cursor_IN = cursor_IN,
                                 from_schema_name_IN = schema_name_IN,
                                 to_schema_name_IN = "ildoc" )

    return status_list_OUT

#-- END function create_person_fk --#

print( "Function create_person_fk() declared at " + str( datetime.datetime.now() ) )


#check whehter columns with int type contains non-numeric string and return a list of those column names
def check_int_column_type( df_IN,
                           column_names_IN,
                           is_verbose_IN = False):
    # map column names to counts of errors for each column
    name_to_value_map = {}
    current_value_map = {}

    for colmn in column_names_IN:
        for item in df_IN[colmn]:
            if type(item) is str:
                if not item.isdigit():
                    if ( colmn not in name_to_value_map ):
                        name_to_value_map[ colmn ] = {}
                    #-- END check to see if name in map already --#
                    current_value_map = name_to_value_map[ colmn ]

                    if ( item not in current_value_map ):
                        current_value_map[ item ] = 0
                    #-- END check to see if name in map already --#

                    # increment counter for this column
                    temp_value = current_value_map[ item ]
                    temp_value += 1
                    current_value_map[ item ] = temp_value

    if is_verbose_IN:#print( name_to_value_map )
        for name in name_to_value_map:
            print( "COLUMN: " + name )
            value_map = name_to_value_map[ name ]
            for value in value_map:
                value_count = value_map[ value ]
                print( '- ' + value + ' count = ' + str( value_count ) )

    return name_to_value_map.keys()

print( "Function check_int_column_type() declared at " + str( datetime.datetime.now() ) )


# copy raw data to additional column and modify the non-numeric value to nan (-999999)
def save_rawdata_modify_column_value( df_IN, column_names_IN ,is_verbose_IN = False, nan_default_value_IN = -999999):
    if type(column_names_IN) is not list:
        print( 'Error: The second varilabe "Column_names_IN" should be a list. Dataframe unmodified.' )
        return df_IN
    else:
        df_OUT=df_IN.copy()
        for colm_n in column_names_IN:
            if colm_n in df_OUT.columns:
                #copy the columns to column_name_raw
                raw_colm_n=colm_n + '_raw'
                raw_colm_v=df_OUT[colm_n]
                df_OUT[raw_colm_n]=raw_colm_v

                #modify the all alpha string to nan_default_value_IN
                modified_idx=[]
                ind=0
                for item in df_OUT[colm_n]:
                    if type(item) is str:
                        if not item.isdigit():
                            modified_idx.append(ind)
                    ind=ind+1
                df_OUT.ix[modified_idx,colm_n]=nan_default_value_IN
            else:
                print( "Error: The column name {} cannot be found in the dataframe. Dataframe unmodified.".format( colm_n ) )
                df_OUT=df_IN
                break
        return df_OUT

print( "Function save_rawdata_modify_column_value() declared at " + str( datetime.datetime.now() ) )

# Accepts DataFrame and column name, converts column to in with NaN replaced by -999999.
def convert_column_to_int( df_IN,
                           column_name_IN,
                           is_verbose_IN = False,
                           float_first_IN = False,
                           nan_default_value_IN = -999999 ):

    '''
    Accepts a pandas DataFrame and a column name.  Converts any NaN values in
        column to 0, then converts column to type "int", replacing the old column
        with the new int column. Returns the updated DataFrame, or None if error.
    '''

    # return reference
    df_OUT = None

    # declare variables
    current_column = None
    unique_values_list = None

    # Make sure we have something passed in.
    if ( df_IN is not None ):

        # got a column name?
        if ( ( column_name_IN is not None ) and ( column_name_IN != "" ) ):

            # convert columns to appropriate types - index, year, quarter, wage,
            #     hours, and weeks should be integers
            df_IN[ column_name_IN ] = df_IN[ column_name_IN ].fillna( nan_default_value_IN )

            # Check out unique values.
            unique_values_list = get_distinct_df_column_values( df_IN, column_name_IN, is_verbose_IN )

            # float first?
            if ( float_first_IN == True ):

                # float first...
                df_IN[ column_name_IN ] = df_IN[ column_name_IN ].astype( float )

            #-- END check to see if float first --#

            # convert column to int
            df_IN[ column_name_IN ] = df_IN[ column_name_IN ].astype( int )

            # store resulting DataFrame so you can return it.
            df_OUT = df_IN

        else:

            print( "ERROR - no column name list passed in, so don't know which column to convert." )
            df_OUT = None

    else:

        # nothing passed in.  For shame.
        print( "ERROR - no DataFrame passed in.  Nothing to do." )
        df_OUT = None

    #-- END check to see if DataFrame passed in. --#

    return df_OUT

#-- END function convert_column_to_int() --#

print( "Function convert_column_to_int() declared at " + str( datetime.datetime.now() ) )


def convert_empty_ints( cursor_IN,
                        table_name_IN = None,
                        empty_value_IN = "-999999",
                        replace_with_IN = "NULL",
                        schema_IN = "public",
                        debug_flag_IN = False ):

    '''
    Accepts database cursor, name of table we are cleaning, value used for
        empty in integer columns, value we want to replace it with, and schema in
        which the table resides.

    Looks for integer columns in the table passed in.  For each integer column,
        looks for rows that contain the empty value.  If any rows with that value,
        updates the table, setting rows with that value to the "replace_with_IN"
        value.
    '''

    # declare variables
    sql_string = ""
    pgsql_cursor = None
    integer_column_name_list = []
    columns_to_transform_list = []
    empty_value = ""
    replace_with = ""
    current_row = None

    # initialize
    pgsql_cursor = cursor_IN
    empty_value = empty_value_IN
    replace_with = replace_with_IN

    # build integer column name list.

    # SQL string to select columns in table.
    sql_string = "SELECT *"
    sql_string += " FROM information_schema.columns"
    sql_string += " WHERE table_schema = 'public'"
    sql_string += "     AND table_name = '" + table_name_IN + "'"
    sql_string += "     AND data_type LIKE '%int%'"
    sql_string += ";"

    pgsql_cursor.execute( sql_string )
    for current_row in pgsql_cursor:

        # store column name
        current_column_name = current_row[ "column_name" ]
        integer_column_name_list.append( current_column_name )

    #-- END loop over integer column names --#

    print( "Integer column name list: " + str( integer_column_name_list ) )

    list_len = len( integer_column_name_list )
    print( "Found " + str( list_len ) + " matches" )

    # for each integer column, count the empty values in that column.
    for column_name in integer_column_name_list:

        sql_string = "SELECT COUNT( * ) AS empty_count"
        #sql_string = "SELECT *"
        sql_string += " FROM " + table_name_IN
        sql_string += " WHERE " + column_name + " = " + empty_value
        sql_string += ";"

        print( sql_string )

        pgsql_cursor.execute( sql_string )
        current_row = pgsql_cursor.fetchone()

        # get empty count
        current_empty_count = current_row[ "empty_count" ]
        #print( "Empty count for column " + column_name + " = " + str( current_empty_count ) )

        if ( current_empty_count > 0 ):

            # add to transform list
            columns_to_transform_list.append( column_name )

        #-- END check to see if any rows contain empty value. --#

    #-- END loop over column names. --#

    print( "Columns to transform: " + str( columns_to_transform_list ) )

    # for each column with empties, change them to NULL.
    for column_name in columns_to_transform_list:

        sql_string = "UPDATE " + table_name_IN
        sql_string += " SET " + column_name + " = " + replace_with
        sql_string += " WHERE " + column_name + " = " + empty_value
        sql_string += ";"

        print( sql_string )

        pgsql_cursor.execute( sql_string )
        pgsql_cursor.commit()

    #-- END loop over column names. --#

#-- END function convert_empty_ints() --#

print( "Function convert_empty_ints() declared at " + str( datetime.datetime.now() ) )


def remove_invalid_person_values( connection_IN,
                                  invalid_value_list_IN,
                                  person_column_IN,
                                  person_column_type_IN = "str",
                                  debug_flag_IN = False ):

    # return reference
    status_info_OUT = {}

    # declare variables
    status_message = ""
    sql_update_string = ""
    invalid_value = ""
    invalid_values_string_list = []
    invalid_values_string = ""

    # declare variables - exception handling
    exception_type = None
    exception_value = None
    exception_traceback = None

    # must have invalid values
    if ( ( invalid_value_list_IN is not None )
        and ( isinstance( invalid_value_list_IN, list ) == True )
        and ( len( invalid_value_list_IN ) > 0 ) ):

        # got a list.  Got a column name?
        if ( ( person_column_IN is not None )
            and ( person_column_IN != "" ) ):

            # got a column name.

            try:

                # create database cursors - one for looping over person...
                person_cursor = connection_IN.cursor( cursor_factory = psycopg2.extras.DictCursor )

                # convert all values to strings, just in case.
                for invalid_value in invalid_value_list_IN:

                    invalid_values_string_list.append( str( invalid_value ) )

                #-- END loop over invalid values --#

                # for any row that contains any invalid value, set the value in
                #     the column whose name was passed in to NULL.
                sql_update_string = "UPDATE person"
                sql_update_string += " SET " + person_column_IN + " = NULL"
                sql_update_string += " WHERE " + person_column_IN + " IN ( "

                # check if string values
                if ( person_column_type_IN == "str" ):

                    # start with a quote
                    sql_update_string += "'"

                    # join values with "', '"
                    invalid_values_string = "', '".join( invalid_values_string_list )

                    # add to SQL string
                    sql_update_string += invalid_values_string

                    # end with quote
                    sql_update_string += "'"

                else:

                    # no quotes.  join values with ", "
                    invalid_values_string = ", ".join( invalid_values_string_list )

                    # add to SQL
                    sql_update_string += invalid_values_string

                #-- END check to see if string, so need quote --#

                # close IN
                sql_update_string += " );"

                # run the update and commit.
                print( "\"" + sql_update_string + "\" started at " + str( datetime.datetime.now() ) )
                person_cursor.execute( sql_update_string )
                connection_IN.commit()
                print( "\"" + sql_update_string + "\" completed at " + str( datetime.datetime.now() ) )

            except psycopg2.IntegrityError as pie:

                # Exception caught.
                print( "psycopg2.IntegrityError caught: " + str( pie ) )

                # details:
                exception_type, exception_value, exception_traceback = sys.exc_info()
                print( "- exception type: " + str( exception_type ) )
                print( "- exception value: " + str( exception_value ) )
                print( "- exception traceback: " + str( traceback.format_exc() ) )

                # And, more details:
                status_string = "values in column " + str( column_of_interest )
                status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
                status_string += str( value_map )
                print( status_string )

                # rollback
                connection_IN.rollback()

            except Exception as e:

                # Exception caught.
                print( "Exception caught: " + str( e ) )

                # details:
                exception_type, exception_value, exception_traceback = sys.exc_info()
                print( "- exception type: " + str( exception_type ) )
                print( "- exception value: " + str( exception_value ) )
                print( "- exception traceback: " + str( traceback.format_exc() ) )

                # rollback
                connection_IN.rollback()

            finally:

                person_cursor.close()

            #-- END try...except...finally --#


        else:

            # no invalid values to remove.
            status_message = "ERROR - no column name passed in, nothing to do."
            status_info_OUT[ "status_message" ] = status_message
            print( status_message )

        #-- END check to see if column name. --#

    else:

        # no invalid values to remove.
        status_message = "ERROR - no invalid values passed in, nothing to remove."
        status_info_OUT[ "status_message" ] = status_message
        print( status_message )

    #-- END check to see if invalid values passed in. --#

    return status_info_OUT

#-- END function remove_invalid_person_values()

print( "Function remove_invalid_person_values() declared at " + str( datetime.datetime.now() ) )


def merge_values_into_person( connection_IN,
                              source_table_info_list_IN,
                              person_column_IN,
                              person_column_type_IN = "str",
                              is_empty_string_value_IN = False,
                              invalid_value_list_IN = None,
                              debug_flag_IN = False,
                              limit_IN = -1,
                              person_id_list_IN = None ):

    '''
    Accepts connection, source table and column name from which you want to
        retrieve values, and the name of the column in person into which
        you want to set values if all rows in source agree.  For each person,
        looks for rows that match belong to that person in the source table.
        Retrieves all the values for the source column from matching rows.
        If all are the same, places the value in destination column in the
        person table.  If not, does nothing.

    Returns map of people who had multiple values to their values.
    '''

    # return reference
    status_info_OUT = {}
    invalid_values_OUT = {}
    status_info_OUT[ "error_map" ] = None
    status_info_OUT[ "invalid_values" ] = invalid_values_OUT

    # declare variables - configuration
    person_column_name = ""
    invalid_value = ""

    # declare variables - processing
    person_id = -1
    person_id_string = ""
    person_id_string_list = []
    person_cursor = None
    work_cursor = None
    value_map = {}
    person_counter = -1
    current_person = None
    current_person_id = -1
    current_docnbr = ""
    table_of_interest = ""
    column_of_interest = ""
    related_sql_string = ""
    current_related = None
    current_value = ""
    value_string = ""
    is_value_ok = True
    value_count = -1
    update_sql_string = ""
    error_person_map = {}
    error_person_counter = -1

    # declare variables - per-row counts
    total_value_counter = -1
    none_counter = -1
    empty_counter = -1
    invalid_value_counter = -1
    no_value_counter = -1
    single_value_counter = -1
    multi_value_counter = -1

    # declare variables - debug
    sql_string = ""
    debug_row = None
    invalid_person_count = -1

    # declare variables - clean up invalid values
    invalid_values_list = None
    cleanup_status_info = None

    # initialize
    person_column_name = person_column_IN

    # got invalid values passed in?
    if ( ( invalid_value_list_IN is not None )
        and ( isinstance( invalid_value_list_IN, list ) == True )
        and ( len( invalid_value_list_IN ) > 0 ) ):

        # yes.  Loop.
        for invalid_value in invalid_value_list_IN:

            # Add each to invalid_values_OUT mapped to empty dict.
            invalid_values_OUT[ invalid_value ] = {}

        #-- END loop over invalid values passed in. --#

    #-- END check to see if invalid values list.

    try:

        # create database cursors - one for looping over person...
        person_cursor = connection_IN.cursor( cursor_factory = psycopg2.extras.DictCursor )

        # ...and a second cursor, for querying related rows.
        work_cursor = connection_IN.cursor( cursor_factory = psycopg2.extras.DictCursor )

        # loop over person records, limiting to those where value is not already set.
        sql_string = "SELECT *"
        sql_string += " FROM person"
        sql_string += " WHERE " + person_column_name + " IS NULL"

        # do we have a person ID list?
        if ( ( person_id_list_IN is not None )
            and ( isinstance( person_id_list_IN, list ) == True )
            and ( len( person_id_list_IN ) > 0 ) ):

            # yes.  only persons with ID in that list:
            sql_string += " AND id IN ( "

            # loop over IDs.
            for person_id in person_id_list_IN:

                # convert to string (in case of integer)
                person_id_string = str( person_id )

                # add to list of string IDs.
                person_id_string_list.append( person_id_string )

            #-- END loop over IDs.

            # convert list to comma-delimited string, add to SQL.
            sql_string += ", ".join( person_id_string_list )
            sql_string += " )"

        #-- END check to see if we are limiting to a certain set of person IDs. --#

        sql_string += " ORDER BY id ASC"
        if ( limit_IN > 0 ):
            sql_string += " LIMIT " + str( limit_IN )
        #-- END check to see if limit --#
        sql_string += ";"

        if ( debug_flag_IN == True ):
            status_string = "====> DEBUG - before \"" + str( sql_string ) + "\" - " + str( datetime.datetime.now() )
            print( status_string )
        #-- END debug --#

        person_cursor.execute( sql_string )

        # loop over person rows
        person_counter = 0
        error_person_map = {}
        error_person_counter = 0
        total_value_counter = 0
        none_counter = 0
        empty_counter = 0
        invalid_value_counter = 0
        no_value_counter = 0
        single_value_counter = 0
        multi_value_counter = 0
        for current_person in person_cursor:

            # increment counter
            person_counter += 1

            # clear value_set
            value_map = {}

            # get person ID and docnbr
            current_person_id = current_person[ "id" ]
            current_docnbr = current_person[ "ildoc_docnbr" ]

            # loop over source tables
            for source_table_info in source_table_info_list_IN:

                # get column and table of interest from source_table_info.
                table_of_interest = source_table_info.get( "table_name", None )
                column_of_interest = source_table_info.get( "column_name", None )
                column_type = source_table_info.get( "column_type", "str" )

                # got a table name?
                if ( ( table_of_interest is not None ) and ( table_of_interest != "" ) ):

                    # got a column name?
                    if ( ( column_of_interest is not None ) and ( column_of_interest != "" ) ):

                        # got what we need.  Get values.
                        # get values for column of interest from related rows.
                        related_sql_string = "SELECT DISTINCT( " + column_of_interest + " ) AS unique_value"
                        related_sql_string += " FROM " + table_of_interest
                        related_sql_string += " WHERE person_id = " + str( current_person_id )
                        related_sql_string += ";"

                        if ( debug_flag_IN == True ):
                            status_string = "====> DEBUG - before \"" + str( related_sql_string ) + "\" - " + str( datetime.datetime.now() )
                            print( status_string )
                        #-- END debug --#

                        # execute SQL
                        work_cursor.execute( related_sql_string )

                        if ( debug_flag_IN == True ):
                            status_string = "====> DEBUG - after related_sql_string - " + str( datetime.datetime.now() )
                            print( status_string )
                        #-- END debug --#

                        # loop over results, converting each to string and adding it to set
                        for current_related in work_cursor:

                            # increment counter
                            total_value_counter += 1

                            # get value
                            current_value = current_related[ "unique_value" ]

                            # Run through checks to see if value is OK.
                            is_value_ok = True

                            # is value None?
                            if ( current_value is None ):

                                # None is not a valid value.
                                is_value_ok = False
                                none_counter += 1

                            #-- END check to see if None. --#

                            # empty string?
                            if ( current_value == "" ):

                                empty_counter += 1

                                # is empty string OK?
                                if ( is_empty_string_value_IN == False ):

                                    # empty string is not OK.
                                    is_value_ok = False

                                #-- END check to see if empty string is counted as a value --#

                            #-- END check to see if empty string --#

                            # is it an invalid value?
                            if current_value in invalid_values_OUT:

                                # Invalid value.
                                is_value_ok = False
                                invalid_value_counter += 1

                            #-- END check to see if invalid value --#

                            # is value OK?
                            if ( is_value_ok == True ):

                                # convert to string
                                value_string = str( current_value )

                                # add to map
                                value_map[ value_string ] = current_value

                            #-- END check to see if value is OK. --#

                        #-- END loop over relateds --#

                        if ( debug_flag_IN == True ):
                            status_string = "values in column " + str( column_of_interest )
                            status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
                            status_string += str( value_map )
                            print( status_string )
                        #-- END check if debug --#

                    else:

                        # no column name specified.
                        print( "ERROR - No column name specified for table " + str( table_of_interest ) + ".  Moving on." )

                    #-- END check to see if column name passed in. --#

                else:

                    # no column name specified.
                    print( "ERROR - No table name specified.  Moving on." )

                #-- END check to see if table name passed in. --#

            #-- END loop over table information. --#

            # how many values?
            value_count = len( value_map )
            if ( value_count == 1 ):

                single_value_counter += 1

                # great!  store it!
                for value_key, value in six.iteritems( value_map ):

                    # UPDATE!
                    update_sql_string = "UPDATE person"

                    # is value a string?
                    if ( person_column_type_IN == "str" ):

                        # string, so surround in quotes.
                        update_sql_string += " SET " + person_column_name + " = '" + str( value ) + "'"

                    else:

                        # not string - don't surround with quotes.
                        update_sql_string += " SET " + person_column_name + " = " + str( value )

                    #-- END check to see if value is string --#

                    update_sql_string += " WHERE id = " + str( current_person_id )
                    update_sql_string += ";"

                    #print( "UPDATE SQL: " + update_sql_string )

                    if ( debug_flag_IN == True ):
                        status_string = "====> DEBUG - before " + str( update_sql_string ) + " - " + str( datetime.datetime.now() )
                        print( status_string )
                    #-- END debug --#

                    # use try to capture UNIQUE constraint violations.
                    try:

                        # do it!
                        work_cursor.execute( update_sql_string )
                        connection_IN.commit()

                    except psycopg2.IntegrityError as pie:

                        # rollback
                        connection_IN.rollback()

                        # Exception caught.
                        print( "psycopg2.IntegrityError caught: " + str( pie ) )

                        # details:
                        exception_type, exception_value, exception_traceback = sys.exc_info()
                        print( "- exception type: " + str( exception_type ) )
                        print( "- exception value: " + str( exception_value ) )
                        print( "- exception traceback: " + str( traceback.format_exc() ) )

                        # And, more details:
                        status_string = "values in column " + str( column_of_interest )
                        status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
                        status_string += str( value_map )
                        print( status_string )

                        # see if we already have a count of people in this table
                        #    who share this value.

                        # update/add entry to invalid_values_OUT
                        if ( value not in invalid_values_OUT ):

                            # add a map for the value to invalid_values_OUT
                            invalid_values_OUT[ value ] = {}

                        #-- END check to see if value in invalid_values_OUT --#

                        # get map for value
                        table_to_count_map = invalid_values_OUT.get( value, None )

                        # got a count already for this table?
                        if ( table_of_interest not in table_to_count_map ):

                            # no - get count of unique users with this value in table of interest.
                            sql_string = "SELECT COUNT( DISTINCT person_id ) AS invalid_person_count"
                            sql_string += " FROM " + table_of_interest
                            sql_string += " WHERE " + column_of_interest + " = "

                            # is value a string?
                            if ( column_type == "str" ):

                                # string, so surround in quotes.
                                sql_string += "'" + str( value ) + "'"

                            else:

                                # not string - don't surround with quotes.
                                sql_string += str( value )

                            #-- END check to see if value is string --#

                            sql_string += ";"

                            # run query
                            work_cursor.execute( sql_string )

                            # retrieve count
                            for debug_row in work_cursor:

                                # got a count.
                                invalid_person_count = debug_row[ "invalid_person_count" ]

                            #-- END loop over results (should only be one). --#

                            # add count for table.
                            table_to_count_map[ table_of_interest ] = invalid_person_count

                        #-- END check to see if table's count is already stored. --#

                    #-- END try-except to catch psycopg2.IntegrityError --#

                    if ( debug_flag_IN == True ):
                        status_string = "====> DEBUG - after update_sql_string - " + str( datetime.datetime.now() )
                        print( status_string )
                    #-- END debug --#

                #-- END loop over values --#

            elif ( value_count == 0 ):

                # no value.  Make a note.
                no_value_counter += 1

            elif ( value_count > 1 ):

                multi_value_counter += 1

                if ( debug_flag_IN == True ):
                    # ERROR - multiple values - should be consistent.
                    error_person_map[ current_person_id ] = value_map
                    error_person_counter += 1
                    error_message = "ERROR - multiple values in column " + str( column_of_interest )
                    error_message += " for person " + str( current_person_id )
                    error_message += ": " + str( error_person_map )
                    print( error_message )
                #-- END DEBUG --#

            else:

                print( "ERROR - value count is neither 0, 1, or more than 1.  Should never get here." )

            #-- END check to see if one value. --#

            # output a heartbeat every 100 people, and commit.
            if ( ( person_counter % 100 ) == 0 ):

                # ... and commit.
                connection_IN.commit()

                # debug?
                if ( debug_flag_IN == True ):

                    # output brief status...
                    status_string = "====> " + str( datetime.datetime.now() )
                    status_string += " - " + str( person_counter ) + " person_records processed"
                    print( status_string )

                #-- END check to see if debug --#

            #-- END check to see if hundredth person processed. --#

            # output details every 10000 docnbr values
            if ( ( person_counter % 10000 ) == 0 ):

                # output brief status...
                status_string = "====> " + str( datetime.datetime.now() )
                status_string += " - " + str( person_counter ) + " person_records processed"
                print( status_string )

                status_string = "- error total = " + str( error_person_counter )
                status_string += "\n- value status per person: 0 = " + str( no_value_counter ) + "; 1 = " + str( single_value_counter ) + "; >1 = " + str( multi_value_counter )
                status_string += "\n- Details on no-value source rows: None = " + str( none_counter ) + "; empty = " + str( empty_counter ) + "; invalid = " + str( invalid_value_counter )
                print( status_string )

            #-- END periodic output of exists counter.

        #-- END loop over persons --#

        # clean up the invalid values
        invalid_values_list = list( six.iterkeys( invalid_values_OUT ) )
        cleanup_status_info = remove_invalid_person_values( connection_IN,
                                                            invalid_values_list,
                                                            person_column_name,
                                                            person_column_type_IN,
                                                            debug_flag_IN )

        # output summary
        status_string = "\n\n====> COMPLETE - " + str( datetime.datetime.now() )
        status_string += "\n==> " + str( person_counter ) + " person_records processed"
        status_string += "\n- error total = " + str( error_person_counter )
        status_string += "\n- value status per person: 0 = " + str( no_value_counter ) + "; 1 = " + str( single_value_counter ) + "; >1 = " + str( multi_value_counter )
        status_string += "\n- Details on values: Total = " + str( total_value_counter ) + "; None = " + str( none_counter ) + "; empty = " + str( empty_counter ) + "; invalid = " + str( invalid_value_counter )

        print( status_string )

    except psycopg2.IntegrityError as pie:

        # Exception caught.
        print( "psycopg2.IntegrityError caught: " + str( pie ) )

        # details:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print( "- exception type: " + str( exception_type ) )
        print( "- exception value: " + str( exception_value ) )
        print( "- exception traceback: " + str( traceback.format_exc() ) )

        # And, more details:
        status_string = "values in column " + str( column_of_interest )
        status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
        status_string += str( value_map )
        print( status_string )

        # rollback
        connection_IN.rollback()

    except Exception as e:

        # Exception caught.
        print( "Exception caught: " + str( e ) )

        # details:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print( "- exception type: " + str( exception_type ) )
        print( "- exception value: " + str( exception_value ) )
        print( "- exception traceback: " + str( traceback.format_exc() ) )

        # rollback
        connection_IN.rollback()

    finally:

        person_cursor.close()
        work_cursor.close()

    #-- END try...except...finally --#

    status_info_OUT[ "error_map" ] = error_person_map

    return status_info_OUT

#-- END function merge_values_into_person() --#

print( "Function merge_values_into_person() declared at " + str( datetime.datetime.now() ) )


def merge_values_into_table( connection_IN,
                             source_table_info_list_IN,
                             dest_table_IN,
                             dest_column_IN,
                             dest_column_type_IN = "str",
                             is_empty_string_value_IN = False,
                             invalid_value_list_IN = None,
                             debug_flag_IN = False,
                             limit_IN = -1,
                             dest_id_list_IN = None,
                             dest_id_column_name = "id",
                             dest_schema_IN = None ):

    '''
    Accepts connection, source table and column name from which you want to
        retrieve values, and the name of the column in person into which
        you want to set values if all rows in source agree.  For each person,
        looks for rows that match belong to that person in the source table.
        Retrieves all the values for the source column from matching rows.
        If all are the same, places the value in destination column in the
        person table.  If not, does nothing.

    Returns map of people who had multiple values to their values.
    '''

    # return reference
    status_info_OUT = {}
    invalid_values_OUT = {}
    status_info_OUT[ "error_map" ] = None
    status_info_OUT[ "invalid_values" ] = invalid_values_OUT

    # declare variables - configuration
    destination_schema_name = None
    destination_table_name = None
    destination_column_name = None
    destination_column_type = None
    invalid_value = ""
    destination_id_list = None
    destination_id_column_name = None
    join_column_list = None
    join_column_info = None

    # declare variables - join on columns
    join_on_list = None
    join_on_info = None
    join_on_source = None
    join_on_dest = None

    # declare variables - processing
    destination_cursor = None
    destination_id = -1
    destination_id_string = ""
    destination_id_string_list = []
    work_cursor = None
    value_map = {}
    destination_counter = -1
    current_record = None
    current_record_id = -1
    current_docnbr = ""
    table_of_interest = ""
    column_of_interest = ""
    related_sql_string = ""
    current_related = None
    current_value = ""
    value_string = ""
    is_value_ok = True
    value_count = -1
    update_sql_string = ""
    error_map = {}
    error_counter = -1

    # declare variables - per-row counts
    total_value_counter = -1
    none_counter = -1
    empty_counter = -1
    invalid_value_counter = -1
    no_value_counter = -1
    single_value_counter = -1
    multi_value_counter = -1

    # declare variables - debug
    sql_string = ""
    debug_row = None
    invalid_count = -1

    # declare variables - clean up invalid values
    invalid_values_list = None
    cleanup_status_info = None

    # initialize
    destination_schema_name = dest_schema_IN
    destination_table_name = dest_table_IN
    destination_column_name = dest_column_IN
    destination_column_type = dest_column_type_IN
    invalid_value = ""
    destination_id_list = dest_id_list_IN
    destination_id_column_name = dest_id_column_name_IN

    # got invalid values passed in?
    if ( ( invalid_value_list_IN is not None )
        and ( isinstance( invalid_value_list_IN, list ) == True )
        and ( len( invalid_value_list_IN ) > 0 ) ):

        # yes.  Loop.
        for invalid_value in invalid_value_list_IN:

            # Add each to invalid_values_OUT mapped to empty dict.
            invalid_values_OUT[ invalid_value ] = {}

        #-- END loop over invalid values passed in. --#

    #-- END check to see if invalid values list.

    try:

        # create database cursors - one for looping over person...
        destination_cursor = connection_IN.cursor( cursor_factory = psycopg2.extras.DictCursor )

        # ...and a second cursor, for querying related rows.
        work_cursor = connection_IN.cursor( cursor_factory = psycopg2.extras.DictCursor )

        # loop over person records, limiting to those where value is not already set.
        sql_string = "SELECT *"
        sql_string += " FROM "
        if ( ( destination_schema_name is not None ) and ( destination_schema_name != "" ) ):
            sql_string += destination_schema_name + "."
        #-- END check to see if schema name. --#
        sql_string += destination_table_name
        sql_string += " WHERE " + destination_column_name + " IS NULL"

        # do we have a destination ID list?
        if ( ( destination_id_list is not None )
            and ( isinstance( destination_id_list, list ) == True )
            and ( len( destination_id_list ) > 0 ) ):

            # yes.  only rows with ID in that list:
            sql_string += " AND " + destination_id_column_name + " IN ( "

            # loop over IDs.
            for destination_id in destination_id_list:

                # convert to string (in case of integer)
                destination_id_string = str( destination_id )

                # add to list of string IDs.
                destination_id_string_list.append( destination_id_string )

            #-- END loop over IDs.

            # convert list to comma-delimited string, add to SQL.
            sql_string += ", ".join( destination_id_string_list )
            sql_string += " )"

        #-- END check to see if we are limiting to a certain set of IDs. --#

        sql_string += " ORDER BY " + destination_id_column_name + " ASC"
        if ( limit_IN > 0 ):
            sql_string += " LIMIT " + str( limit_IN )
        #-- END check to see if limit --#
        sql_string += ";"

        if ( debug_flag_IN == True ):
            status_string = "====> DEBUG - before \"" + str( sql_string ) + "\" - " + str( datetime.datetime.now() )
            print( status_string )
        #-- END debug --#

        destionation_cursor.execute( sql_string )

        # loop over person rows
        destination_counter = 0
        error_map = {}
        error_counter = 0
        total_value_counter = 0
        none_counter = 0
        empty_counter = 0
        invalid_value_counter = 0
        no_value_counter = 0
        single_value_counter = 0
        multi_value_counter = 0
        for current_record in destination_cursor:

            # increment counter
            destination_counter += 1

            # clear value_set
            value_map = {}

            # get person ID and docnbr
            current_record_id = current_record[ destination_id_column_name ]

            # loop over source tables
            for source_table_info in source_table_info_list_IN:

                # get column and table of interest from source_table_info.
                table_of_interest = source_table_info.get( "table_name", None )
                column_of_interest = source_table_info.get( "column_name", None )
                column_type = source_table_info.get( "column_type", "str" )
                join_on_list = source_table_info.get( "join_on_list", None )

                # got a table name?
                if ( ( table_of_interest is not None ) and ( table_of_interest != "" ) ):

                    # got a column name?
                    if ( ( column_of_interest is not None ) and ( column_of_interest != "" ) ):

                        # got a JOIN ON list?
                        if ( ( join_on_list is not None )
                            and ( isinstance( join_on_list, list ) == True )
                            and ( len( join_on_list ) > 0 ) ):

                            # got what we need.  Get values.
                            # get values for column of interest from related rows.
                            related_sql_string = "SELECT DISTINCT( " + column_of_interest + " ) AS unique_value"
                            related_sql_string += " FROM " + table_of_interest

                            # !TODO - JOIN ON HERE
                            related_sql_string += " WHERE person_id = " + str( current_person_id )

                            related_sql_string += ";"

                            if ( debug_flag_IN == True ):
                                status_string = "====> DEBUG - before \"" + str( related_sql_string ) + "\" - " + str( datetime.datetime.now() )
                                print( status_string )
                            #-- END debug --#

                            # execute SQL
                            work_cursor.execute( related_sql_string )

                            if ( debug_flag_IN == True ):
                                status_string = "====> DEBUG - after related_sql_string - " + str( datetime.datetime.now() )
                                print( status_string )
                            #-- END debug --#

                            # loop over results, converting each to string and adding it to set
                            for current_related in work_cursor:

                                # increment counter
                                total_value_counter += 1

                                # get value
                                current_value = current_related[ "unique_value" ]

                                # Run through checks to see if value is OK.
                                is_value_ok = True

                                # is value None?
                                if ( current_value is None ):

                                    # None is not a valid value.
                                    is_value_ok = False
                                    none_counter += 1

                                #-- END check to see if None. --#

                                # empty string?
                                if ( current_value == "" ):

                                    empty_counter += 1

                                    # is empty string OK?
                                    if ( is_empty_string_value_IN == False ):

                                        # empty string is not OK.
                                        is_value_ok = False

                                    #-- END check to see if empty string is counted as a value --#

                                #-- END check to see if empty string --#

                                # is it an invalid value?
                                if current_value in invalid_values_OUT:

                                    # Invalid value.
                                    is_value_ok = False
                                    invalid_value_counter += 1

                                #-- END check to see if invalid value --#

                                # is value OK?
                                if ( is_value_ok == True ):

                                    # convert to string
                                    value_string = str( current_value )

                                    # add to map
                                    value_map[ value_string ] = current_value

                                #-- END check to see if value is OK. --#

                            #-- END loop over relateds --#

                            if ( debug_flag_IN == True ):
                                status_string = "values in column " + str( column_of_interest )
                                status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
                                status_string += str( value_map )
                                print( status_string )
                            #-- END check if debug --#

                        else:

                            # no column name specified.
                            print( "ERROR - No join columns specified for table " + str( table_of_interest ) + ".  Moving on." )
                        #-- END check to see if JOIN ON list. --#

                    else:

                        # no column name specified.
                        print( "ERROR - No column name specified for table " + str( table_of_interest ) + ".  Moving on." )

                    #-- END check to see if column name passed in. --#

                else:

                    # no column name specified.
                    print( "ERROR - No table name specified.  Moving on." )

                #-- END check to see if table name passed in. --#

            #-- END loop over table information. --#

            # how many values?
            value_count = len( value_map )
            if ( value_count == 1 ):

                single_value_counter += 1

                # great!  store it!
                for value_key, value in six.iteritems( value_map ):

                    # UPDATE!
                    update_sql_string = "UPDATE person"

                    # is value a string?
                    if ( person_column_type_IN == "str" ):

                        # string, so surround in quotes.
                        update_sql_string += " SET " + person_column_name + " = '" + str( value ) + "'"

                    else:

                        # not string - don't surround with quotes.
                        update_sql_string += " SET " + person_column_name + " = " + str( value )

                    #-- END check to see if value is string --#

                    update_sql_string += " WHERE id = " + str( current_person_id )
                    update_sql_string += ";"

                    #print( "UPDATE SQL: " + update_sql_string )

                    if ( debug_flag_IN == True ):
                        status_string = "====> DEBUG - before " + str( update_sql_string ) + " - " + str( datetime.datetime.now() )
                        print( status_string )
                    #-- END debug --#

                    # use try to capture UNIQUE constraint violations.
                    try:

                        # do it!
                        work_cursor.execute( update_sql_string )
                        connection_IN.commit()

                    except psycopg2.IntegrityError as pie:

                        # rollback
                        connection_IN.rollback()

                        # Exception caught.
                        print( "psycopg2.IntegrityError caught: " + str( pie ) )

                        # details:
                        exception_type, exception_value, exception_traceback = sys.exc_info()
                        print( "- exception type: " + str( exception_type ) )
                        print( "- exception value: " + str( exception_value ) )
                        print( "- exception traceback: " + str( traceback.format_exc() ) )

                        # And, more details:
                        status_string = "values in column " + str( column_of_interest )
                        status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
                        status_string += str( value_map )
                        print( status_string )

                        # see if we already have a count of people in this table
                        #    who share this value.

                        # update/add entry to invalid_values_OUT
                        if ( value not in invalid_values_OUT ):

                            # add a map for the value to invalid_values_OUT
                            invalid_values_OUT[ value ] = {}

                        #-- END check to see if value in invalid_values_OUT --#

                        # get map for value
                        table_to_count_map = invalid_values_OUT.get( value, None )

                        # got a count already for this table?
                        if ( table_of_interest not in table_to_count_map ):

                            # no - get count of unique users with this value in table of interest.
                            sql_string = "SELECT COUNT( DISTINCT person_id ) AS invalid_person_count"
                            sql_string += " FROM " + table_of_interest
                            sql_string += " WHERE " + column_of_interest + " = "

                            # is value a string?
                            if ( column_type == "str" ):

                                # string, so surround in quotes.
                                sql_string += "'" + str( value ) + "'"

                            else:

                                # not string - don't surround with quotes.
                                sql_string += str( value )

                            #-- END check to see if value is string --#

                            sql_string += ";"

                            # run query
                            work_cursor.execute( sql_string )

                            # retrieve count
                            for debug_row in work_cursor:

                                # got a count.
                                invalid_person_count = debug_row[ "invalid_person_count" ]

                            #-- END loop over results (should only be one). --#

                            # add count for table.
                            table_to_count_map[ table_of_interest ] = invalid_person_count

                        #-- END check to see if table's count is already stored. --#

                    #-- END try-except to catch psycopg2.IntegrityError --#

                    if ( debug_flag_IN == True ):
                        status_string = "====> DEBUG - after update_sql_string - " + str( datetime.datetime.now() )
                        print( status_string )
                    #-- END debug --#

                #-- END loop over values --#

            elif ( value_count == 0 ):

                # no value.  Make a note.
                no_value_counter += 1

            elif ( value_count > 1 ):

                multi_value_counter += 1

                if ( debug_flag_IN == True ):
                    # ERROR - multiple values - should be consistent.
                    error_person_map[ current_person_id ] = value_map
                    error_person_counter += 1
                    error_message = "ERROR - multiple values in column " + str( column_of_interest )
                    error_message += " for person " + str( current_person_id )
                    error_message += ": " + str( error_person_map )
                    print( error_message )
                #-- END DEBUG --#

            else:

                print( "ERROR - value count is neither 0, 1, or more than 1.  Should never get here." )

            #-- END check to see if one value. --#

            # output a heartbeat every 100 people, and commit.
            if ( ( person_counter % 100 ) == 0 ):

                # ... and commit.
                connection_IN.commit()

                # debug?
                if ( debug_flag_IN == True ):

                    # output brief status...
                    status_string = "====> " + str( datetime.datetime.now() )
                    status_string += " - " + str( person_counter ) + " person_records processed"
                    print( status_string )

                #-- END check to see if debug --#

            #-- END check to see if hundredth person processed. --#

            # output details every 10000 docnbr values
            if ( ( person_counter % 10000 ) == 0 ):

                # output brief status...
                status_string = "====> " + str( datetime.datetime.now() )
                status_string += " - " + str( person_counter ) + " person_records processed"
                print( status_string )

                status_string = "- error total = " + str( error_person_counter )
                status_string += "\n- value status per person: 0 = " + str( no_value_counter ) + "; 1 = " + str( single_value_counter ) + "; >1 = " + str( multi_value_counter )
                status_string += "\n- Details on no-value source rows: None = " + str( none_counter ) + "; empty = " + str( empty_counter ) + "; invalid = " + str( invalid_value_counter )
                print( status_string )

            #-- END periodic output of exists counter.

        #-- END loop over persons --#

        # clean up the invalid values
        invalid_values_list = list( six.iterkeys( invalid_values_OUT ) )
        cleanup_status_info = remove_invalid_person_values( connection_IN,
                                                            invalid_values_list,
                                                            person_column_name,
                                                            person_column_type_IN,
                                                            debug_flag_IN )

        # output summary
        status_string = "\n\n====> COMPLETE - " + str( datetime.datetime.now() )
        status_string += "\n==> " + str( person_counter ) + " person_records processed"
        status_string += "\n- error total = " + str( error_person_counter )
        status_string += "\n- value status per person: 0 = " + str( no_value_counter ) + "; 1 = " + str( single_value_counter ) + "; >1 = " + str( multi_value_counter )
        status_string += "\n- Details on values: Total = " + str( total_value_counter ) + "; None = " + str( none_counter ) + "; empty = " + str( empty_counter ) + "; invalid = " + str( invalid_value_counter )

        print( status_string )

    except psycopg2.IntegrityError as pie:

        # Exception caught.
        print( "psycopg2.IntegrityError caught: " + str( pie ) )

        # details:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print( "- exception type: " + str( exception_type ) )
        print( "- exception value: " + str( exception_value ) )
        print( "- exception traceback: " + str( traceback.format_exc() ) )

        # And, more details:
        status_string = "values in column " + str( column_of_interest )
        status_string += " for person " + str( current_person_id ) + " (docnbr = " + str( current_docnbr ) + "): "
        status_string += str( value_map )
        print( status_string )

        # rollback
        connection_IN.rollback()

    except Exception as e:

        # Exception caught.
        print( "Exception caught: " + str( e ) )

        # details:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print( "- exception type: " + str( exception_type ) )
        print( "- exception value: " + str( exception_value ) )
        print( "- exception traceback: " + str( traceback.format_exc() ) )

        # rollback
        connection_IN.rollback()

    finally:

        person_cursor.close()
        work_cursor.close()

    #-- END try...except...finally --#

    status_info_OUT[ "error_map" ] = error_person_map

    return status_info_OUT

#-- END function merge_values_into_table() --#

print( "Function merge_values_into_table() declared at " + str( datetime.datetime.now() ) )


def render_create_index_script_sql( sql_string_IN, index_name_IN ):

    '''
    Accepts CREATE INDEX SQL and name of incex to be created.
        Returns string that contains SQL to output a time stamp when
        the CREATE INDEX starts, run the CREATE, then output a time stamp
        when the CREATE INDEX has completed.
    '''

    # return reference
    sql_OUT = ""

    # declare variables

    sql_OUT += "-- message: starting creation of index.\n"
    sql_OUT += "DO $$\n"
    sql_OUT += "BEGIN\n"
    sql_OUT += "RAISE NOTICE '%1 - Starting creation of index: " + str( index_name_IN ) + "', NOW();\n"
    sql_OUT += "END;\n"
    sql_OUT += "$$;\n"
    sql_OUT += "\n"
    sql_OUT += "-- index: " + str( index_name_IN ) + "\n"
    sql_OUT += sql_string_IN + "\n"
    sql_OUT += "\n"
    sql_OUT += "-- message: finished last, starting next.\n"
    sql_OUT += "DO $$\n"
    sql_OUT += "BEGIN\n"
    sql_OUT += "RAISE NOTICE '----> %1 - Index created: " + str( index_name_IN ) + "', NOW();\n"
    sql_OUT += "END;\n"
    sql_OUT += "$$;\n"
    sql_OUT += "\n"

    return sql_OUT

#-- END function render_create_index_script_sql() --#

print( "Function render_create_index_script_sql() declared at " + str( datetime.datetime.now() ) )


def create_index( table_name_IN,
                  column_list_IN,
                  schema_IN = None,
                  index_name_IN = None,
                  do_run_sql_IN = False,
                  connection_IN = None,
                  cursor_IN = None,
                  script_output_IN = False ):

    '''
    Accepts table name, column name list, and optional schema and index names and flag
        to tell whether we want simple SQL, or SQL intended for a script (includes print
        "RAISE NOTICE" print statements).  Builds CREATE INDEX statement, and then either
        runs it and returns the SQL string or just returns the string.
    '''

    # return reference
    sql_string_OUT = None

    # declare variables
    index_name = None
    schema_name = None
    table_name = ""
    column_list = None
    column_name = ""
    column_list_string = ""
    index_sql_string = ""

    # got a table name?
    if ( ( table_name_IN is not None ) and ( table_name_IN != "" ) ):

        # yes.
        table_name = table_name_IN

        # got a column_list?
        if ( ( column_list_IN is not None ) and ( isinstance( column_list_IN, list ) == True ) and ( len( column_list_IN ) > 0 ) ):

            # schema name?
            if ( ( schema_IN is not None ) and ( schema_IN != "" ) ):

                schema_name = schema_IN

            #-- END check to see if schema name --#

            # yes. convert column_list to string
            column_list_string = ", ".join( column_list_IN )

            # index name?
            if ( index_name_IN is None ):

                index_name = table_name + "_"
                index_name += "_".join( column_list_IN )
                index_name += "_index"

            else:

                index_name = index_name_IN

            #-- END check to see if index name passed in. --#

            # Build SQL.
            index_sql_string = "CREATE INDEX " + index_name
            index_sql_string += " ON "

            # got schema name?
            if ( schema_name is not None ):
                index_sql_string += schema_name + "."
            #-- END check to see if schema name. --#

            index_sql_string += table_name + " ( " + column_list_string + " );"

            sql_string = index_sql_string

            # run SQL?
            if ( do_run_sql_IN == True ):

                print( "====> " + sql_string + " started at " + str( datetime.datetime.now() ) )
                cursor_IN.execute( sql_string )
                connection_IN.commit()
                print( "====> " + sql_string + " completed at " + str( datetime.datetime.now() ) )

            #-- END check to see if we are actually running SQL --#

            # render output for a script?
            if ( script_output_IN == True ):

                # Render CREATE INDEX script SQL
                sql_string = render_create_index_script_sql( index_sql_string, index_name )
                print( sql_string )

            #-- END check to see if script output --#

        else:

            # no columns specified. No Index.
            print( "No columns specified.  Can't make an INDEX." )

        #-- END check to see if columns passed in. --#

    else:

        # no table name passed in.  No INDEX.
        print( "No table name specified.  Can't make an INDEX." )

    #-- END check to see if table passed in. --#

    sql_string_OUT = sql_string

    return sql_string_OUT

#-- END function create_index() --#

print( "Function create_index() declared at " + str( datetime.datetime.now() ) )
