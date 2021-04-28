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

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError
from python_utilities.etl.etl_processor import ETLProcessor
from python_utilities.etl.etl_object_loader import ETLObjectLoader
from python_utilities.etl.etl_django_model_loader import ETLDjangoModelLoader


#===============================================================================
# class ETLFromExcelWithHeaders
#===============================================================================


# lineage: object --> ETLProcessor --> ETLObjectLoader --> ETLDjangoModelLoader
class ETLFromExcelWithHeaders( ETLDjangoModelLoader ):


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    #STATUS_SUCCESS = "Success!"
    #STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLFromExcelWithHeaders"


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
        self.input_worksheet = None

        # status - worksheet-level
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

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def get_input_worksheet( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.input_worksheet

        return value_OUT

    #-- END method get_input_worksheet() --#


    def get_value_for_key( self, record_IN, key_IN ):

        # return reference
        value_OUT = False

        # input parameters
        row_index_IN = None

        # declare variables
        me = "get_value_for_key"
        status_message = None
        my_debug_flag = None
        my_worksheet = None
        current_column_index = None
        current_cell = None
        current_value = None

        # init
        my_debug_flag = self.debug_flag
        row_index_IN = record_IN  # for this type, pass index, not record.

        # get spec information
        my_worksheet = self.get_input_worksheet()
        my_etl_spec = self.get_etl_entity()

        if ( my_debug_flag == True ):
            status_message = "Getting value for key: {}".format( key_IN )
            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        # retrieve column index
        current_column_index = my_etl_spec.pull_index_for_key( key_IN )

        if ( my_debug_flag == True ):
            status_message = "- Current column index: {}".format( current_column_index )
            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        if ( ( current_column_index is not None ) and ( current_column_index != "" ) ):

            # retrieve value from this row.
            current_cell = my_worksheet.cell( row = row_index_IN, column = current_column_index )
            current_value = current_cell.value
            value_OUT = current_value

            if ( my_debug_flag == True ):
                status_message = "- Current column value: {}".format( current_value )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

        else:

            # ERROR
            status_message = "In method ETLFromExcelWithHeaders.{method_name}(): No index found for key {key_name}.".format(
                method_name = me,
                key_name = key_IN
            )
            self.output_log_message( status_message, me, log_level_code_IN = logging.ERROR, do_print_IN = True )

            # unknown key - can't get value.
            value_OUT = None

            raise ETLError( status_message )

        #-- END check to see if key maps to index. --#

        return value_OUT

    #-- END method get_value_for_key() --#


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
                status_message = "index {index}; name = {name} ( exists?: {exists_flag} )".format(
                    index = current_column_index,
                    name = current_column_name,
                    exists_flag = attr_exists
                )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
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
            self.reset_record_information()
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
                        status_message = "unknown_attr_name_to_value_map = {}".format( unknown_attr_name_to_value_map )
                        self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                    #-- END DEBUG --#

                    # All processed. Save.
                    current_entry_instance.save()

                else:

                    status_message = "In {}(): row {} - failed to find instance of class {} to load into. This shouldn't happen.".format( me, current_row_index, my_class )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                    self.add_status_message( status_message )

                #-- END check to see if instance to load into --#

            else:

                # missing required fields, move on.
                status_message = "row {} is missing required fields, moving on.".format( current_row_index )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
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

                self.output_debug( status_message, method_IN = me, do_print_IN = True )
            #-- END periodic status update. --#

        #-- END loop over rows in openpyxl worksheet --#

    #-- END method process_rows() --#


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


#-- END class ETLFromExcelWithHeaders --#
