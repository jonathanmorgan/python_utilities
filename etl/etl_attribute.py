#===============================================================================
# imports
#===============================================================================


# base python libraries
import datetime
import importlib
import json
import logging
import pytz
import sys
import time
import traceback

# other packages
import dateutil
import dateutil.parser
# import updated because of this: https://stackoverflow.com/questions/48632176/python-dateutil-attributeerror-module-dateutil-has-no-attribute-parse

# python_utilities
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer


#===============================================================================
# class ETLAttribute
#===============================================================================

# lineage: object
class ETLAttribute( object ):


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "

    # DEBUG - changed to class variable "debug_flag", below.
    #DEBUG_FLAG = False

    # logger name
    MY_LOGGER_NAME = "etl_attribute"

    # data types
    DATA_TYPE_STRING = "string"
    DATA_TYPE_INT = "int"
    DATA_TYPE_DATETIME_DATE = "datetime.date"
    DATA_TYPE_DATETIME_DATETIME = "datetime.datetime"

    # logical types
    LOGICAL_TYPE_STRING_DATE = "string_date"
    LOGICAL_TYPE_STRING_DATETIME = "string_datetime"
    LOGICAL_TYPE_STRING_DATETIME_ISO_8601 = "string_datetime_ISO_8601"

    # related data types
    RELATED_TYPE_DICT = "dict"
    RELATED_TYPE_LIST = "list"
    RELATED_TYPE_LIST_OF_DICTS = "list_of_dicts"
    RELATED_TYPE_LIST_OF_VALUES = "list_of_values"
    RELATED_TYPE_VALUE_TO_TYPE_MAP = dict()
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_DICT ] = dict
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_LIST ] = list
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_LIST_OF_DICTS ] = list
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_LIST_OF_VALUES ] = list

    # Reusable format strings
    FORMAT_DATETIME_ISO_8601 = "ISO-8601"

    # status properties returned from store_attribute_in_object()
    PROP_WAS_ATTR_UPDATED = "was_attr_updated"
    PROP_WAS_UNKNOWN_ATTR = "was_unknown_attr"
    PROP_ATTR_UPDATE_DETAIL = "attr_update_detail"
    PROP_ATTR_NAME = "attr_name"
    PROP_ATTR_OLD_VALUE = "attr_old_value"
    PROP_ATTR_NEW_VALUE = "attr_new_value"


    #===========================================================================
    # ! ==> class variables
    #===========================================================================


    # debug_flag
    debug_flag = False

    # logging
    logging_level = logging.ERROR

    # status
    include_detailed_status = False

    #===========================================================================
    # ! ==> class methods
    #===========================================================================


    @classmethod
    def clean_value( cls, value_IN, desired_type_IN = DATA_TYPE_STRING ):

        # return reference
        value_OUT = None

        # declare variables
        me = "clean_value ( {} )".format( cls )

        # got a None?
        if ( value_IN is not None ):

            # seed output with input.
            value_OUT = value_IN

            # clean based on desired type.
            if ( desired_type_IN == cls.DATA_TYPE_STRING ):

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

            elif ( desired_type_IN == cls.DATA_TYPE_INT ):

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

                LoggingHelper.output_debug( "in {}: Unknown desired type \"{}\"".format( me, desired_type_IN ) )

            #-- END process based on desired type --#

        else:

            # nothing to do.
            value_OUT = value_IN

        #-- END check if None --#

        return value_OUT

    #-- END function clean_value() --#


    @classmethod
    def create_transform_attribute(
        cls,
        extract_prop_IN = None,
        load_prop_IN = None,
        transform_to_attr_name_IN = None,
        extract_data_type_IN = DATA_TYPE_STRING,
        extract_logical_type_IN = None,
        is_required_IN = None,
        load_attr_data_type_IN = None,
        conversion_string_IN = None
    ):

        # return reference
        attr_OUT = None

        # declare variables
        temp_etl_attr = None

        # init
        temp_etl_attr = ETLAttribute()

        #----------------------------------------------------------------------#
        # extract
        #----------------------------------------------------------------------#

        temp_etl_attr.set_extract_name( extract_prop_IN )
        temp_etl_attr.set_extract_data_type( extract_data_type_IN )

        if ( extract_logical_type_IN is not None ):
            temp_etl_attr.set_extract_logical_type( extract_logical_type_IN )
        #-- END check to see if logical type --#

        if ( is_required_IN is not None ):
            temp_etl_attr.set_extract_is_required( is_required_IN )
        #-- END check if is required --#

        #----------------------------------------------------------------------#
        # transform
        #----------------------------------------------------------------------#

        if ( conversion_string_IN is not None ):
            temp_etl_attr.set_transform_conversion_string( conversion_string_IN )
        #-- END check if conversion string passed in --#

        if ( transform_to_attr_name_IN is not None ):
            temp_etl_attr.set_transform_to_attr_name( transform_to_attr_name_IN )
        #-- END check if transform_to_attr_name --#

        #----------------------------------------------------------------------#
        # load
        #----------------------------------------------------------------------#

        if ( load_attr_data_type_IN is not None ):
            temp_etl_attr.set_load_attr_data_type( load_attr_data_type_IN )
        #-- END check if load attr data type --#

        temp_etl_attr.set_load_attr_name( load_prop_IN )

        attr_OUT = temp_etl_attr

        return attr_OUT

    #-- END classmethod create_transform_attribute() --#


    @classmethod
    def create_transform_attribute_date(
        cls,
        extract_prop_IN = None,
        load_prop_IN = None,
        transform_to_attr_name_IN = None,
        extract_data_type_IN = DATA_TYPE_STRING,
        extract_logical_type_IN = LOGICAL_TYPE_STRING_DATETIME_ISO_8601,
        is_required_IN = None,
        load_attr_data_type_IN = DATA_TYPE_DATETIME_DATE,
        conversion_string_IN = FORMAT_DATETIME_ISO_8601
    ):

        # return reference
        attr_OUT = None

        attr_OUT = cls.create_transform_attribute(
            extract_prop_IN = extract_prop_IN,
            load_prop_IN = load_prop_IN,
            transform_to_attr_name_IN = transform_to_attr_name_IN,
            extract_data_type_IN = extract_data_type_IN,
            extract_logical_type_IN = extract_logical_type_IN,
            is_required_IN = is_required_IN,
            load_attr_data_type_IN = load_attr_data_type_IN,
            conversion_string_IN = conversion_string_IN
        )

        return attr_OUT

    #-- END classmethod createtransform_attribute_date() --#


    @classmethod
    def create_transform_attribute_datetime(
        cls,
        extract_prop_IN = None,
        load_prop_IN = None,
        transform_to_attr_name_IN = None,
        extract_data_type_IN = DATA_TYPE_STRING,
        extract_logical_type_IN = LOGICAL_TYPE_STRING_DATETIME_ISO_8601,
        is_required_IN = None,
        load_attr_data_type_IN = DATA_TYPE_DATETIME_DATETIME,
        conversion_string_IN = FORMAT_DATETIME_ISO_8601
    ):

        # return reference
        attr_OUT = None

        attr_OUT = cls.create_transform_attribute(
            extract_prop_IN = extract_prop_IN,
            load_prop_IN = load_prop_IN,
            transform_to_attr_name_IN = transform_to_attr_name_IN,
            extract_data_type_IN = extract_data_type_IN,
            extract_logical_type_IN = extract_logical_type_IN,
            is_required_IN = is_required_IN,
            load_attr_data_type_IN = load_attr_data_type_IN,
            conversion_string_IN = conversion_string_IN
        )

        return attr_OUT

    #-- END classmethod createtransform_attribute_datetime() --#


    @classmethod
    def store_attribute_in_ldm_instance( cls, instance_IN, attr_name_IN, attr_value_IN ):

        '''
        Assumes we are working with a django model object that extends
            LoadableDjangoModel (ldm).
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "store_attribute_in_ldm_instance"
        status_message = None
        my_debug_flag = None
        do_detailed_status = False
        attr_exists = None
        current_value = None
        extra_data_json = None
        has_extra_data_changed = None

        # init
        my_debug_flag = cls.debug_flag
        #my_debug_flag = True
        do_detailed_status = cls.include_detailed_status
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have an instance?
        if ( ( instance_IN is not None ) and ( instance_IN != "" ) ):

            # do we have an attribute name?
            if ( ( attr_name_IN is not None ) and ( attr_name_IN != "" ) ):

                # is this name in the instance?
                attr_exists = hasattr( instance_IN, attr_name_IN )

                if ( my_debug_flag == True ):
                    status_message = "- attr_name = {attr_name} ( exists?: {attr_exists} ); attr_value = {attr_value}".format(
                        attr_name = attr_name_IN,
                        attr_exists = attr_exists,
                        attr_value = attr_value_IN
                    )
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # if name in instance, store value. If not, add to extra data.
                if ( attr_exists == True ):

                    # update status
                    status_OUT.set_detail_value( cls.PROP_WAS_UNKNOWN_ATTR, False )

                    # get existing value
                    current_value = getattr( instance_IN, attr_name_IN )

                    # attribute update detail
                    status_message = "{attr_name}: {old_value} ==> {new_value}.".format(
                        attr_name = attr_name_IN,
                        old_value = current_value,
                        new_value = attr_value_IN
                    )
                    status_OUT.set_detail_value( cls.PROP_ATTR_UPDATE_DETAIL, status_message )

                    # changed?
                    if ( current_value != attr_value_IN ):

                        # changed - make a note in status.
                        setattr( instance_IN, attr_name_IN, attr_value_IN )
                        status_OUT.set_detail_value( cls.PROP_WAS_ATTR_UPDATED, True )

                        # status message
                        status_message = "model attribute {attr_name} updated from {old_value} to {new_value}.".format(
                            attr_name = attr_name_IN,
                            old_value = current_value,
                            new_value = attr_value_IN
                        )
                        status_OUT.add_message( status_message )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, do_print_IN = my_debug_flag )

                    else:

                        # not changed - no need to do anything.
                        status_OUT.set_detail_value( cls.PROP_WAS_ATTR_UPDATED, False )
                        status_message = "model attribute {attr_name} NOT changed (current: {old_value}; new: {new_value}), so NOT updated.".format(
                            attr_name = attr_name_IN,
                            old_value = current_value,
                            new_value = attr_value_IN
                        )
                        status_OUT.add_message( status_message )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, do_print_IN = my_debug_flag )

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
                    status_OUT.set_detail_value( cls.PROP_ATTR_UPDATE_DETAIL, status_message )

                    # update status
                    status_OUT.set_detail_value( cls.PROP_WAS_UNKNOWN_ATTR, True )
                    status_message = "attribute {attr_name} NOT in model, adding to extra data (current: {old_value}; new: {new_value}).".format(
                        attr_name = attr_name_IN,
                        old_value = current_value,
                        new_value = attr_value_IN
                    )
                    status_OUT.add_message( status_message )
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, do_print_IN = my_debug_flag )

                    # update the value for this attribute in the extra_data
                    #     JSONField.
                    has_extra_data_changed = instance_IN.update_extra_data_attr( attr_name_IN, attr_value_IN )

                    # check if unknown attribute already present, if so,
                    #    only set updated flag if value was different.

                    # did it change?
                    if ( has_extra_data_changed == True ):

                        # it has!
                        status_OUT.set_detail_value( cls.PROP_WAS_ATTR_UPDATED, True )

                    else:

                        # no change!
                        status_OUT.set_detail_value( cls.PROP_WAS_ATTR_UPDATED, False )

                    #-- END check to see if extra data changed. --#

                #-- END check if has attr --#

                # detailed status?
                if ( do_detailed_status == True ):

                    # store details
                    status_OUT.set_detail_value( cls.PROP_ATTR_NAME, attr_name_IN )
                    status_OUT.set_detail_value( cls.PROP_ATTR_OLD_VALUE, current_value )
                    status_OUT.set_detail_value( cls.PROP_ATTR_NEW_VALUE, attr_value_IN )

                #-- END detailed status --#

            else:

                # no name. error.
                status_message = "ERROR in {}(): no attribute name passed in, nothing to be done.".format( me )
                LoggingHelper.log_message( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, log_level_code_IN = logging.ERROR, do_print_IN = True )

                # raise ETLError.
                raise ETLError( status_message )

            #-- END check to see if attribute name passed in --#

        else:

            # no instance. error.
            status_message = "ERROR in {}(): no load instance passed in, nothing to be done.".format( me )
            LoggingHelper.log_message( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, log_level_code_IN = logging.ERROR, do_print_IN = True )

            # raise ETLError.
            raise ETLError( status_message )

        #-- END check to see if instance --#

        return status_OUT

    #-- END method store_attribute_in_ldm_instance() --#


    #===========================================================================
    # ! ==> __init__() method - instance variables
    #===========================================================================


    def __init__( self ):

        '''
        Constructor
        '''

        # call parent's __init__()
        super().__init__()

        # extract storage traits
        self.extract_name = None
        self.extract_index = None
        self.extract_data_type = None
        self.extract_logical_type = None
        self.extract_is_required = False

        # transform information
        self.transform_conversion_string = None
        self.transform_method_name = None
        self.transform_to_attr_name = None

        # load storage traits
        self.load_attr_name = None
        self.load_attr_data_type = None

        # ==> related class

        # can either store instance of class...
        self.load_attr_related_model_class = None

        # ...or string name of module and class for dynamic loading.
        self.load_attr_related_model_class_module = None
        self.load_attr_related_model_class_name = None

        # and other related information.
        self.load_attr_related_model_data_type = None
        self.load_attr_related_model_fk_attr_name = None
        self.load_attr_related_model_method_name = None

        # processing method hooks.
        self.custom_processing_method_name = None

        # debug - class variable now
        #self.debug_flag = False

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def get_custom_processing_method_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.custom_processing_method_name

        return value_OUT

    #-- END method get_custom_processing_method_name --#


    def get_extract_index( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_index

        return value_OUT

    #-- END method get_extract_index --#


    def get_extract_is_required( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_is_required

        return value_OUT

    #-- END method get_extract_is_required --#


    def get_extract_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_name

        return value_OUT

    #-- END method get_extract_name --#


    def get_extract_data_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_data_type

        return value_OUT

    #-- END method get_extract_data_type --#


    def get_extract_logical_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_logical_type

        return value_OUT

    #-- END method get_extract_logical_type --#


    def get_load_attr_data_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_data_type

        return value_OUT

    #-- END method get_load_attr_data_type --#


    def get_load_attr_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_name

        return value_OUT

    #-- END method get_load_attr_name --#


    def get_load_attr_related_model_class( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_class

        return value_OUT

    #-- END method get_load_attr_related_model_class --#


    def get_load_attr_related_model_class_module( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_class_module

        return value_OUT

    #-- END method get_load_attr_related_model_class_module --#


    def get_load_attr_related_model_class_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_class_name

        return value_OUT

    #-- END method get_load_attr_related_model_class_name --#


    def get_load_attr_related_model_data_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_data_type

        return value_OUT

    #-- END method get_load_attr_related_model_data_type --#


    def get_load_attr_related_model_fk_attr_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_fk_attr_name

        return value_OUT

    #-- END method get_load_attr_related_model_fk_attr_name --#


    def get_load_attr_related_model_method_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_attr_related_model_method_name

        return value_OUT

    #-- END method get_load_attr_related_model_method_name --#


    def get_related_model_class( self ):

        '''
        First checks if actual related class stored in instance. If so, returns
            it. If not, tries to load class from module name and class name.
            Returns the result, if either name is missing, outputs error log and
            returns None. If problems with module or class loading, Exception
            will be thrown.
        '''

        # return reference
        class_OUT = None

        # declare variables
        me = "get_related_model_class"
        my_debug_flag = None
        status_message = None
        spec_json = None
        spec_json_string = None
        my_attr_name = None
        related_class = None
        related_class_module_name = None
        related_class_module = None
        related_class_name = None

        # init
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        spec_json = self.to_json()
        spec_json_string = json.dumps( spec_json, indent = 4, sort_keys = True )

        # retrieve spec info.
        my_attr_name = self.get_extract_name()
        related_class = self.get_load_attr_related_model_class()
        related_class_module_name = self.get_load_attr_related_model_class_module()
        related_class_name = self.get_load_attr_related_model_class_name()

        if ( my_debug_flag == True ):
            status_message = "In {my_method_name}() TOP: attribute {my_attr_name}; spec:\n{my_spec_json}.".format(
                my_method_name = me,
                my_attr_name = my_attr_name,
                my_spec_json = spec_json_string
            )
            LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        # are any of the three specified? If not, just return None.
        if ( ( related_class is not None )
            or ( ( related_class_module_name is not None ) and ( related_class_module_name != "" ) )
            or ( ( related_class_name is not None ) and ( related_class_name != "" ) ) ):

            # do we have actual class reference?
            if ( related_class is None ):

                # no class reference. Do we have module and name so we can load it
                #     dynamically?
                related_class_module_name = self.get_load_attr_related_model_class_module()
                related_class_name = self.get_load_attr_related_model_class_name()

                if ( my_debug_flag == True ):
                    status_message = "No related class."
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # must have both module and name.
                if ( ( related_class_module_name is not None ) and ( related_class_module_name != "" ) ):

                    if ( ( related_class_name is not None ) and ( related_class_name != "" ) ):

                        # try to load the module.
                        related_class_module = importlib.import_module( related_class_module_name )

                        # and, then, try to retrieve class from module.
                        related_class = getattr( related_class_module, related_class_name )

                        # if we get here without exception, return the class.
                        class_OUT = related_class

                        if ( my_debug_flag == True ):
                            status_message = "Loaded related class {my_class} ( module: {my_module}; class: {my_class_name})".format(
                                my_class = class_OUT,
                                my_module = related_class_module_name,
                                my_class_name = related_class_name
                            )
                            LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                    else:

                        # ERROR - no class name. Nothing to do.

                        status_message = "ERROR in {my_method_name}(): no related class name passed in for attr_name: {my_attr_name}; full attribute specification:\n{my_spec_json}. If no related class reference stored, must have both related class module name and related class name.  Nothing to be done.".format(
                            my_method_name = me,
                            my_attr_name = self.get_extract_name(),
                            my_spec_json = json_string
                        )
                        LoggingHelper.log_message( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, log_level_code_IN = logging.ERROR, do_print_IN = True )

                        # return None
                        class_OUT = None

                    #-- END check if class name. --#

                else:

                    # ERROR - no module name. Nothing to do.
                    spec_json = self.to_json()
                    json_string = json.dumps( spec_json, indent = 4, sort_keys = True )

                    status_message = "ERROR in {my_method_name}(): no related class module name passed in for attr_name: {my_attr_name}; full attribute specification:\n{my_spec_json}. If no related class reference stored, must have both related class module name and related class name. Nothing to be done.".format(
                        my_method_name = me,
                        my_attr_name = self.get_extract_name(),
                        my_spec_json = json_string
                    )
                    LoggingHelper.log_message( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, log_level_code_IN = logging.ERROR, do_print_IN = True )

                    # return None
                    class_OUT = None

                #-- END check to see if module name. --#

            else:

                # related class reference found - return it.
                class_OUT = related_class

                if ( my_debug_flag == True ):
                    status_message = "Found related class ( {my_class} ).".format( my_class = class_OUT )
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            #-- END check to see if class reference present --#

        else:

            # Nothing to see here - no related class info - return None.
            class_OUT = None

        #-- END check to see if anything class-related set at all --#

        return class_OUT

    #-- END method get_related_model_class() --#


    def get_transform_conversion_string( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.transform_conversion_string

        return value_OUT

    #-- END method get_transform_conversion_string --#


    def get_transform_method_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.transform_method_name

        return value_OUT

    #-- END method get_transform_method_name --#


    def get_transform_to_attr_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.transform_to_attr_name

        return value_OUT

    #-- END method get_transform_to_attr_name --#


    def process_ldm_object_value( self, value_IN, instance_IN, time_zone_IN = pytz.UTC ):

        '''
        takes types and transform traits of attribute spec into account to
            convert value for loading into instance.

        logic:
        - if transform method is defined, tries to call it on the instance,
            stores result in value_OUT, then proceeds with the standard
            processing.
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
        me = "process_ldm_object_value"
        status_message = None
        my_debug_flag = None
        work_value = None
        spec_json = None
        json_string = None

        # declare variables - info from spec
        transform_method_name = None
        method_exists = None
        transform_method = None
        transform_to_attr_name = None

        # init
        my_debug_flag = self.debug_flag
        #my_debug_flag = True

        # base behavior - return value passed in.
        value_OUT = value_IN

        # retrieve info from spec.
        attr_name = self.get_load_attr_name()

        # do we have a value?
        if ( value_IN is not None ):

            # first, do normal processing.
            value_OUT = self.process_value( value_IN, time_zone_IN )

            # do we have an instance?
            if ( instance_IN is not None ):

                # retrieve info from spec.
                attr_name = self.get_load_attr_name()
                in_data_type = self.get_extract_data_type()
                in_logical_type = self.get_extract_logical_type()
                out_data_type = self.get_load_attr_data_type()
                transform_pattern = self.get_transform_conversion_string()
                transform_method_name = self.get_transform_method_name()
                transform_to_attr_name = self.get_transform_to_attr_name()

                if ( my_debug_flag == True ):
                    spec_json = self.to_json()
                    json_string = json.dumps( spec_json, indent = 4, sort_keys = True )
                    status_message = "attr: {attr_name}; value: \"{value}\"; ETLAttribute JSON string:\n{json_string}".format(
                        attr_name = attr_name,
                        value = value_IN,
                        json_string = json_string
                    )
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # is there a transform method?
                if ( ( transform_method_name is not None ) and ( transform_method_name != "" ) ):

                    # is there a method by that name on this instance?
                    method_exists = hasattr( instance_IN, transform_method_name )
                    if ( method_exists == True ):

                        # get pointer to instance
                        transform_method = getattr( instance_IN, transform_method_name )

                        # call it on instance, passing it value_IN and self.
                        value_OUT = transform_method( instance_IN, value_IN, self )

                    else:

                        # no method by that name. Error - log, then raise error.
                        status_message = "ERROR in ETLAttribute.{method_name}(): no method with name {transform_method_name} found on instance {object_instance} of type {object_type}. Transform specification is broken.".format(
                            method_name = me,
                            transform_method_name = transform_method_name,
                            object_instance = instance_IN,
                            object_type = type( instance_IN )
                        )
                        LoggingHelper.log_message( status_message, method_IN = me, logger_name_IN = cls.MY_LOGGER_NAME, log_level_code_IN = logging.ERROR, do_print_IN = True )

                        # raise ETLError.
                        raise ETLError( status_message )

                    #-- END check to see if method exists. --#

                #-- END check to see if transform method name --#

                # are we transforming to a separate attribute?
                if ( ( transform_to_attr_name is not None ) and ( transform_to_attr_name != "" ) ):

                    if ( my_debug_flag == True ):
                        status_message = "storing translated value {} in attr {}".format( value_OUT, transform_to_attr_name )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                    # we are. store transformed value there...
                    self.store_attribute_in_ldm_instance( instance_IN, transform_to_attr_name, value_OUT )

                    # ...then return value passed in.
                    value_OUT = value_IN

                #-- END check to see if we store transformed value in separate attribute. --#

            else:

                # no instance_IN - nothing to do.
                status_message = "In {}(): no instance passed in for value, nothing to be done.".format( me )
                if ( my_debug_flag == True ):
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            #-- END check if instance --#

        else:

            # no value - nothing to do.
            status_message = "In {method_name}(): no value passed in for attr {attr_name}, nothing to be done.".format(
                method_name = me,
                attr_name = attr_name
            )
            if ( my_debug_flag == True ):
                LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

        #-- check if value. --#

        return value_OUT

    #-- END method process_ldm_object_value() --#


    def process_value( self, value_IN, time_zone_IN = pytz.UTC ):

        '''
        takes types and transform traits of attribute spec into account to
            convert value for loading into instance.

        logic:
        - if extract and load types are set, convert from one to other.
        - if types could use a transform string, see if one is present. If so,
            use it. If not, try to transform using default.
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
        transformed_value = None
        time_zone = None

        # declare variables - info from spec
        attr_name = None
        in_data_type = None
        in_logical_type = None
        transform_pattern = None
        transform_method_name = None
        method_exists = None
        transform_method = None
        transform_to_attr_name = None
        out_data_type = None

        # init
        my_debug_flag = self.debug_flag
        #my_debug_flag = True

        # base behavior - return value passed in.
        value_OUT = value_IN

        # retrieve info from spec.
        attr_name = self.get_load_attr_name()

        # do we have a value?
        if ( value_IN is not None ):

            # retrieve info from spec.
            in_data_type = self.get_extract_data_type()
            in_logical_type = self.get_extract_logical_type()
            out_data_type = self.get_load_attr_data_type()
            transform_pattern = self.get_transform_conversion_string()

            if ( my_debug_flag == True ):
                spec_json = self.to_json()
                json_string = json.dumps( spec_json, indent = 4, sort_keys = True )
                status_message = "attr: {attr_name}; value: \"{value}\"; ETLAttribute JSON string:\n{json_string}".format(
                    attr_name = attr_name,
                    value = value_IN,
                    json_string = json_string
                )
                LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

            # is there an output data type we transform to...
            if ( ( out_data_type is not None ) and ( out_data_type != "" ) ):

                # there is an output data type. Process based on output
                #     type.
                # simple type - int
                if ( out_data_type == self.DATA_TYPE_INT ):

                    # convert to int
                    value_OUT = self.clean_value(
                        value_IN,
                        desired_type_IN = self.DATA_TYPE_INT
                    )

                    if ( my_debug_flag == True ):
                        status_message = "translated {} to int {}".format( value_IN, value_OUT )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                # simple type - string
                elif ( out_data_type == self.DATA_TYPE_STRING ):

                    # convert to string
                    value_OUT = self.clean_value(
                        value_IN,
                        desired_type_IN = self.DATA_TYPE_STRING
                    )

                    if ( my_debug_flag == True ):
                        status_message = "translated {} to string {}".format( value_IN, value_OUT )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                # complex type - datetime.datetime
                elif ( ( out_data_type == self.DATA_TYPE_DATETIME_DATETIME )
                    or ( out_data_type == self.DATA_TYPE_DATETIME_DATE ) ):

                    # make sure string is clean first.
                    work_value = self.clean_value(
                        value_IN,
                        desired_type_IN = self.DATA_TYPE_STRING
                    )

                    if ( my_debug_flag == True ):
                        status_message = "datetime attr: {attr_name}; cleaned value: \"{value}\"".format(
                            attr_name = attr_name,
                            value = work_value
                        )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

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
                                LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )

                                # ...return value passed in.
                                value_OUT = value_IN

                            #-- END try...except around date parsing --#

                        #-- check if transform pattern. --#

                        # date or datetime?
                        if ( out_data_type == self.DATA_TYPE_DATETIME_DATE ):

                            # ==> datetime.date
                            # don't worry about time zone, just grab the date
                            #     part of the parsed datetime.
                            value_OUT = value_OUT.date()

                        elif ( out_data_type == self.DATA_TYPE_DATETIME_DATETIME ):

                            # ==> datetime.datetime
                            # date time - deal with time zone.
                            time_zone = value_OUT.tzinfo

                            if ( my_debug_flag == True ):
                                status_message = "translated datetime \"{translated_value}\" has tzinfo: {my_tzinfo}".format(
                                    translated_value = value_OUT,
                                    my_tzinfo = time_zone
                                )
                                LoggingHelper.output_debug( status_message, method_IN = me, indent_with_IN = "--------> ", logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                            #-- END DEBUG --#

                            if ( time_zone is None ):

                                # got a default time zone?
                                if ( time_zone_IN is not None ):

                                    value_OUT = time_zone_IN.localize( value_OUT )

                                #-- END check to see if we have a time zone --#

                            #-- END check to see if time zone set. --#

                        else:

                            # inconceivable! It had to be one of the above two
                            #     to get into this branch - how did it change?
                            status_message = "WARNING - type {output_type} changed mid-execution - should be either {date_type} or {datetime_type}.".format(
                                output_type = out_data_type,
                                date_type = self.DATA_TYPE_DATETIME_DATE,
                                datetime_type = self.DATA_TYPE_DATETIME_DATETIME
                            )
                            LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )

                        #-- END check to see if date or datetime --#

                    else:

                        # no value passed in, just return None (standardize
                        #     empty dates from either None or "" to None).
                        value_OUT = None

                    #-- END check to see if value is parse-able. --#

                    if ( my_debug_flag == True ):
                        status_message = "translated \"{my_input_value}\" to {my_output_type} \"{my_output_value}\"".format(
                            my_input_value = value_IN,
                            my_output_type = out_data_type,
                            my_output_value = value_OUT
                        )
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                # unknown type.
                else:

                    # unknown output type - nothing to do.
                    status_message = "In {method_name}(): unknown output type \"{output_type}\" for attr {attr_name} (value: \"{attr_value}\"), nothing to be done.".format(
                        method_name = me,
                        output_type = out_data_type,
                        attr_name = attr_name,
                        attr_value = value_IN
                    )
                    if ( my_debug_flag == True ):
                        LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                #-- END check to see what type we want --#

            else:

                # no output type - nothing to do.
                status_message = "In {method_name}(): no output type for attr {attr_name} (value: \"{attr_value}\"), nothing to be done.".format(
                    method_name = me,
                    attr_name = attr_name,
                    attr_value = value_IN
                )
                if ( my_debug_flag == True ):
                    LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

            #-- END check to see if output type set. --#

        else:

            # no value - nothing to do.
            status_message = "In {method_name}(): no value passed in for attr {attr_name}, nothing to be done.".format(
                method_name = me,
                attr_name = attr_name
            )
            if ( my_debug_flag == True ):
                LoggingHelper.output_debug( status_message, method_IN = me, logger_name_IN = self.MY_LOGGER_NAME, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

        #-- check if value. --#

        return value_OUT

    #-- END method process_value() --#


    def set_custom_processing_method_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.custom_processing_method_name = value_IN

        # return it.
        value_OUT = self.get_custom_processing_method_name()

        return value_OUT

    #-- END method set_custom_processing_method_name() --#


    def set_extract_index( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_index = value_IN

        # return it.
        value_OUT = self.get_extract_index()

        return value_OUT

    #-- END method set_extract_index() --#


    def set_extract_is_required( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_is_required = value_IN

        # return it.
        value_OUT = self.get_extract_is_required()

        return value_OUT

    #-- END method set_extract_is_required() --#


    def set_extract_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_name = value_IN

        # return it.
        value_OUT = self.get_extract_name()

        return value_OUT

    #-- END method set_extract_name() --#


    def set_extract_data_type( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_data_type = value_IN

        # return it.
        value_OUT = self.get_extract_data_type()

        return value_OUT

    #-- END method set_extract_data_type() --#


    def set_extract_logical_type( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_logical_type = value_IN

        # return it.
        value_OUT = self.get_extract_logical_type()

        return value_OUT

    #-- END method set_extract_logical_type() --#


    def set_load_attr_data_type( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_data_type = value_IN

        # return it.
        value_OUT = self.get_load_attr_data_type()

        return value_OUT

    #-- END method set_load_attr_data_type() --#


    def set_load_attr_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_name = value_IN

        # return it.
        value_OUT = self.get_load_attr_name()

        return value_OUT

    #-- END method set_load_attr_name() --#


    def set_load_attr_related_model_class( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_related_model_class = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_class()

        return value_OUT

    #-- END method set_load_attr_related_model_class() --#


    def set_load_attr_related_model_class_module( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_related_model_class_module = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_class_module()

        return value_OUT

    #-- END method set_load_attr_related_model_class_module() --#


    def set_load_attr_related_model_class_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_related_model_class_name = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_class_name()

        return value_OUT

    #-- END method set_load_attr_related_model_class_name() --#


    def set_load_attr_related_model_data_type( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # check validity? value_IN in self.RELATED_TYPE_VALUE_TO_TYPE_MAP?

        # store value.
        self.load_attr_related_model_data_type = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_data_type()

        return value_OUT

    #-- END method set_load_attr_related_model_data_type() --#


    def set_load_attr_related_model_fk_attr_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_related_model_fk_attr_name = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_fk_attr_name()

        return value_OUT

    #-- END method set_load_attr_related_model_fk_attr_name() --#


    def set_load_attr_related_model_method_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_attr_related_model_method_name = value_IN

        # return it.
        value_OUT = self.get_load_attr_related_model_method_name()

        return value_OUT

    #-- END method set_load_attr_related_model_method_name() --#


    def set_transform_conversion_string( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.transform_conversion_string = value_IN

        # return it.
        value_OUT = self.get_transform_conversion_string()

        return value_OUT

    #-- END method set_transform_conversion_string() --#


    def set_transform_method_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.transform_method_name = value_IN

        # return it.
        value_OUT = self.get_transform_method_name()

        return value_OUT

    #-- END method set_transform_method_name() --#


    def set_transform_to_attr_name( self, value_IN ):

        '''
        Accepts value, stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.transform_to_attr_name = value_IN

        # return it.
        value_OUT = self.get_transform_to_attr_name()

        return value_OUT

    #-- END method set_transform_to_attr_name() --#


    def to_json( self ):

        # return reference
        json_OUT = None

        # declare variables
        current_value = None
        json_root = None

        # init
        json_root = {}

        # add all fields to dictionary, then return.
        json_root[ "extract_name" ] = self.get_extract_name()
        json_root[ "extract_index" ] = self.get_extract_index()
        json_root[ "extract_data_type" ] = self.get_extract_data_type()
        json_root[ "extract_logical_type" ] = self.get_extract_logical_type()
        json_root[ "extract_is_required" ] = self.get_extract_is_required()

        # transform information
        json_root[ "transform_conversion_string" ] = self.get_transform_conversion_string()
        json_root[ "transform_to_attr_name" ] = self.get_transform_to_attr_name()
        json_root[ "transform_method_name" ] = self.get_transform_method_name()

        # load storage traits
        json_root[ "load_attr_name" ] = self.get_load_attr_name()
        json_root[ "load_attr_data_type" ] = self.get_load_attr_data_type()

        # related models
        json_root[ "load_attr_related_model_class_module" ] = self.get_load_attr_related_model_class_module()
        json_root[ "load_attr_related_model_class_name" ] = self.get_load_attr_related_model_class_name()
        json_root[ "load_attr_related_model_data_type" ] = self.get_load_attr_related_model_data_type()
        json_root[ "load_attr_related_model_fk_attr_name" ] = self.get_load_attr_related_model_fk_attr_name()
        json_root[ "load_attr_related_model_method_name" ] = self.get_load_attr_related_model_method_name()

        # related model class is special, since it is not a string or int.

        # get value.
        current_value = self.get_load_attr_related_model_class()

        # if not None, convert to String
        if ( current_value is not None ):
            current_value = str( current_value )
        #-- END check if not None --#

        # store in JSON
        json_root[ "load_attr_related_model_class" ] = current_value

        # custom processing
        json_root[ "custom_processing_method_name" ] = self.get_custom_processing_method_name()

        json_OUT = json_root

        return json_OUT

    #-- END method to_json() --#


#-- END class ETLAttribute --#
