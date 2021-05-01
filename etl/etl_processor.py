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
import logging
import openpyxl
import sys
import time
import traceback

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

    #===========================================================================
    # ! ==> class variables
    #===========================================================================


    # debug_flag
    debug_flag = False

    # logging
    logging_level = logging.ERROR
    update_status_every = 1000


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
        self.record_iterator = None

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


    def get_record_iterator( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.record_iterator

        return value_OUT

    #-- END method get_record_iterator() --#


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
        my_worksheet = None

        # declare variables - check required
        missing_field_list = None
        required_attr_key_list = None
        current_required_key = None
        current_required_value = None

        # init
        my_debug_flag = self.debug_flag

        # get spec information
        my_worksheet = self.get_input_worksheet()
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
                missing_field_list.append( "key: {}; index: {}".format( current_required_key, current_required_index ) )
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

        # return reference
        status_OUT = None

        # status_OUT should contain a StatusContainer instance.

        # declare variables
        me = "process_records"

        raise ETLError( "In abstract-ish method ETLProcessor.{}(): OVERRIDE ME".format( me ) )

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


    def set_record_iterator( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.record_iterator = iter( value_IN )

        # clear out status variables.
        self.reset_status_information()

        # return value
        value_OUT = self.get_record_iterator()

        return value_OUT

    #-- END method set_input_worksheet() --#


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
