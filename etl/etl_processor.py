# TODO
# - add timing information - keep track of:
#     - // start
#     - // time and total elapsed at each periodic output.
#     - elapsed for just period
#     - average per item.

#===============================================================================
# imports
#===============================================================================


# base python libraries
import datetime
import dateutil
import itertools
import logging
import openpyxl
import sys
import time
import traceback

# other packages
import pytz

# python_utilities
from python_utilities.logging.logging_helper import LoggingHelper

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError


#===============================================================================
# class ETLProcessor
#===============================================================================


# lineage: object
class ETLProcessor( object ):


    '''
    ETLProcessor is parent class for using an ETL spec to load data. All
        functionality that remains the same independent of type of source or
        destination lives here, is pulled in by extending this class and then
        building processing appropriate to the source/destination.
    '''


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLProcessor"

    # properties in a record
    RECORD_PROP_NAME_LIST_VALUE = "list_value"

    # status properties
    STATUS_PROP_PROCESSED_RECORD_COUNT = "processed_record_count"
    STATUS_PROP_UPDATE_ERROR_COUNT = "update_error_count"
    STATUS_PROP_UPDATE_SUCCESS_COUNT = "update_success_count"
    STATUS_PROP_UPDATED_RECORD_COUNT = "updated_record_count"

    #===========================================================================
    # ! ==> class variables
    #===========================================================================


    # debug_flag
    debug_flag = False

    # logging
    logging_level = logging.ERROR
    update_status_every = 1000

    # time zones (sigh) - default to UTC.
    default_time_zone = pytz.UTC

    # list of time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    # example loading EST zone:
    #default_time_zone = pytz.timezone( "America/New_York" )


    #===========================================================================
    # ! ==> class methods
    #===========================================================================


    @classmethod
    def clean_value( cls, value_IN, desired_type_IN = ETLAttribute.DATA_TYPE_STRING ):

        # return reference
        value_OUT = None

        # declare variables
        me = "clean_value ( {} )".format( cls )

        # got a None?
        if ( value_IN is not None ):

            # seed output with input.
            value_OUT = value_IN

            # clean based on desired type.
            if ( desired_type_IN == ETLAttribute.DATA_TYPE_STRING ):

                # type of string?
                if ( isinstance( value_OUT, str ) == False ):

                    # no - cast to string.
                    value_OUT = str( value_OUT )

                #-- END check to see if type of string. --#

                # always strip strings
                if ( isinstance( value_OUT, str ) == True ):

                    # strip white space
                    value_OUT = value_OUT.strip()

                #-- END check to see if string. --#

            elif ( desired_type_IN == ETLAttribute.DATA_TYPE_INT ):

                # make sure it is an int
                # type of int?
                if ( isinstance( value_OUT, int ) == False ):

                    # always strip strings
                    if ( isinstance( value_OUT, str ) == True ):

                        # strip white space
                        value_OUT = value_OUT.strip()

                    #-- END check to see if string. --#

                    # cast to int.
                    value_OUT = int( value_OUT )

                #-- END check to see if type of string. --#

            else:

                output_debug( "in {}: Unknown desired type \"{}\"".format( me, desired_type_IN ) )

            #-- END process based on desired type --#

        else:

            # nothing to do.
            value_OUT = value_IN

        #-- END check if None --#

        return value_OUT

    #-- END function clean_value() --#


    #===========================================================================
    # ! ==> __init__() method - instance variables
    #===========================================================================


    def __init__( self ):

        '''
        Constructor
        '''

        # call parent's __init__()
        super().__init__()

        # spec
        self.etl_entity = None

        # input
        self.record_list = None
        #self.record_iterator = None

        # status - batch-level
        self.status_message_list = []
        self.latest_status = None
        self.unknown_attrs_list = []
        self.existing_count = 0
        self.new_count = 0
        self.start_dt = None

        # status - row-level
        self.unknown_attrs_name_to_value_map = {}
        self.missing_field_list = []

        # debug
        self.debug_flag = False

    #-- END constructor --#

    @classmethod
    def get_default_time_zone( cls ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = cls.default_time_zone

        return value_OUT

    #-- END classmethod get_default_time_zone() --#


    @classmethod
    def set_default_time_zone( cls, value_IN ):

        # return reference
        value_OUT = None

        # store value
        cls.default_time_zone = value_IN

        # return value
        value_OUT = cls.get_default_time_zone()

        return value_OUT

    #-- END classmethod set_default_time_zone() --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def add_status_message( self, value_IN, do_print_IN = False ):

        # declare variables
        status_list = None
        debug_flag = None

        # init
        debug_flag = self.debug_flag

        # get status list
        status_list = self.get_status_message_list()

        # add status.
        status_list.append( value_IN )

        # print?
        if ( ( do_print_IN == True ) or ( debug_flag == True ) ):
            # print
            print( value_IN )
        #-- END print or DEBUG --#

    #-- END method add_status_message() --#


    def get_etl_entity( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.etl_entity

        return value_OUT

    #-- END method get_etl_entity() --#


    def get_missing_field_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.missing_field_list

        return value_OUT

    #-- END method get_missing_field_list() --#


    def get_record_count( self ):

        # return reference
        value_OUT = None

        # declare variables
        my_record_list = None

        # get record list
        my_record_list = self.record_list

        # do we have a list?
        if ( my_record_list is not None ):

            # get len
            value_OUT = len( my_record_list )

        else:

            # no list - return None
            value_OUT = None

        #-- END check to see if list stored within. --#

        return value_OUT

    #-- END method get_record_count() --#


    def get_record_iterator( self, start_index_IN = None, record_count_IN = None, use_islice_IN = False ):

        # return reference
        value_OUT = None

        # declare variables
        my_record_list = None
        my_iterator = None

        # do we have a record list?
        my_record_list = self.get_record_list()
        if ( my_record_list is not None ):

            # process a subset?
            if ( ( start_index_IN is not None )
                or ( record_count_IN is not None ) ):

                # are we using itertools.islice()? (leaving this here because it is
                #     interesting, but probably not the right answer in most cases)
                # - main takeaway - Slicing list before making iterator is usually better. islice() traverses iterator to get to the first item, so the farther into the list the first item is, the more processing you do to get there.
                if ( use_islice_IN != True ):

                    # just slice the list, then make an iterator from the result.
                    # - start is 0-indexed
                    # - stop stops at and does not return the index you pass to stop (so
                    #     if you want from 0 to 9, start is 0, count is 10). If you want
                    #     from 4 to 9, start index is 4, count is 6, so stop will be 10).
                    if ( ( start_index_IN is not None )
                        and ( record_count_IN is not None ) ):

                        # we have both start and count.
                        start_index = start_index_IN
                        stop_index = start_index_IN + record_count_IN

                    elif ( ( start_index_IN is not None )
                        and ( record_count_IN is None ) ):

                        # we have start, no count.
                        start_index = start_index_IN
                        stop_index = None

                    elif ( ( start_index_IN is None )
                        and ( record_count_IN is not None ) ):

                        # no start, just count (limit).
                        start_index = 0
                        stop_index = record_count_IN

                    #-- END check to see how to set start and stop.

                    # slice list...
                    my_record_list = my_record_list[ start_index : stop_index ]

                    # ...make iterator.
                    my_iterator = iter( my_record_list )

                else:

                    # using itertools.islice() - leaving this here because it is
                    #     interesting, but probably not the right answer in most
                    #     cases
                    # - main takeaway - Slicing list before making iterator is usually better. islice() traverses iterator to get to the first item, so the farther into the list the first item is, the more processing you do to get there.
                    # - https://stackoverflow.com/questions/18048698/efficient-iteration-over-slice-in-python
                    # - https://docs.python.org/3/library/itertools.html#itertools.islice

                    # get iterator
                    my_iterator = iter( my_record_list )

                    # we have been asked to subset using itertools.islice():
                    # - start is 0-indexed
                    # - stop stops at and does not return the index you pass to stop (so
                    #     if you want from 0 to 9, start is 0, count is 10). If you want
                    #     from 4 to 9, start index is 4, count is 6, so stop will be 10).
                    if ( ( start_index_IN is not None )
                        and ( record_count_IN is not None ) ):

                        # we have both start and count.
                        start_index = start_index_IN
                        stop_index = start_index_IN + record_count_IN

                    elif ( ( start_index_IN is not None )
                        and ( record_count_IN is None ) ):

                        # we have start, no count.
                        start_index = start_index_IN
                        stop_index = None

                    elif ( ( start_index_IN is None )
                        and ( record_count_IN is not None ) ):

                        # no start, just count (limit).
                        start_index = 0
                        stop_index = record_count_IN

                    #-- END check to see how to set start and stop.

                    # islice the iterator
                    my_iterator = itertools.islice( my_iterator, start_index, stop_index )

                #-- END check to see if we use itertools.islice() --#

            else:

                # no subsetting, just make and return iterator.
                my_iterator = iter( my_record_list )

            #-- END check to see if we have been asked to subset. --#

            # return the result
            value_OUT = my_iterator

        else:

            # we do not have a record list - return None.
            value_OUT = None

        #-- END check if associated list. --#

        return value_OUT

    #-- END method get_record_iterator() --#


    def get_record_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.record_list

        return value_OUT

    #-- END method get_record_list() --#


    def get_status_message_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.status_message_list

        return value_OUT

    #-- END method get_status_message_list() --#


    def get_unknown_attrs_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.unknown_attrs_list

        return value_OUT

    #-- END method get_unknown_attrs_list() --#


    def get_unknown_attrs_name_to_value_map( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.unknown_attrs_name_to_value_map

        return value_OUT

    #-- END method get_unknown_attrs_name_to_value_map() --#


    def get_value_for_key( self, record_IN, key_IN ):

        # return reference
        spec_OUT = None

        # declare variables
        me = "get_value_for_key"

        raise ETLError( "In abstract-ish method ETLProcessor.{}(): OVERRIDE ME".format( me ) )

        return spec_OUT

    #-- END class method get_value_for_key() --#


    def has_required( self, record_IN ):

        '''
        Accepts record to check for required fields. For each required field,
            looks up value in record, makes sure there is a value. If all
            required values are present, then returns True. If not, returns
            False.
        '''

        # return reference
        has_required_OUT = False

        # declare variables
        me = "has_required"
        status_message = None
        my_debug_flag = None

        # declare variables - check required
        missing_field_list = None
        required_attr_key_list = None
        current_required_key = None
        current_required_value = None

        # init
        my_debug_flag = self.debug_flag

        # get spec information
        my_etl_spec = self.get_etl_entity()
        required_attr_key_list = my_etl_spec.get_required_attr_key_set()

        # ==> check required.
        has_required_OUT = True
        missing_field_list = []

        # loop over required keys
        for current_required_key in required_attr_key_list:

            if ( my_debug_flag == True ):
                status_message = "Current required key: {}".format( current_required_key )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

            # retrieve value for key.
            current_required_value = self.get_value_for_key( record_IN, current_required_key )

            if ( my_debug_flag == True ):
                status_message = "- Current required value: {}".format( current_required_value )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

            # Is it set? Needs to not be None, and not be empty.
            if ( ( current_required_value is None ) or ( current_required_value == "" ) ):

                # not set.
                missing_field_list.append( current_required_key )
                has_required_OUT = False

                if ( my_debug_flag == True ):
                    status_message = "- Current value MISSING!"
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            else:

                # set.
                if ( my_debug_flag == True ):
                    status_message = "- Current value FOUND!"
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            #-- END check if value is present. --#

        #-- END loop over required keys --#

        # got missing fields?
        if ( len( missing_field_list ) > 0 ):

            # yes. Store the list.
            self.set_missing_field_list( missing_field_list )

        #-- END check to see if missing field list. --#

        return has_required_OUT

    #-- END method has_required() --#


    def output_log_message( self, message_IN, method_IN = "", indent_with_IN = "", log_level_code_IN = logging.DEBUG, do_print_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
        does nothing for now.
        '''

        # declare variables
        logger_name = None
        do_print = False

        # init
        logger_name = self.MY_LOGGER_NAME
        do_print = do_print_IN
        if ( do_print is None ):

            # parameter not set, default to instance debug flag.
            do_print = self.debug_flag

        #-- END check to see if print parameter set --#

        # got a message?
        if ( message_IN ):

            # call LoggingHelper method
            LoggingHelper.log_message( message_IN,
                                    method_IN = method_IN,
                                    indent_with_IN = indent_with_IN,
                                    logger_name_IN = logger_name,
                                    log_level_code_IN = log_level_code_IN,
                                    do_print_IN = do_print )

        #-- END check to see if message. --#

    #-- END method output_log_message() --#


    def output_debug( self, message_IN, method_IN = "", indent_with_IN = "", do_print_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
        does nothing for now.
        '''

        # declare variables
        logger_name = None
        do_print = False

        # init
        logger_name = self.MY_LOGGER_NAME
        do_print = do_print_IN
        if ( do_print is None ):

            # parameter not set, default to instance debug flag.
            do_print = self.debug_flag

        #-- END check to see if print parameter set --#

        # got a message?
        if ( message_IN ):

            # call LoggingHelper method
            LoggingHelper.output_debug( message_IN,
                                        method_IN = method_IN,
                                        indent_with_IN = indent_with_IN,
                                        logger_name_IN = logger_name,
                                        do_print_IN = do_print )

        #-- END check to see if message. --#

    #-- END method output_debug() --#


    def process_records( self, start_index_IN = None, index_count_IN = None ):

        '''
        Postconditions: StatusContainer returned should contain:
        - the count of the records processed during processing in a
            StatusContainer detail property named
            STATUS_PROP_PROCESSED_RECORD_COUNT ( "processed_record_count" ).
        - the count of the records with errors during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATE_ERROR_COUNT ( "update_error_count" ).
        - the count of the records successfully processed during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATE_SUCCESS_COUNT ( "update_success_count" ).
        - the count of the records updated during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATED_RECORD_COUNT ( "updated_record_count" ).
        '''

        # return reference
        status_OUT = None

        # status_OUT should contain a StatusContainer instance.

        # declare variables
        me = "process_records"

        # Example of status
        status_message = "In abstract-ish method ETLProcessor.{}(): OVERRIDE ME".format( me )
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
        status_OUT.add_message( status_message )
        status_OUT.set_detail_value( self.STATUS_PROP_PROCESSED_RECORD_COUNT, 0 )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATE_ERROR_COUNT, 0 )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATE_SUCCESS_COUNT, 0 )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATED_RECORD_COUNT, 0 )

        raise ETLError( status_message )

        return status_OUT

    #-- END class method initialize_etl() --#


    def reset_record_information( self ):

        # status - row-level
        self.unknown_attrs_name_to_value_map = {}
        self.set_missing_field_list( [] )

    #-- END method reset_record_information() --#


    def reset_status_information( self ):

        # reset status variables. - worksheet-level
        self.status_message_list = []
        self.latest_status = None
        self.unknown_attrs_list = []
        self.existing_count = 0
        self.new_count = 0
        self.start_dt = None

        # status - row-level
        self.reset_record_information()

    #-- END method reset_status_information() --#


    def set_etl_entity( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.etl_entity = value_IN

        # return value
        value_OUT = self.get_etl_entity()

        return value_OUT

    #-- END method set_etl_entity() --#


    def set_missing_field_list( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.missing_field_list = value_IN

        # return value
        value_OUT = self.get_missing_field_list()

        return value_OUT

    #-- END method set_missing_field_list() --#


    def set_record_list( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.record_list = value_IN

        # clear out status variables.
        self.reset_status_information()

        # return value
        value_OUT = self.get_record_list()

        return value_OUT

    #-- END method set_record_list() --#


    def set_status_message_list( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.status_message_list = value_IN

        # return value
        value_OUT = self.get_status_message_list()

        return value_OUT

    #-- END method set_status_message_list() --#


    def set_unknown_attrs_list( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.unknown_attrs_list = value_IN

        # return value
        value_OUT = self.get_unknown_attrs_list()

        return value_OUT

    #-- END method set_unknown_attrs_list() --#


    def set_unknown_attrs_name_to_value_map( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.unknown_attrs_name_to_value_map = value_IN

        # return value
        value_OUT = self.get_unknown_attrs_name_to_value_map()

        return value_OUT

    #-- END method set_unknown_attrs_name_to_value_map() --#


#-- END class ETLProcessor --#
