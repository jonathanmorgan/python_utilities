#===============================================================================
# imports
#===============================================================================


# base python libraries
import datetime
import dateutil
import json
import logging
import openpyxl
import sys
import time
import traceback

# python_utilities
from python_utilities.status.status_container import StatusContainer

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError
from python_utilities.etl.etl_processor import ETLProcessor


#===============================================================================
# class ETLObjectLoader
#===============================================================================


# lineage: object --> ETLProcessor
class ETLObjectLoader( ETLProcessor ):


    '''
    ETLObjectLoader is parent class for using an ETL spec to load data from
        different types of sources into Python objects (using attrs). All
        functionality that remains the same regardless of type of source lives
        here, is pulled in by extending this class and then building processing
        appropriate to the source.
    '''


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    #STATUS_SUCCESS = "Success!"
    #STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLObjectLoader"

    # status properties returned from store_attribute()
    PROP_WAS_ATTR_UPDATED = ETLAttribute.PROP_WAS_ATTR_UPDATED  # "was_attr_updated"
    PROP_WAS_UNKNOWN_ATTR = ETLAttribute.PROP_WAS_UNKNOWN_ATTR  # "was_unknown_attr"
    PROP_ATTR_UPDATE_DETAIL = ETLAttribute.PROP_ATTR_UPDATE_DETAIL  # "attr_update_detail"
    PROP_ATTR_NAME = ETLAttribute.PROP_ATTR_NAME  # "attr_name"
    PROP_ATTR_OLD_VALUE = ETLAttribute.PROP_ATTR_OLD_VALUE  # "attr_old_value"
    PROP_ATTR_NEW_VALUE = ETLAttribute.PROP_ATTR_NEW_VALUE  # "attr_new_value"

    # status properties for a particular record
    PROP_WAS_INSTANCE_UPDATED = "was_instance_updated"
    PROP_UPDATED_ATTR_LIST = "updated_attr_list"
    PROP_NO_CHANGE_ATTR_LIST = "no_change_attr_list"
    PROP_ERROR_ATTR_LIST = "error_attr_list"
    PROP_SUCCESS_STATUS_LIST = "success_status_list"
    PROP_ERROR_STATUS_LIST = "error_status_list"


    #===========================================================================
    # ! ==> class variables
    #===========================================================================


    # debug_flag
    debug_flag = False

    # logging
    #logging_level = logging.ERROR
    #update_status_every = 1000


    #===========================================================================
    # ! ==> class methods
    #===========================================================================


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
        #self.etl_entity = None

        # input
        #self.record_iterator = None

        # status - batch-level
        #self.status_message_list = []
        #self.latest_status = None
        #self.unknown_attrs_list = []
        #self.existing_count = 0
        #self.new_count = 0
        #self.start_dt = None

        # status - row-level
        #self.unknown_attrs_name_to_value_map = {}

        # debug
        self.debug_flag = False
        self.include_detailed_status = True

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def init_status( self, status_IN ):

        '''
        Standardized StatusContainer initialization, so it is ready for:
        - process_attr_error()
        - process_result_status()
        '''

        # return reference
        status_OUT = None

        # start with status passed in
        status_OUT = status_IN

        # init
        status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )
        status_OUT.set_detail_value( self.PROP_UPDATED_ATTR_LIST, list() )
        status_OUT.set_detail_value( self.PROP_NO_CHANGE_ATTR_LIST, list() )
        status_OUT.set_detail_value( self.PROP_ERROR_ATTR_LIST, list() )
        status_OUT.set_detail_value( self.PROP_SUCCESS_STATUS_LIST, list() )
        status_OUT.set_detail_value( self.PROP_ERROR_STATUS_LIST, list() )

        return status_OUT

    #-- END init_status() method --#


    def process_attr_error( self, status_IN, attr_spec_IN, message_IN ):

        # return reference
        status_OUT = None

        # declare variables
        error_attr_list = None
        error_status_list = None
        error_status = None

        # start with status passed in
        status_OUT = status_IN

        # get lists
        error_attr_list = status_OUT.get_detail_value( self.PROP_ERROR_ATTR_LIST, None )
        error_status_list = status_OUT.get_detail_value( self.PROP_ERROR_STATUS_LIST, None )

        # Add spec to error_attr_list.
        error_attr_list.append( attr_spec_IN )

        # make and store status
        error_status = StatusContainer()
        error_status.set_status_code( StatusContainer.STATUS_CODE_ERROR )
        error_status.add_message( message_IN )
        error_status_list.append( error_status )

        return status_OUT

    #-- END method process_attr_error()


    def process_result_status( self,
                               status_IN,
                               result_status_IN,
                               was_updated_prop_name_IN,
                               details_IN = None ):

        # return reference
        status_OUT = None

        # declare variables - information from status
        success_status_list = None
        updated_attr_list = None
        no_change_attr_list = None
        error_attr_list = None
        error_status_list = None

        # declare variables - processing
        result_success = None
        was_updated = None

        # init - start with status passed in
        status_OUT = status_IN

        # get info from status
        success_status_list = status_OUT.get_detail_value( self.PROP_SUCCESS_STATUS_LIST, None )
        updated_attr_list = status_OUT.get_detail_value( self.PROP_UPDATED_ATTR_LIST, None )
        no_change_attr_list = status_OUT.get_detail_value( self.PROP_NO_CHANGE_ATTR_LIST, None )
        error_attr_list = status_OUT.get_detail_value( self.PROP_ERROR_ATTR_LIST, None )
        error_status_list = status_OUT.get_detail_value( self.PROP_ERROR_STATUS_LIST, None )

        # success?
        result_success = result_status_IN.is_success()
        if ( result_success == True ):

            # success.
            success_status_list.append( result_status_IN )

            # was updated?
            was_updated = result_status_IN.get_detail_value( was_updated_prop_name_IN, None )
            if ( was_updated == True ):

                # updated.
                status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, True )

                # details?
                if ( details_IN is not None ):

                    # yes - store in appropriate list.
                    updated_attr_list.append( details_IN )

                #-- END check to see if details --#

            else:

                # details?
                if ( details_IN is not None ):

                    # yes - store details of thing not updated.
                    no_change_attr_list.append( details_IN )

                #-- END check to see if details --#

            #-- END check to see if updated. --#

        else:

            # error.
            error_status_list.append( result_status_IN )

            # details?
            if ( details_IN is not None ):

                # yes - store error details
                error_attr_list.append( details_IN )

            #-- END check to see if details --#

        #-- END check to see if update was a success --#

        return status_OUT

    #-- END method process_result_status() --#


    def process_value( self, value_IN, attribute_spec_IN, instance_IN ):

        '''
        takes types and transform traits of attribute spec into account to
            convert value for loading into instance.

        logic:
        - if extract and load types are set, convert from one to other.
        - if types could use a transform string, see if one is present. If so,
            use it. If not, try to transform using default.
        - if transform spec includes storing transformed value in separate
            attribute, once transform is done, add to separate attribute in
            instance.

        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "process_value"
        status_message = None
        my_debug_flag = None

        # init
        my_debug_flag = self.debug_flag

        # base behavior - return value passed in.
        value_OUT = value_IN

        # do we have a spec?
        if ( attribute_spec_IN is not None ):

            # do we have a value?
            if ( value_IN is not None ):

                # call method on attribute spec
                value_OUT = attribute_spec_IN.process_ldm_object_value( value_IN, instance_IN, self.get_default_time_zone() )

            else:

                # no value - nothing to do.
                status_message = "In {}(): no value passed in, nothing to be done.".format( me )
                if ( my_debug_flag == True ):
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            #-- check if value. --#

        else:

            # no spec - nothing to do.
            status_message = "In {}(): no spec for value, nothing to be done.".format( me )
            if ( my_debug_flag == True ):
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

        #-- END check if spec --#

        return value_OUT

    #-- END method process_value() --#


    def store_attribute( self, instance_IN, attr_name_IN, attr_value_IN ):

        '''
        postconditions: In StatusContainer returned, expects
            self.PROP_WAS_ATTR_UPDATED to be set to boolean True if updated,
            False if not.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "store_attribute"

        status_OUT = ETLAttribute.store_attribute_in_ldm_instance( instance_IN, attr_name_IN, attr_value_IN )

        return status_OUT

    #-- END method store_attribute() --#


#-- END class ETLObjectLoader --#
