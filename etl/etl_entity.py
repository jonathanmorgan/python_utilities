#===============================================================================
# imports
#===============================================================================

# base python libraries
import datetime
import logging
import sys
import time
import traceback

# etl imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_error import ETLError


#===============================================================================
# class ETLEntity
#===============================================================================

# lineage: object
class ETLEntity( object ):


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "

    # DEBUG - changed to instance variable.
    #DEBUG_FLAG = False

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLEntity"

    # type of "extract" entity.
    STORAGE_TYPE_DICT = "dict"
    STORAGE_TYPE_JSON_STRING = "json_string"
    STORAGE_TYPE_JSON = "json"  # effectively dictionary
    STORAGE_TYPE_LIST_WITH_HEADERS = "list_with_headers"
    STORAGE_TYPE_LIST_NO_HEADERS = "list_no_headers"
    STORAGE_TYPE_XLSX_WITH_HEADERS = "xlsx_with_headers"
    STORAGE_TYPE_XLSX_NO_HEADERS = "xlsx_no_headers"

    # valid storage types
    VALID_STORAGE_TYPE_LIST = []
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_DICT )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_JSON_STRING )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_JSON )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_LIST_WITH_HEADERS )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_LIST_NO_HEADERS )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_XLSX_WITH_HEADERS )
    VALID_STORAGE_TYPE_LIST.append( STORAGE_TYPE_XLSX_NO_HEADERS )

    # type of "load" entity.
    STORAGE_TYPE_PYTHON_CLASS = "python_class"

    # identification type
    ID_TYPE_AND_EXACT = "and_exact"


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

        # NOTE: if you add a field, remember to add it to "to_json()" method!

        # external information
        self.extract_storage_type = None
        self.extract_first_index = 1
        self.load_storage_type = None
        self.load_class = None

        # external storage traits
        self.attr_key_to_attribute_map = {}
        self.attr_load_name_to_key_map = {}
        self.attr_index_to_key_map = {}
        self.attr_key_to_index_map = {}

        # required in extract...
        self.required_attr_key_set = set()

        # ID - record identification
        self.id_attr_key_list = []
        self.id_match_type = self.ID_TYPE_AND_EXACT

        # data attributes
        self.data_attr_key_list = []

        # related entity attributes
        self.related_entity_attr_key_list = []

        # debug
        self.debug_flag = False

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def add_data_attr( self, attr_IN ):

        # return reference
        attr_key_OUT = None

        # declare variables
        me = "add_data_attr"
        status_message = None

        # declare variables - attribute traits
        attr_key = None
        attr_extract_name = None
        attr_extract_index = None
        attr_load_name = None
        attr_is_required = None

        # declare variables - processing
        key_to_attribute_map = None
        load_name_to_key_map = None
        index_to_key_map = None
        key_to_index_map = None
        my_data_key_list = None
        required_set = None

        # got an attribute?
        if ( attr_IN is not None ):

            # retrieve information from attribute instance.
            attr_extract_name = attr_IN.get_extract_name()
            attr_load_name = attr_IN.get_load_attr_name()
            attr_extract_index = attr_IN.get_extract_index()
            attr_is_required = attr_IN.get_extract_is_required()

            # do we have extract name (the only required value)?
            if ( ( attr_extract_name is not None ) and ( attr_extract_name != "" ) ):

                # we have extract name - use as key.
                attr_key = attr_extract_name

                # do we have a load name?
                if ( ( attr_load_name is None ) or ( attr_load_name == "" ) ):

                    # no. Use extract name as load name.
                    attr_load_name = attr_IN.set_load_attr_name( attr_extract_name )

                #-- END check to see if load name --#

                # first, add to attribute store.
                key_to_attribute_map = self.get_attr_key_to_attribute_map()
                key_to_attribute_map[ attr_key ] = attr_IN

                # add mapping of load name to extract name.
                load_name_to_key_map = self.get_attr_load_name_to_key_map()
                load_name_to_key_map[ attr_load_name ] = attr_key

                # add to list of keys associated with data fields.
                my_data_key_list = self.get_data_attr_key_list()
                if ( attr_key not in my_data_key_list ):

                    my_data_key_list.append( attr_key )

                #-- END check if attr_key is in list of data field keys --#

                # if index, add to index-to-key map.
                if ( ( attr_extract_index is not None ) and ( attr_extract_index != "" ) ):

                    # add to index-to-key map.
                    index_to_key_map = self.get_attr_index_to_key_map()
                    index_to_key_map[ attr_extract_index ] = attr_key

                    # add to key-to-index map.
                    key_to_index_map = self.get_attr_key_to_index_map()
                    key_to_index_map[ attr_key ] = attr_extract_index

                    # TODO: break this out into separate method to check for
                    #     collisions, corruption, etc.

                #-- END check to see if index present. --#

                # required?
                if ( ( attr_is_required is not None )
                    and ( attr_is_required != "" )
                    and ( attr_is_required == True ) ):

                    # required!
                    self.add_required_attr_key( attr_key )

                #-- END check to see if required. --#

                # return attr_key
                attr_key_OUT = attr_key

            else:

                # ERROR
                status_message = "In {}(): ERROR - no attribute extract name present in instance: {}.".format( me, attr_IN )
                attr_key_OUT = None
                print( status_message )

            #-- END check to see if extract name set. --#

        else:

            # ERROR
            status_message = "In {}(): ERROR - no attribute passed in.".format( me )
            attr_key_OUT = None
            print( status_message )

        #-- END check to see if attribute passed in --#

        return attr_key_OUT

    #-- END method add_data_attr() --#


    def add_id_attr_key( self, attr_key_IN ):

        # return reference
        attr_key_OUT = None

        # declare variables
        me = "add_id_attr_key"
        status_message = None
        id_attr_key_list = None

        # do we have an attribute key?
        if ( ( attr_key_IN is not None ) and ( attr_key_IN != "" ) ):

            # yes. Add it to the list.
            id_attr_key_list = self.get_id_attr_key_list()

            # already there?
            if ( attr_key_IN not in id_attr_key_list ):

                # not there. Add it.
                id_attr_key_list.append( attr_key_IN )

                # TODO: add ability to specify index, to order?

            else:

                # already there. Output a message.
                status_message = "In {}(): WARNING - attribute key {} already in attribute key list: {}".format( me, attr_key_IN, id_attr_key_list )
                print( status_message )

            #-- END check to see if attribute already in list. --#

            # return key
            attr_key_OUT = attr_key_IN

        else:

            # ERROR
            status_message = "In {}(): ERROR - no attribute passed in.".format( me )
            print( status_message )

        #-- END check to see if attribute key passed in. --#

        return attr_key_OUT

    #-- END method add_id_attr_key() --#


    def add_identity_attr( self, attr_IN ):

        # return reference
        attr_key_OUT = None

        # declare variables
        me = "add_identity_attr"
        status_message = None
        attr_key = None

        # anything passed in?
        if ( attr_IN is not None ):

            # first, add as data attribute.
            attr_key = self.add_data_attr( attr_IN )

            # did we get an attribute key back? None or "" = error.
            if ( ( attr_key is not None ) and ( attr_key != "" ) ):

                # data add worked - now to add as an ID.
                self.add_id_attr_key( attr_key )

                # set attr key to return.
                attr_key_OUT = attr_key

            else:

                # ERROR
                status_message = "In {}(): ERROR - no attribute key returned by add_data_attr() for attribute: {}.".format( me, attr_IN )
                print( status_message )

            #-- END check if data add worked. --#

        else:

            # ERROR
            status_message = "In {}(): ERROR - no attribute passed in.".format( me )
            print( status_message )

        #-- END check to see if attribute passed in --#

        return attr_key_OUT

    #-- END method add_identity_attr() --#


    def add_required_attr_key( self, attr_key_IN ):

        # return reference
        attr_key_OUT = None

        # declare variables
        me = "add_required_attr_key"
        status_message = None
        my_required_attr_key_set = None

        # do we have an attribute key?
        if ( ( attr_key_IN is not None ) and ( attr_key_IN != "" ) ):

            # yes. Add it to the list.
            my_required_attr_key_set = self.get_required_attr_key_set()

            # already there?
            if ( attr_key_IN not in my_required_attr_key_set ):

                # not there. Add it.
                my_required_attr_key_set.add( attr_key_IN )

            else:

                # already there. Output a message.
                status_message = "In {}(): WARNING - attribute key {} already in required attribute key set: {}".format( me, attr_key_IN, my_required_attr_key_set )
                print( status_message )

            #-- END check to see if attribute already in list. --#

            # return key
            attr_key_OUT = attr_key_IN

        else:

            # ERROR
            status_message = "In {}(): ERROR - no attribute passed in.".format( me )
            print( status_message )

        #-- END check to see if attribute key passed in. --#

        return attr_key_OUT

    #-- END method add_required_attr_key() --#


    def get_extract_first_index( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_first_index

        return value_OUT

    #-- END method get_extract_first_index --#


    def get_attr_index_to_key_map( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.attr_index_to_key_map

        return value_OUT

    #-- END method get_attr_index_to_key_map --#


    def get_attr_key_to_attribute_map( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.attr_key_to_attribute_map

        return value_OUT

    #-- END method get_attr_key_to_attribute_map --#


    def get_attr_key_to_index_map( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.attr_key_to_index_map

        return value_OUT

    #-- END method get_attr_key_to_index_map --#


    def get_attr_load_name_to_key_map( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.attr_load_name_to_key_map

        return value_OUT

    #-- END method get_attr_load_name_to_key_map --#


    def get_data_attr_key_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.data_attr_key_list

        return value_OUT

    #-- END method get_data_attr_key_list --#


    def get_extract_storage_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.extract_storage_type

        return value_OUT

    #-- END method get_extract_storage_type --#


    def get_id_attr_key_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.id_attr_key_list

        return value_OUT

    #-- END method get_id_attr_key_list --#


    def get_id_match_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.id_match_type

        return value_OUT

    #-- END method get_id_match_type --#


    def get_load_class( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_class

        return value_OUT

    #-- END method get_load_class --#


    def get_load_storage_type( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.load_storage_type

        return value_OUT

    #-- END method get_load_storage_type --#


    def get_related_entity_attr_key_list( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.related_entity_attr_key_list

        return value_OUT

    #-- END method get_related_entity_attr_key_list --#


    def get_required_attr_key_set( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.required_attr_key_set

        return value_OUT

    #-- END method get_required_attr_key_set --#


    def pull_attr_for_key( self, key_IN ):

        '''
        Accepts attribute key. Retrieves ETLAttribute instance associated with
            that key. On error, returns None.
        '''

        # return reference
        attr_OUT = None

        # declare variables
        me = "pull_attr_for_key"
        status_message = None
        my_debug_flag = None
        key_to_attr_map = None

        # init
        my_debug_flag = self.debug_flag

        # got a key?
        if ( ( key_IN is not None ) and ( key_IN != "" ) ):

            # retrieve key-to-attr map.
            key_to_attr_map = self.get_attr_key_to_attribute_map()

            # check if key is in map
            if ( key_IN in key_to_attr_map ):

                # retrieve value for that key.
                attr_OUT = key_to_attr_map.get( key_IN )

            else:

                # key not found output message, return None.
                status_message = "In {}(): no ETLAttribute found for key {}, returning None.".format( me, key_IN )
                if ( my_debug_flag == True ):
                    print( status_message )
                #-- END DEBUG --#
                attr_OUT = None

            #-- END check to see if key is in map. --#

        else:

            status_message = "In {}(): ERROR - no key passed in, can't pull anything for an empty key.".format( me )
            print( status_message )
            attr_OUT = None

        #-- END check to see if key passed in. --#

        return attr_OUT

    #-- END method pull_attr_for_key() --#


    def pull_index_for_key( self, key_IN ):

        '''
        Accepts attribute key. Retrieves index associated with that key. On
            error, returns None.
        '''

        # return reference
        index_OUT = None

        # declare variables
        me = "pull_index_for_key"
        status_message = None
        index_to_key_map = None

        # got an key?
        if ( ( key_IN is not None ) and ( key_IN != "" ) ):

            # retrieve key-to-index map.
            key_to_index_map = self.get_attr_key_to_index_map()

            # check if key is in map
            if ( key_IN in key_to_index_map ):

                # retrieve value for that key.
                index_OUT = key_to_index_map.get( key_IN, None )

            else:

                # index not found - output message, return None.
                status_message = "In {}(): no index found for key {}, returning None.".format( me, key_IN )
                print( status_message )
                index_OUT = None

            #-- END check to see if index is in map. --#

        else:

            status_message = "In {}(): ERROR - no key passed in, can't pull anything for an empty key.".format( me )
            print( status_message )
            index_OUT = None

        #-- END check to see if index passed in. --#

        return index_OUT

    #-- END method pull_index_for_key() --#


    def pull_key_for_index( self, index_IN ):

        '''
        Accepts attribute index. Retrieves key associated with that index. On
            error, returns None.
        '''

        # return reference
        key_OUT = None

        # declare variables
        me = "pull_key_for_index"
        status_message = None
        index_to_key_map = None

        # got an index?
        if ( ( index_IN is not None ) and ( index_IN != "" ) ):

            # retrieve index-to-key map.
            index_to_key_map = self.get_attr_index_to_key_map()

            # check if index is in map
            if ( index_IN in index_to_key_map ):

                # retrieve value for that index.
                key_OUT = index_to_key_map.get( index_IN, None )

            else:

                # index not found - output message, return None.
                status_message = "In {}(): no key found for index {}, returning None.".format( me, index_IN )
                print( status_message )
                key_OUT = None

            #-- END check to see if index is in map. --#

        else:

            status_message = "In {}(): ERROR - no index passed in, can't pull anything for an empty index.".format( me )
            print( status_message )
            key_OUT = None

        #-- END check to see if index passed in. --#

        return key_OUT

    #-- END method pull_key_for_index() --#


    def pull_load_attr_name_for_index( self, index_IN ):

        '''
        Accepts attribute key. Retrieves "load_attr_name" for that key from the
            ETLAttribute instance associated with that key.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "pull_load_attr_name_for_index"
        status_message = None
        index_key = None

        # got an index?
        if ( ( index_IN is not None ) and ( index_IN != "" ) ):

            # retrieve key for index
            index_key = self.pull_key_for_index( index_IN )

            # got a key?
            if ( ( index_key is not None ) and ( index_key != "" ) ):

                # pull name for key.
                value_OUT = self.pull_load_attr_name_for_key( index_key )

            else:

                # no key associated with that index.
                status_message = "In {}(): ERROR - no key associated with index passed in ( {} ), can't pull anything without a key.".format( me, index_IN )
                print( status_message )
                attr_OUT = None

            #-- END check to see if key associated with index. --#

        else:

            status_message = "In {}(): ERROR - no index passed in, can't pull anything for an empty key.".format( me )
            print( status_message )
            attr_OUT = None

        #-- END check to see if key passed in. --#

        return value_OUT

    #-- END method pull_load_attr_name_for_index() --#


    def pull_load_attr_name_for_key( self, key_IN ):

        '''
        Accepts attribute key. Retrieves "load_attr_name" for that key from the
            ETLAttribute instance associated with that key.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "pull_load_attr_name_for_key"
        status_message = None
        attr_instance = None

        # got a key?
        if ( ( key_IN is not None ) and ( key_IN != "" ) ):

            # retrieve ETLAttribute instance for key.
            attr_instance = self.pull_attr_for_key( key_IN )

            # do we have an ETLAttribute?
            if ( attr_instance is not None ):

                # get requested value.
                value_OUT = attr_instance.get_load_attr_name()

            else:

                # no ETLAttribute - return the key.
                value_OUT = key_IN

            #-- END check for ETLAttribute --#

        else:

            status_message = "In {}(): ERROR - no key passed in, can't pull anything for an empty key.".format( me )
            print( status_message )
            attr_OUT = None

        #-- END check to see if key passed in. --#

        return value_OUT

    #-- END method pull_load_attr_name_for_key() --#


    def set_extract_first_index( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_first_index = value_IN

        # return it.
        value_OUT = self.get_extract_first_index()

        return value_OUT

    #-- END method set_extract_first_index() --#


    def set_attr_index_to_key_map( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.attr_index_to_key_map = value_IN

        # return it.
        value_OUT = self.get_attr_index_to_key_map()

        return value_OUT

    #-- END method set_attr_index_to_key_map() --#


    def set_attr_key_to_attribute_map( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.attr_key_to_attribute_map = value_IN

        # return it.
        value_OUT = self.get_attr_key_to_attribute_map()

        return value_OUT

    #-- END method set_attr_key_to_attribute_map() --#


    def set_attr_key_to_index_map( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.attr_key_to_index_map = value_IN

        # return it.
        value_OUT = self.get_attr_key_to_index_map()

        return value_OUT

    #-- END method set_attr_key_to_index_map() --#


    def set_attr_load_name_to_key_map( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.attr_load_name_to_key_map = value_IN

        # return it.
        value_OUT = self.get_attr_load_name_to_key_map()

        return value_OUT

    #-- END method set_attr_load_name_to_key_map() --#



    def set_data_attr_key_list( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.data_attr_key_list = value_IN

        # return it.
        value_OUT = self.get_data_attr_key_list()

        return value_OUT

    #-- END method set_data_attr_key_list() --#


    def set_extract_storage_type( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.extract_storage_type = value_IN

        # return it.
        value_OUT = self.get_extract_storage_type()

        return value_OUT

    #-- END method set_extract_storage_type() --#


    def set_id_attr_key_list( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.id_attr_key_list = value_IN

        # return it.
        value_OUT = self.get_id_attr_key_list()

        return value_OUT

    #-- END method set_id_attr_key_list() --#


    def set_id_match_type( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.id_match_type = value_IN

        # return it.
        value_OUT = self.get_id_match_type()

        return value_OUT

    #-- END method set_id_match_type() --#


    def set_load_class( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_class = value_IN

        # return it.
        value_OUT = self.get_load_class()

        return value_OUT

    #-- END method set_load_class() --#


    def set_load_storage_type( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.load_storage_type = value_IN

        # return it.
        value_OUT = self.get_load_storage_type()

        return value_OUT

    #-- END method set_load_storage_type() --#


    def set_related_entity_attr_key_list( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.related_entity_attr_key_list = value_IN

        # return it.
        value_OUT = self.get_related_entity_attr_key_list()

        return value_OUT

    #-- END method set_related_entity_attr_key_list() --#


    def set_required_attr_key_set( self, value_IN ):

        '''
        Accepts value.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.required_attr_key_set = value_IN

        # return it.
        value_OUT = self.get_required_attr_key_set()

        return value_OUT

    #-- END method set_required_attr_key_set() --#


    def to_json( self ):

        # return reference
        json_OUT = None

        # declare variables
        json_root = {}
        key_to_attribute_map = None
        key_to_attribute_json_map = None
        current_key = None
        current_attr_instance = None
        current_attr_json = None

        # external data information
        json_root[ "extract_storage_type" ] = self.get_extract_storage_type()
        json_root[ "extract_first_index" ] = self.get_extract_first_index()
        json_root[ "load_storage_type" ] = self.get_load_storage_type()
        json_root[ "load_class" ] = str( self.get_load_class() )

        # external storage traits

        # retrieve map of keys to ETLAttribute instances.
        key_to_attribute_map = self.get_attr_key_to_attribute_map()
        key_to_attribute_json_map = {}
        for current_key, current_attr_instance in key_to_attribute_map.items():

            # Convert attribute to JSON.
            current_attr_json = current_attr_instance.to_json()

            # add to new dictionary.
            key_to_attribute_json_map[ current_key ] = current_attr_json

        #-- END loop over key-attribute pairs --#

        # add key-to-attribute_json map.
        json_root[ "attr_key_to_attribute_map" ] = key_to_attribute_json_map

        json_root[ "attr_load_name_to_key_map" ] = self.get_attr_load_name_to_key_map()
        json_root[ "attr_index_to_key_map" ] = self.get_attr_index_to_key_map()
        json_root[ "attr_key_to_index_map" ] = self.get_attr_key_to_index_map()

        # required in extract...
        json_root[ "required_attr_key_set" ] = list( self.get_required_attr_key_set() )

        # ID - record identification
        json_root[ "id_attr_key_list" ] = self.get_id_attr_key_list()
        json_root[ "id_match_type" ] = self.get_id_match_type()

        # data attributes
        json_root[ "data_attr_key_list" ] = self.get_data_attr_key_list()

        # related entity attributes
        json_root[ "related_entity_attr_key_list" ] = self.get_related_entity_attr_key_list()

        # debug
        json_root[ "debug_flag" ] = self.debug_flag

        json_OUT = json_root

        return json_OUT

    #-- END method to_json() --#


#-- END class ETLEntity --#
