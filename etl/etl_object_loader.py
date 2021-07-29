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
