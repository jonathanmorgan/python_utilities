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
class ETLFromDictionaryIterable( ETLDjangoModelLoader ):


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


    def get_value_for_key( self, record_IN, key_IN ):

        # return reference
        value_OUT = False

        # declare variables
        me = "get_value_for_key"
        status_message = None
        my_debug_flag = None
        current_value = None

        # init
        my_debug_flag = self.debug_flag

        if ( my_debug_flag == True ):
            status_message = "Getting value for key: {}".format( key_IN )
            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        current_value = record_IN.get( key_IN, None )
        value_OUT = current_value

        if ( my_debug_flag == True ):
            status_message = "- Current value: {}".format( current_value )
            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        return value_OUT

    #-- END method get_value_for_key() --#


    def process_records( self, start_index_IN = None, index_count_IN = None ):

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
        record_count = None
        my_iterator = None
        start_index = None
        stop_index = None
        record_counter = None
        print_every_x_records = None
        current_record = None
        current_entry_instance = None
        current_key = None
        current_value = None

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

        # get iterator
        my_iterator = self.get_record_iterator()

        # process a subset?
        if ( ( start_index_IN is not None )
            or ( index_count_IN is not None ) ):

            # we have been asked to subset. See how we call itertools.islice()
            # - start is 0-indexed
            # - stop stops at and does not return the index you pass to stop (so
            #     if you want from 0 to 9, start is 0, count is 10). If you want
            #     from 4 to 9, start index is 4, count is 6, so stop will be 10).
            if ( ( start_index_IN is not None )
                and ( index_count_IN is not None ) ):

                # we have both start and count.
                start_index = start_index_IN
                stop_index = start_index_IN + index_count_IN

            elif ( ( start_index_IN is not None )
                and ( index_count_IN is None ) ):

                # we have start, no count.
                start_index = start_index_IN
                stop_index = None

            elif ( ( start_index_IN is None )
                and ( index_count_IN is not None ) ):

                # no start, just count (limit).
                start_index = 0
                stop_index = index_count_IN

            #-- END check to see how to set start and stop.

            # islice the iterator
            my_iterator = itertools.islice( my_iterator, start_index, stop_index )

        else:

            # just use the iterator.
            pass

        #-- END check to see if custom start row --#

        # get record count
        record_count = sum( 1 for current_record in my_iterator )

        # loop over data dictionaries
        record_counter = 0
        print_every_x_records = self.update_status_every
        for current_record in my_iterator:

            # ==> reset per-row variables
            self.reset_record_information()
            unknown_attr_name_to_value_map = self.get_unknown_attrs_name_to_value_map()

            # ==> check required.
            has_required = self.has_required( current_record )
            if ( has_required == True ):

                # ==> try to lookup existing instance.
                current_entry_instance = self.find_load_instance( current_record, check_required_IN = False )

                # got an instance?
                if ( current_entry_instance is not None ):

                    # loop over keys/names in current record to get values for
                    #     each and store in instance.
                    for current_key, current_value in current_record.items():

                        # start with attribute value set to column value
                        current_attr_value = current_value

                        # retrieve ETLAttribute for this index.
                        my_etl_attribute = my_etl_spec.pull_attr_for_key( current_key )

                        # TODO: deal with value being JSON that needs to be handed off to a child model.

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
                            current_attr_name = current_key

                        #-- END check to see if attribute spec. --#

                        # store the value.
                        self.store_attribute( current_entry_instance, current_attr_name, current_attr_value )

                    #-- END loop over columns in row --#

                    # TODO: place unknown fields into JSONField.

                    if ( my_debug_flag == True ):
                        status_message = "- in {}(): unknown_attr_name_to_value_map = {}".format( me, unknown_attr_name_to_value_map )
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
            record_counter += 1

            # output a message?
            if ( ( record_counter % print_every_x_records ) == 0 ):
                my_start_dt = self.start_dt
                current_dt = datetime.datetime.now()
                current_elapsed = current_dt - previous_dt
                total_elapsed = current_dt - my_start_dt
                total_average = total_elapsed / record_counter
                previous_dt = current_dt

                status_message = "----> processed {} of {} records ( existing: {}; new: {} ) @ {} ( timing: last {} elapsed = {}; total elapsed = {}; average = {} ).".format(
                            record_counter,
                            record_count,
                            self.existing_count,
                            self.new_count,
                            current_dt,
                            record_counter,
                            current_elapsed,
                            total_elapsed,
                            total_average )

                self.output_debug( status_message, method_IN = me, do_print_IN = True )
            #-- END periodic status update. --#

        #-- END loop over rows in openpyxl worksheet --#

    #-- END method process_records() --#

#-- END class ETLFromDictionaryIterable --#
