#===============================================================================
# imports
#===============================================================================

# base python libraries
import datetime
import logging
import sys
import time
import traceback


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

    # DEBUG - changed to instance variable.
    #DEBUG_FLAG = False

    # logger name
    MY_LOGGER_NAME = "etl_attribute"

    # data types
    DATA_TYPE_STRING = "string"
    DATA_TYPE_INT = "int"
    DATA_TYPE_DATETIME_DATETIME = "datetime.datetime"

    # logical types
    LOGICAL_TYPE_STRING_DATE = "string_date"
    LOGICAL_TYPE_STRING_DATETIME = "string_datetime"
    LOGICAL_TYPE_STRING_DATETIME_ISO_8601 = "string_datetime_ISO_8601"

    # related data types
    RELATED_TYPE_DICT = "dict"
    RELATED_TYPE_LIST = "list"
    RELATED_TYPE_VALUE_TO_TYPE_MAP = dict()
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_DICT ] = dict
    RELATED_TYPE_VALUE_TO_TYPE_MAP[ RELATED_TYPE_LIST ] = list

    # Reusable format strings
    FORMAT_DATETIME_ISO_8601 = "ISO-8601"


    #===========================================================================
    # ! ==> class variables
    #===========================================================================


    # debug_flag
    debug_flag = False

    # logging
    logging_level = logging.ERROR


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

        # extract storage traits
        self.extract_name = None
        self.extract_index = None
        self.extract_data_type = None
        self.extract_logical_type = None
        self.extract_is_required = False

        # transform information
        self.transform_conversion_string = None
        self.transform_to_attr_name = None

        # load storage traits
        self.load_attr_name = None
        self.load_attr_data_type = None
        self.load_attr_related_model_class = None
        self.load_attr_related_model_data_type = None
        self.load_attr_related_model_fk_attr_name = None
        self.load_attr_related_model_method_name = None

        # debug
        self.debug_flag = False

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


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


    def get_transform_conversion_string( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.transform_conversion_string

        return value_OUT

    #-- END method get_transform_conversion_string --#


    def get_transform_to_attr_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.transform_to_attr_name

        return value_OUT

    #-- END method get_transform_to_attr_name --#


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

        # load storage traits
        json_root[ "load_attr_name" ] = self.get_load_attr_name()
        json_root[ "load_attr_data_type" ] = self.get_load_attr_data_type()
        json_root[ "load_attr_related_model_class" ] = self.get_load_attr_related_model_class()
        json_root[ "load_attr_related_model_data_type" ] = self.get_load_attr_related_model_data_type()

        json_OUT = json_root

        return json_OUT

    #-- END method to_json() --#


#-- END class ETLAttribute --#
