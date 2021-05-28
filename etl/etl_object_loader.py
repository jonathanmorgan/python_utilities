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
    PROP_WAS_ATTR_UPDATED = "was_attr_updated"
    PROP_WAS_UNKNOWN_ATTR = "was_unknown_attr"
    PROP_ATTR_UPDATE_DETAIL = "attr_update_detail"
    PROP_ATTR_NAME = "attr_name"
    PROP_ATTR_OLD_VALUE = "attr_old_value"
    PROP_ATTR_NEW_VALUE = "attr_new_value"

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
        work_value = None
        spec_json = None
        json_string = None
        in_data_type = None
        in_logical_type = None
        transform_pattern = None
        transform_to_attr_name = None
        out_data_type = None

        # init
        my_debug_flag = self.debug_flag

        # base behavior - return value passed in.
        value_OUT = value_IN

        # do we have a spec?
        if ( attribute_spec_IN is not None ):

            # do we have a value?
            if ( value_IN is not None ):

                if ( my_debug_flag == True ):
                    spec_json = attribute_spec_IN.to_json()
                    json_string = json.dumps( spec_json, indent = 4, sort_keys = True )
                    status_message = "ETLAttribute JSON string:\n{json_string}".format( json_string = json_string )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # retrieve info from spec.
                in_data_type = attribute_spec_IN.get_extract_data_type()
                in_logical_type = attribute_spec_IN.get_extract_logical_type()
                out_data_type = attribute_spec_IN.get_load_attr_data_type()
                transform_pattern = attribute_spec_IN.get_transform_conversion_string()
                transform_to_attr_name = attribute_spec_IN.get_transform_to_attr_name()

                # is there an output data type we transform to...
                if ( ( out_data_type is not None ) and ( out_data_type != "" ) ):

                    # there is an output data type. Process based on output
                    #     type.
                    # simple type - int
                    if ( out_data_type == ETLAttribute.DATA_TYPE_INT ):

                        # convert to int
                        value_OUT = self.clean_value(
                            value_IN,
                            desired_type_IN = ETLAttribute.DATA_TYPE_INT
                        )

                        if ( my_debug_flag == True ):
                            status_message = "translated {} to int {}".format( value_IN, value_OUT )
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                    # simple type - string
                    elif ( out_data_type == ETLAttribute.DATA_TYPE_STRING ):

                        # convert to string
                        value_OUT = self.clean_value(
                            value_IN,
                            desired_type_IN = ETLAttribute.DATA_TYPE_STRING
                        )

                        if ( my_debug_flag == True ):
                            status_message = "translated {} to string {}".format( value_IN, value_OUT )
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                    # complex type - datetime.datetime
                    elif ( out_data_type == ETLAttribute.DATA_TYPE_DATETIME_DATETIME ):

                        # make sure string is clean first.
                        work_value = self.clean_value(
                            value_IN,
                            desired_type_IN = ETLAttribute.DATA_TYPE_STRING
                        )

                        # is there a value?
                        if ( ( work_value is not None ) and ( work_value != "" ) ):

                            # is there a transform pattern?
                            if ( ( transform_pattern is not None ) and ( transform_pattern != "" ) ):

                                # parse using pattern.
                                value_OUT = datetime.datetime.strptime( work_value, transform_pattern )

                            else:

                                try:

                                    # no pattern, let dateutil try to figure it out.
                                    value_OUT = dateutil.parser.parse( work_value )

                                except dateutil.parser.ParserError as pe:

                                    # bad date string. Log and print it...
                                    status_message = "unable to parse date string value {date_value} ( exception: {parse_exception} ); transform_pattern: {pattern}; Returning None.".format(
                                        date_value = work_value,
                                        parse_exception = pe,
                                        pattern = transform_pattern
                                    )
                                    self.output_debug( status_message, method_IN = me, do_print_IN = True )

                                    # ...return value passed in.
                                    value_OUT = value_IN

                                #-- END try...except around date parsing --#

                            #-- check if transform pattern. --#

                        else:

                            # no value passed in, just return it.
                            value_OUT = value_IN

                        #-- END check to see if value is parse-able. --#

                        if ( my_debug_flag == True ):
                            status_message = "translated {} to datetime {}".format( value_IN, value_OUT )
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                    # unknown type.
                    else:

                        # unknown output type - nothing to do.
                        status_message = "In {}(): unknown output type \"{}\", nothing to be done.".format( me, out_data_type )
                        if ( my_debug_flag == True ):
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                    #-- END check to see what type we want --#

                    # are we transforming to a separate attribute?
                    if ( ( transform_to_attr_name is not None ) and ( transform_to_attr_name != "" ) ):

                        if ( my_debug_flag == True ):
                            status_message = "storing translated value {} in attr {}".format( value_OUT, transform_to_attr_name )
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                        # we are. store transformed value there...
                        self.store_attribute( instance_IN, transform_to_attr_name, value_OUT )

                        # ...then return value passed in.
                        value_OUT = value_IN

                    #-- END check to see if we store transformed value in separate attribute. --#

                else:

                    # no output type - nothing to do.
                    status_message = "In {}(): no output type, nothing to be done.".format( me )
                    if ( my_debug_flag == True ):
                        self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                #-- END check to see if output type set. --#

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

        # return reference
        status_OUT = None

        # declare variables
        me = "store_attribute"
        status_message = None
        my_debug_flag = None
        do_detailed_status = False
        my_etl_spec = None
        my_class = None
        attr_exists = None
        current_value = None
        unknown_attr_name_to_value_map = None
        extra_data_json = None
        has_extra_data_changed = None

        # init
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        do_detailed_status = self.include_detailed_status
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have an instance?
        if ( ( instance_IN is not None ) and ( instance_IN != "" ) ):

            # do we have an attribute name?
            if ( ( attr_name_IN is not None ) and ( attr_name_IN != "" ) ):

                # we do. Get info from spec.
                my_etl_spec = self.get_etl_entity()
                my_class = my_etl_spec.get_load_class()

                # is this name in the instance?
                attr_exists = hasattr( my_class, attr_name_IN )

                if ( my_debug_flag == True ):
                    status_message = "- attr_name = {attr_name} ( exists?: {attr_exists} ); attr_value = {attr_value}".format(
                        attr_name = attr_name_IN,
                        attr_exists = attr_exists,
                        attr_value = attr_value_IN
                    )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # if name in instance, store value. If not, add to list for processing.
                if ( attr_exists == True ):

                    # update status
                    status_OUT.set_detail_value( self.PROP_WAS_UNKNOWN_ATTR, False )

                    # get existing value
                    current_value = getattr( instance_IN, attr_name_IN )

                    # attribute update detail
                    status_message = "{attr_name}: {old_value} ==> {new_value}.".format(
                        attr_name = attr_name_IN,
                        old_value = current_value,
                        new_value = attr_value_IN
                    )
                    status_OUT.set_detail_value( self.PROP_ATTR_UPDATE_DETAIL, status_message )

                    # changed?
                    if ( current_value != attr_value_IN ):

                        # changed - make a note in status.
                        setattr( instance_IN, attr_name_IN, attr_value_IN )
                        status_OUT.set_detail_value( self.PROP_WAS_ATTR_UPDATED, True )

                        # status message
                        status_message = "model attribute {attr_name} updated from {old_value} to {new_value}.".format(
                            attr_name = attr_name_IN,
                            old_value = current_value,
                            new_value = attr_value_IN
                        )
                        status_OUT.add_message( status_message )
                        self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )

                    else:

                        # not changed - no need to do anything.
                        status_OUT.set_detail_value( self.PROP_WAS_ATTR_UPDATED, False )
                        status_message = "model attribute {attr_name} NOT changed (current: {old_value}; new: {new_value}), so NOT updated.".format(
                            attr_name = attr_name_IN,
                            old_value = current_value,
                            new_value = attr_value_IN
                        )
                        status_OUT.add_message( status_message )
                        self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )

                    #-- END check if changed. --#

                else:

                    # get existing value
                    current_value = instance_IN.get_extra_data_attr_value( attr_name_IN )

                    # attribute update detail
                    status_message = "X {attr_name}: {old_value} ==> {new_value}.".format(
                        attr_name = attr_name_IN,
                        old_value = current_value,
                        new_value = attr_value_IN
                    )
                    status_OUT.set_detail_value( self.PROP_ATTR_UPDATE_DETAIL, status_message )

                    # attribute does not exist. Add to the unknown attribute map.
                    unknown_attr_name_to_value_map = self.get_unknown_attrs_name_to_value_map()
                    unknown_attr_name_to_value_map[ attr_name_IN ] = attr_value_IN

                    # update status
                    status_OUT.set_detail_value( self.PROP_WAS_UNKNOWN_ATTR, True )
                    status_message = "attribute {attr_name} NOT in model, adding to extra data (current: {old_value}; new: {new_value}).".format(
                        attr_name = attr_name_IN,
                        old_value = current_value,
                        new_value = attr_value_IN
                    )
                    status_OUT.add_message( status_message )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )

                    # update the value for this attribute in the extra_data
                    #     JSONField.
                    has_extra_data_changed = instance_IN.update_extra_data_attr( attr_name_IN, attr_value_IN )

                    # check if unknown attribute already present, if so,
                    #    only set updated flag if value was different.

                    # did it change?
                    if ( has_extra_data_changed == True ):

                        # it has!
                        status_OUT.set_detail_value( self.PROP_WAS_ATTR_UPDATED, True )

                    else:

                        # no change!
                        status_OUT.set_detail_value( self.PROP_WAS_ATTR_UPDATED, False )

                    #-- END check to see if extra data changed. --#

                #-- END check if has attr --#

                # detailed status?
                if ( do_detailed_status == True ):

                    # store details
                    status_OUT.set_detail_value( self.PROP_ATTR_NAME, attr_name_IN )
                    status_OUT.set_detail_value( self.PROP_ATTR_OLD_VALUE, current_value )
                    status_OUT.set_detail_value( self.PROP_ATTR_NEW_VALUE, attr_value_IN )

                #-- END detailed status --#

            else:

                # no name. error.
                status_message = "ERROR in {}(): no attribute name passed in, nothing to be done.".format( me )
                self.output_log_message( status_message, me, log_level_code_IN = logging.ERROR, do_print_IN = True )

                # raise ETLError.
                raise ETLError( status_message )

            #-- END check to see if attribute name passed in --#

        else:

            # no instance. error.
            status_message = "ERROR in {}(): no load instance passed in, nothing to be done.".format( me )
            self.output_log_message( status_message, me, log_level_code_IN = logging.ERROR, do_print_IN = True )

            # raise ETLError.
            raise ETLError( status_message )

        #-- END check to see if instance --#

        return status_OUT

    #-- END method store_attribute() --#


#-- END class ETLObjectLoader --#
