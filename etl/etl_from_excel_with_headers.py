# TODO
# - formal logging for debugging, other messages (extend LoggingHelper or ExceptionHelper).
# - parent class for everything that isn't Excel-specific (value-level stuff,
#     for example...).
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

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError


#===============================================================================
# class ETLFromExcelWithHeaders
#===============================================================================


# lineage: object
class ETLFromExcelWithHeaders( object ):


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "etl_attribute"


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
        self.input_worksheet = None

        # status - worksheet-level
        self.status_message_list = []
        self.latest_status = None
        self.unknown_attrs_list = []
        self.existing_count = 0
        self.new_count = 0
        self.start_dt = None

        # status - row-level
        self.unknown_attrs_name_to_value_map = {}

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


    def find_load_instance( self, row_index_IN, check_required_IN = True ):

        '''
        Finds instance of model into which we are "load"-ing
            (Extract-Transform-Load).
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "find_load_instance"
        status_message = None
        my_debug_flag = None
        my_etl_spec = None
        my_worksheet = None
        my_class = None
        id_column_key_list = None
        current_entry_instance = None

        # declare variables - lookup existing row
        has_required = None
        lookup_qs = None
        current_id_key = None
        current_id_index = None
        current_id_cell = None
        current_id_value = None
        current_id_attr_name = None
        attr_to_value_map = None
        lookup_match_count = None

        #----------------------------------------------------------------------#
        # work

        # init
        my_debug_flag = self.debug_flag

        # get spec information
        my_etl_spec = self.get_etl_entity()
        id_column_key_list = my_etl_spec.get_id_attr_key_list()
        my_class = my_etl_spec.get_load_class()

        # get worksheet
        my_worksheet = self.get_input_worksheet()

        # ==> check required?
        if ( check_required_IN == True ):

            # check required.
            has_required = self.has_required( row_index_IN )

        else:

            # not checking required - assume true.
            has_required = True

        #-- END check to see if required. --#

        if ( has_required == True ):

            # ==> try to lookup existing instance.
            lookup_qs = my_class.objects.all()
            current_entry_instance = None
            attr_to_value_map = {}

            # loop over id keys
            for current_id_key in id_column_key_list:

                if ( my_debug_flag == True ):
                    print( "Current ID key: {}".format( current_id_key ) )
                #-- END DEBUG --#

                # find index.
                current_id_index = my_etl_spec.pull_index_for_key( current_id_key )

                if ( my_debug_flag == True ):
                    print( "- Current ID index: {}".format( current_id_index ) )
                #-- END DEBUG --#

                if ( ( current_id_index is not None ) and ( current_id_index != "" ) ):

                    # retrieve value from this row.
                    current_id_cell = my_worksheet.cell( row = row_index_IN, column = current_id_index )
                    current_id_value = current_id_cell.value

                    if ( my_debug_flag == True ):
                        print( "- Current ID value: {}".format( current_id_value ) )
                    #-- END DEBUG --#

                    # retrieve attribute name for key.
                    current_id_attr_name = my_etl_spec.pull_load_attr_name_for_key( current_id_key )

                    # add to filter
                    # https://stackoverflow.com/questions/9122169/calling-filter-with-a-variable-for-field-name
                    lookup_qs = lookup_qs.filter( **{ current_id_attr_name: current_id_value } )

                    # add to map
                    attr_to_value_map[ current_id_attr_name ] = current_id_value

                #-- END check to see if we have an index --#

            #-- END loop over id column keys. --#

            # 1 match in QuerySet?
            lookup_match_count = lookup_qs.count()
            if ( lookup_match_count == 1 ):

                # - if yes, get()
                if ( my_debug_flag == True ):
                    status_message = "in {}(): FOUND match for current input row, get()-ing instance ( count: {}; values: {}; query: {} )".format( me, lookup_match_count, attr_to_value_map, lookup_qs.query )
                    print( status_message )
                #-- END DEBUG --#

                self.existing_count += 1
                current_entry_instance = lookup_qs.get()

            else:

                # - if no, create new instance.
                status_message = "in {}(): NO match for current input row, creating new instance ( count: {}; values: {} )".format( me, lookup_match_count, attr_to_value_map )

                if ( my_debug_flag == True ):
                    print( status_message )
                #-- END DEBUG --#

                self.new_count += 1
                current_entry_instance = my_class()

            #-- END check to see if lookup count == 1 --#

            instance_OUT = current_entry_instance

        else:

            # missing required fields, move on.
            if ( my_debug_flag == True ):
                print( "in {}(): row {} is missing required fields, moving on.".format( me, row_index_IN ) )
            #-- END DEBUG --#

        #-- END check if required columns are present. --#

        return instance_OUT

    #-- END method find_load_instance() --#


    def get_etl_entity( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.etl_entity

        return value_OUT

    #-- END method get_etl_entity() --#


    def get_input_worksheet( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.input_worksheet

        return value_OUT

    #-- END method get_input_worksheet() --#


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


    def has_required( self, row_index_IN ):

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
        current_required_index = None
        current_required_cell = None
        current_required_value = None

        # init
        my_debug_flag = self.debug_flag

        # get spec information
        my_worksheet = self.get_input_worksheet()
        my_etl_spec = self.get_etl_entity()
        key_to_index_map = my_etl_spec.get_attr_key_to_index_map()
        required_attr_key_list = my_etl_spec.get_required_attr_key_set()

        # ==> check required.
        has_required_OUT = True
        missing_field_list = []

        # loop over required keys
        for current_required_key in required_attr_key_list:

            if ( my_debug_flag == True ):
                print( "Current required key: {}".format( current_required_key ) )
            #-- END DEBUG --#

            # retrieve index
            current_required_index = my_etl_spec.pull_index_for_key( current_required_key )

            if ( my_debug_flag == True ):
                print( "- Current required index: {}".format( current_required_index ) )
            #-- END DEBUG --#

            if ( ( current_required_index is not None ) and ( current_required_index != "" ) ):

                # retrieve value from this row.
                current_required_cell = my_worksheet.cell( row = row_index_IN, column = current_required_index )
                current_required_value = current_required_cell.value

                if ( my_debug_flag == True ):
                    print( "- Current required value: {}".format( current_required_value ) )
                #-- END DEBUG --#

                # Is it set? Needs to not be None, and not be empty.
                if ( ( current_required_value is None ) or ( current_required_value == "" ) ):

                    # not set.
                    missing_field_list.append( "key: {}; index: {}".format( current_required_key, current_required_index ) )
                    has_required_OUT = False

                    if ( my_debug_flag == True ):
                        print( "- Current value MISSING!" )
                    #-- END DEBUG --#

                else:

                    # set.
                    if ( my_debug_flag == True ):
                        print( "- Current value FOUND!" )
                    #-- END DEBUG --#

                #-- END check if value is present. --#

            else:

                # no index for required key - this counts as missing required.
                has_required_OUT = False

                # TODO: and probably means the whole file is broken, so we should raise an exception.

            #-- END check to see if we have an index --#

        #-- END loop over required keys --#

        return has_required_OUT

    #-- END method has_required() --#


    def map_indexes_to_keys( self ):

        # declare variables
        me = "map_indexes_to_keys"
        status_message = None
        my_debug_flag = None
        my_etl_spec = None
        my_worksheet = None
        my_class = None
        index_to_key_map = None
        key_to_index_map = None
        missing_attr_list = None

        # declare variables - column processing
        column_count = None
        header_row_number = None
        current_column_index = None
        current_cell = None
        current_column_name = None
        attr_exists = None

        #----------------------------------------------------------------------#
        # work

        my_debug_flag = self.debug_flag

        # get instances
        my_etl_spec = self.get_etl_entity()
        my_worksheet = self.get_input_worksheet()
        my_class = my_etl_spec.get_load_class()

        # create dictionaries in which we store maps of index to value and value to index for each column in first row.
        index_to_key_map = {}
        key_to_index_map = {}
        missing_attr_list = []

        # initialize processing
        column_count = my_worksheet.max_column
        header_row_number = 1

        # loop over columns to get value from first row for each.
        for current_column_index in range( 1, column_count + 1 ):

            # retrieve value for this cell
            current_cell = my_worksheet.cell( row = header_row_number, column = current_column_index )
            current_column_name = current_cell.value

            # store in index-to-name map
            index_to_key_map[ current_column_index ] = current_column_name
            key_to_index_map[ current_column_name ] = current_column_index

            # is this name in the instance?
            attr_exists = hasattr( my_class, current_column_name )

            if ( my_debug_flag == True ):
                status_message = "In {}(): index {}; name = {} ( exists?: {} )".format( me, current_column_index, current_column_name, attr_exists )
                print( status_message )
            #-- END DEBUG --#

            # if name not in instance, add to list for processing.
            if ( attr_exists == False ):

                # attr does not exist.
                missing_attr_list.append( current_column_name )

            #-- END check if has attr --#

        #-- END loop over columns in 1st row --#

        # store the maps.
        my_etl_spec.set_attr_index_to_key_map( index_to_key_map )
        my_etl_spec.set_attr_key_to_index_map( key_to_index_map )

        # store unknown attributes.
        self.set_unknown_attrs_list( missing_attr_list )

        status_message = "fields that don't correspond to attrs in instance: {}".format( missing_attr_list )
        self.add_status_message( status_message )

    #-- END method map_indexes_to_keys() --#


    def process_rows( self, start_row_IN = -1, row_count_IN = -1 ):

        # declare variables
        me = "process_rows"
        status_message = None
        my_debug_flag = None
        my_etl_spec = None
        index_to_key_map = None
        key_to_index_map = None
        my_worksheet = None
        my_class = None

        # declare variables - loop over rows
        row_count = None
        column_count = None
        first_data_row_index = 2
        end_data_row_index = 2
        row_counter = None
        print_every_x_rows = None
        current_row_index = None
        id_column_key_list = None
        current_entry_instance = None

        # declare variables - timing
        my_start_dt = None
        previous_dt = None
        current_dt = None
        current_elapsed = None
        total_elapsed = None
        total_average = None

        # declare variables - check required
        has_required = None

        # declare variables - update and save
        current_column_index = None
        current_column_value = None
        current_column_key = None
        my_etl_attribute = None
        current_attr_name = None
        current_attr_value = None
        unknown_attr_name_to_value_map = None

        #----------------------------------------------------------------------#
        # work

        # init
        my_debug_flag = self.debug_flag
        self.reset_status_information()
        self.start_dt = datetime.datetime.now()
        previous_dt = self.start_dt

        # get spec information
        my_etl_spec = self.get_etl_entity()
        index_to_key_map = my_etl_spec.get_attr_index_to_key_map()
        key_to_index_map = my_etl_spec.get_attr_key_to_index_map()
        required_attr_key_list = my_etl_spec.get_required_attr_key_set()
        id_column_key_list = my_etl_spec.get_id_attr_key_list()
        my_class = my_etl_spec.get_load_class()

        # get worksheet
        my_worksheet = self.get_input_worksheet()
        row_count = my_worksheet.max_row
        column_count = my_worksheet.max_column

        # where do we start?
        if ( ( start_row_IN is not None ) and ( start_row_IN != "" ) and ( start_row_IN > 0 ) ):

            # start row passed in - use that.
            first_data_row_index = start_row_IN

        else:

            # default
            first_data_row_index = 2

        #-- END check to see if custom start row --#

        # where do we stop?
        if ( ( row_count_IN is not None ) and ( row_count_IN != "" ) and ( row_count_IN > 0 ) ):

            # row count passed in - use that.
            end_data_row_index = first_data_row_index + row_count_IN - 1

        else:

            # default
            end_data_row_index = row_count

        #-- END check to see if custom start row --#

        # loop over data rows
        row_counter = 0
        print_every_x_rows = self.update_status_every
        for current_row_index in range( first_data_row_index, end_data_row_index + 1 ):

            # ==> reset per-row variables
            self.reset_row_information()
            unknown_attr_name_to_value_map = self.get_unknown_attrs_name_to_value_map()

            # ==> check required.
            has_required = self.has_required( current_row_index )

            if ( has_required == True ):

                # ==> try to lookup existing instance.
                current_entry_instance = self.find_load_instance( current_row_index, check_required_IN = False )

                # got an instance?
                if ( current_entry_instance is not None ):

                    # loop over columns to get values each column and store in instance.
                    for current_column_index in range( 1, column_count + 1 ):

                        # retrieve value for this cell
                        current_cell = my_worksheet.cell( row = current_row_index, column = current_column_index )
                        current_column_value = current_cell.value

                        # get key for index.
                        current_column_key = my_etl_spec.pull_key_for_index( current_column_index )

                        # start with attribute value set to column value
                        current_attr_value = current_column_value

                        # retrieve ETLAttribute for this index.
                        my_etl_attribute = my_etl_spec.pull_attr_for_key( current_column_key )

                        # got an attribute spec?
                        if ( my_etl_attribute is not None ):

                            # ETLAttribute found.  Retrieve values and do
                            #     processing.
                            current_attr_name = my_etl_attribute.get_load_attr_name()

                            # process value.
                            current_attr_value = self.process_value( current_attr_value, my_etl_attribute, current_entry_instance )

                        else:

                            # no ETLAttribute instance. Direct, untranslated
                            #     load to instance.
                            current_attr_name = current_column_key

                        #-- END check to see if attribute spec. --#

                        # store the value.
                        self.store_attribute( current_entry_instance, current_attr_name, current_attr_value )

                    #-- END loop over columns in row --#

                    # TODO: place unknown fields into JSONField.

                    if ( my_debug_flag == True ):
                        print( "- in {}(): unknown_attr_name_to_value_map = {}".format( me, unknown_attr_name_to_value_map ) )
                    #-- END DEBUG --#

                    # All processed. Save.
                    current_entry_instance.save()

                else:

                    status_message = "In {}(): row {} - failed to find instance of class {} to load into. This shouldn't happen.".format( me, current_row_index, my_class )
                    self.add_status_message( status_message )

                #-- END check to see if instance to load into --#

            else:

                # missing required fields, move on.
                status_message = "row {} is missing required fields, moving on.".format( current_row_index )
                self.add_status_message( status_message )

            #-- END check if required columns are present. --#

            # increment counter
            row_counter += 1

            # output a message?
            if ( ( row_counter % print_every_x_rows ) == 0 ):
                my_start_dt = self.start_dt
                current_dt = datetime.datetime.now()
                current_elapsed = current_dt - previous_dt
                total_elapsed = current_dt - my_start_dt
                total_average = total_elapsed / row_counter
                previous_dt = current_dt

                status_message = "----> processed {} of {} records ( existing: {}; new: {} ) @ {} ( timing: last {} elapsed = {}; total elapsed = {}; average = {} ).".format(
                            row_counter,
                            row_count,
                            self.existing_count,
                            self.new_count,
                            current_dt,
                            row_counter,
                            current_elapsed,
                            total_elapsed,
                            total_average )

                print( status_message )
            #-- END periodic status update. --#

        #-- END loop over rows in openpyxl worksheet --#

    #-- END method process_rows() --#


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
                    print( "ETLAttribute JSON string:" )
                    print( json_string )
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
                        value_OUT = int( value_IN )

                        if ( my_debug_flag == True ):
                            print( "In {}(): translated {} to int {}".format( me, value_IN, value_OUT ) )
                        #-- END DEBUG --#

                    # simple type - string
                    elif ( out_data_type == ETLAttribute.DATA_TYPE_STRING ):

                        # convert to string
                        value_OUT = str( value_IN )

                        if ( my_debug_flag == True ):
                            print( "In {}(): translated {} to string {}".format( me, value_IN, value_OUT ) )
                        #-- END DEBUG --#

                    # complex type - datetime.datetime
                    elif ( out_data_type == ETLAttribute.DATA_TYPE_DATETIME_DATETIME ):

                        # is there a transform pattern?
                        if ( ( transform_pattern is not None ) and ( transform_pattern != "" ) ):

                            # parse using pattern.
                            value_OUT = datetime.datetime.strptime( value_IN, transform_pattern )

                        else:

                            # no pattern, let dateutil try to figure it out.
                            value_OUT = dateutil.parser.parse( value_IN )

                        #-- check if transform pattern. --#

                        if ( my_debug_flag == True ):
                            print( "In {}(): translated {} to datetime {}".format( me, value_IN, value_OUT ) )
                        #-- END DEBUG --#

                    # unknown type.
                    else:

                        # unknown output type - nothing to do.
                        status_message = "In {}(): unknown output type \"{}\", nothing to be done.".format( me, out_data_type )
                        if ( my_debug_flag == True ):
                            print( status_message )
                        #-- END DEBUG --#

                    #-- END check to see what type we want --#

                    # are we transforming to a separate attribute?
                    if ( ( transform_to_attr_name is not None ) and ( transform_to_attr_name != "" ) ):

                        if ( my_debug_flag == True ):
                            print( "In {}(): storing translated value {} in attr {}".format( me, value_OUT, transform_to_attr_name ) )
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
                        print( status_message )
                    #-- END DEBUG --#

                #-- END check to see if output type set. --#

            else:

                # no value - nothing to do.
                status_message = "In {}(): no value passed in, nothing to be done.".format( me )
                if ( my_debug_flag == True ):
                    print( status_message )
                #-- END DEBUG --#

            #-- check if value. --#

        else:

            # no spec - nothing to do.
            status_message = "In {}(): no spec for value, nothing to be done.".format( me )
            if ( my_debug_flag == True ):
                print( status_message )
            #-- END DEBUG --#

        #-- END check if spec --#

        return value_OUT

    #-- END method process_value() --#


    def reset_row_information( self ):

        # status - row-level
        self.unknown_attrs_name_to_value_map = {}

    #-- END method reset_row_information() --#


    def reset_status_information( self ):

        # reset status variables. - worksheet-level
        self.status_message_list = []
        self.latest_status = None
        self.unknown_attrs_list = []
        self.existing_count = 0
        self.new_count = 0
        self.start_dt = None

        # status - row-level
        self.reset_row_information()

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


    def set_input_worksheet( self, value_IN ):

        # return reference
        value_OUT = None

        # store value
        self.input_worksheet = value_IN

        # clear out status variables.
        self.reset_status_information()

        # return value
        value_OUT = self.get_input_worksheet()

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


    def store_attribute( self, instance_IN, attr_name_IN, attr_value_IN ):

        # return reference
        status_OUT = None

        # declare variables
        me = "store_attribute"
        status_message = None
        my_debug_flag = None
        my_etl_spec = None
        my_class = None
        attr_exists = None
        unknown_attr_name_to_value_map = None
        extra_data_json = None

        # init
        my_debug_flag = self.debug_flag

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
                    print( "- attr_name = {} ( exists?: {} ); attr_value".format( attr_name_IN, attr_exists, attr_value_IN ) )
                #-- END DEBUG --#

                # if name in instance, store value. If not, add to list for processing.
                if ( attr_exists == True ):

                    # Store the value.
                    setattr( instance_IN, attr_name_IN, attr_value_IN )

                else:

                    # attribute does not exist. Add to the unknown attribute map.
                    unknown_attr_name_to_value_map = self.get_unknown_attrs_name_to_value_map()
                    unknown_attr_name_to_value_map[ attr_name_IN ] = attr_value_IN

                    # update the value for this attribute in the extra_data
                    #     JSONField.
                    instance_IN.update_extra_data_attr( attr_name_IN, attr_value_IN )

                #-- END check if has attr --#

            else:

                # no name. error.
                status_message = "ERROR in {}(): no attribute name passed in, nothing to be done.".format( me )
                # TODO: raise ETLError.
                if ( my_debug_flag == True ):
                    print( status_message )
                #-- END DEBUG --#

            #-- END check to see if attribute name passed in --#

        else:

            # no instance. error.
            status_message = "ERROR in {}(): no load instance passed in, nothing to be done.".format( me )
            # TODO: raise ETLError.
            if ( my_debug_flag == True ):
                print( status_message )
            #-- END DEBUG --#

        #-- END check to see if instance --#

    #-- END method store_attributes() --#

#-- END class ETLFromExcelWithHeaders --#
