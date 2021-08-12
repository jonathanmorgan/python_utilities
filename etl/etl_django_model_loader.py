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
from python_utilities.etl.etl_object_loader import ETLObjectLoader


#===============================================================================
# class ETLObjectLoader
#===============================================================================


# lineage: object --> ETLProcessor --> ETLObjectLoader
class ETLDjangoModelLoader( ETLObjectLoader ):


    '''
    ETLDjangoModelLoader is parent class for using an ETL spec to load data from
        different types of sources into Django model instances (using attrs).
        All functionality that remains the same regardless of type of source
        lives here, is pulled in by extending this class and then building
        processing appropriate to the source.
    '''


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    #STATUS_SUCCESS = "Success!"
    #STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLDjangoModelLoader"


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

    #-- END constructor --#


    #===========================================================================
    # ! ==> instance methods
    #===========================================================================


    def find_load_instance( self, record_IN, check_required_IN = True ):

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
        my_class = None
        id_column_key_list = None
        current_entry_instance = None

        # declare variables - lookup existing row
        has_required = None
        lookup_qs = None
        current_id_key = None
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

        # ==> check required?
        if ( check_required_IN == True ):

            # check required.
            has_required = self.has_required( record_IN )

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

                # retrieve value for key.
                current_id_value = self.get_value_for_key( record_IN, current_id_key )

                # retrieve attribute name for key.
                current_id_attr_name = my_etl_spec.pull_load_attr_name_for_key( current_id_key )

                if ( my_debug_flag == True ):
                    status_message = "Looking for field {id_key} ( attr: {id_attr_name} ) with value \"{id_value}\"".format(
                        id_key = current_id_key,
                        id_attr_name = current_id_attr_name,
                        id_value = current_id_value
                    )
                    self.output_debug( status_message, method_IN = me, indent_with_IN = "====> ", do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # add to filter
                # https://stackoverflow.com/questions/9122169/calling-filter-with-a-variable-for-field-name
                lookup_qs = lookup_qs.filter( **{ current_id_attr_name: current_id_value } )

                # add to map
                attr_to_value_map[ current_id_attr_name ] = current_id_value

            #-- END loop over id column keys. --#

            # 1 match in QuerySet?
            lookup_match_count = lookup_qs.count()
            if ( lookup_match_count == 1 ):

                if ( my_debug_flag == True ):
                    status_message = "FOUND match for current input row, get()-ing instance ( count: {}; values: {}; query: {} )".format( lookup_match_count, attr_to_value_map, lookup_qs.query )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # - if yes, get()
                self.existing_count += 1
                current_entry_instance = lookup_qs.get()

            else:

                if ( my_debug_flag == True ):
                    status_message = "NO match for current input row, creating new instance ( count: {}; values: {} )".format( lookup_match_count, attr_to_value_map )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # - if no, create new instance.
                self.new_count += 1
                current_entry_instance = my_class()

            #-- END check to see if lookup count == 1 --#

            instance_OUT = current_entry_instance

        else:

            # missing required fields, move on.
            if ( my_debug_flag == True ):
                status_message = "row {} is missing required fields, moving on.".format( record_IN )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

        #-- END check if required columns are present. --#

        return instance_OUT

    #-- END method find_load_instance() --#


    def process_records(
        self,
        start_index_IN = None,
        record_count_IN = None,
        do_output_progress_IN = False
    ):

        '''
        Processes all records in iterator stored in this instance. returns
            StatusContainer instance with details on how it all went.

        Postconditions: StatusContainer returned should contain:
        - the count of the records processed during processing in a
            StatusContainer detail property named
            STATUS_PROP_PROCESSED_RECORD_COUNT ( "processed_record_count" ).
        - the count of the records with errors during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATE_ERROR_COUNT ( "update_error_count" ).
        - the count of the records successfully processed during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATE_SUCCESS_COUNT ( "update_success_count" ).
        - the count of the records updated during processing in a
            StatusContainer detail property named
            STATUS_PROP_UPDATED_RECORD_COUNT ( "updated_record_count" ).

        TODO:
        - // populate StatusContainer, rather than/in addition to status list.
        - // test and make sure this all works.
        - // move process_records up a level to ETLDjangoModelLoader.
        - // try to make "update_instance_from_record()" for Excel, see if
            "process_records()" there works the same as "process_rows()".
        '''


        # return reference
        status_OUT = None

        # declare variables
        me = "process_records"
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
        error_counter = None
        record_counter = None
        success_counter = None
        update_counter = None
        print_every_x_records = None
        current_record = None
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
        update_status = None
        was_update_success = None
        was_instance_updated = None
        unknown_attr_name_to_value_map = None

        #----------------------------------------------------------------------#
        # work

        if ( do_output_progress_IN == True ):
            # hello world.
            status_message = "\n\nTop of {me}! ( @ {right_now} )\n\n".format( me = me, right_now = datetime.datetime.now() )
            self.output_log_message(
                status_message,
                method_IN = me,
                indent_with_IN = "\n\n====> ",
                log_level_code_IN = logging.INFO,
                do_print_IN = True
            )
        #-- END check if do_output_progress_IN --#

        # init
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        self.reset_status_information()
        self.start_dt = datetime.datetime.now()
        previous_dt = self.start_dt
        error_counter = 0
        record_counter = 0
        success_counter = 0
        update_counter = 0

        # get spec information
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_etl_spec = self.get_etl_entity()
        index_to_key_map = my_etl_spec.get_attr_index_to_key_map()
        key_to_index_map = my_etl_spec.get_attr_key_to_index_map()
        required_attr_key_list = my_etl_spec.get_required_attr_key_set()
        id_column_key_list = my_etl_spec.get_id_attr_key_list()
        my_class = my_etl_spec.get_load_class()

        # get iterator
        my_iterator = self.get_record_iterator( start_index_IN = start_index_IN, record_count_IN = record_count_IN )

        # get record count
        record_count = self.get_record_count()

        # loop over data dictionaries
        error_counter = 0
        record_counter = 0
        success_counter = 0
        update_counter = 0
        print_every_x_records = self.update_status_every
        for current_record in my_iterator:

            # increment counter
            record_counter += 1
            #print( "record_counter: {counter}".format( counter = record_counter ) )

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

                    # update instance from record
                    update_status = self.update_instance_from_record( current_entry_instance, current_record )

                    # evaluate status
                    was_update_success = update_status.is_success()
                    was_instance_updated = update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED )

                    # success?
                    if ( was_update_success == True ):

                        # success
                        success_counter += 1

                    else:

                        # error
                        error_counter += 1

                    #-- END check if success. --#

                    # was record updated?
                    if ( was_instance_updated == True ):

                        # increment update counter
                        update_counter += 1

                    #-- END check if instance was updated --#

                    if ( my_debug_flag == True ):

                        # output details of entry update.
                        status_message = "- in {method}(): update_status = {status_instance} ( success?: {success_flag}; record updated?: {was_updated}; changed list:{changed_list}".format(
                            method = me,
                            status_instance = update_status,
                            success_flag = was_update_success,
                            was_updated = was_instance_updated,
                            changed_list = update_status.get_detail_value( self.PROP_UPDATED_ATTR_LIST )
                        )
                        self.output_debug( status_message, method_IN = me, indent_with_IN = "\n\n====> ", do_print_IN = my_debug_flag )

                        # and, output unknown attributes.
                        status_message = "- in {method}(): unknown_attr_name_to_value_map = {unknown_attrs}".format(
                            method = me,
                            unknown_attrs = unknown_attr_name_to_value_map
                        )
                        self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )

                    #-- END DEBUG --#

                else:

                    status_message = "In {}(): row {} - failed to find instance of class {} to load into. This shouldn't happen.".format( me, current_row_index, my_class )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                    self.add_status_message( status_message )

                #-- END check to see if instance to load into --#

            else:

                # missing required fields, move on.
                status_message = "record {record_number} is missing required fields, moving on.".format(
                    record_number = record_counter
                )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #self.output_debug( status_message, method_IN = me, do_print_IN = True )
                self.add_status_message( status_message )

            #-- END check if required columns are present. --#

            # output a progress message?
            if ( ( ( record_counter % print_every_x_records ) == 0 )
                and ( do_output_progress_IN == True ) ):

                # basic timing analysis.
                my_start_dt = self.start_dt
                current_dt = datetime.datetime.now()
                current_elapsed = current_dt - previous_dt
                total_elapsed = current_dt - my_start_dt
                total_average = total_elapsed / record_counter
                previous_dt = current_dt

                status_message = "processed {counter} of {count} records ( existing: {existing_count}; new: {new_count} ) @ {right_now} ( timing: last {current_count} elapsed = {current_elapsed}; total elapsed = {total_elapsed}; average = {total_average} ).".format(
                    counter = record_counter,
                    count = record_count,
                    existing_count = self.existing_count,
                    new_count = self.new_count,
                    right_now = current_dt,
                    current_count = print_every_x_records,
                    current_elapsed = current_elapsed,
                    total_elapsed = total_elapsed,
                    total_average = total_average
                )
                self.output_log_message(
                    status_message,
                    method_IN = me,
                    indent_with_IN = "\n\n----> ",
                    log_level_code_IN = logging.INFO,
                    do_print_IN = True
                )
            #-- END periodic status update. --#

        #-- END loop over records --#

        # output final status message?
        if ( do_output_progress_IN == True ):

            my_start_dt = self.start_dt
            current_dt = datetime.datetime.now()
            current_elapsed = current_dt - previous_dt
            total_elapsed = current_dt - my_start_dt
            total_average = total_elapsed / record_counter
            previous_dt = current_dt

            status_message = "Processing COMPLETE - processed {counter} of {count} records ( existing: {existing_count}; new: {new_count} ) @ {right_now} ( timing: last {current_count} elapsed = {current_elapsed}; total elapsed = {total_elapsed}; average = {total_average} ).".format(
                counter = record_counter,
                count = record_count,
                existing_count = self.existing_count,
                new_count = self.new_count,
                right_now = current_dt,
                current_count = ( record_count % print_every_x_records ),
                current_elapsed = current_elapsed,
                total_elapsed = total_elapsed,
                total_average = total_average
            )
            self.output_log_message(
                status_message,
                method_IN = me,
                indent_with_IN = "\n\n====> ",
                log_level_code_IN = logging.INFO,
                do_print_IN = True
            )
        #-- END check if we are outputting progress. --#

        # set record, error, success, and update counts in status
        status_OUT.set_detail_value( self.STATUS_PROP_PROCESSED_RECORD_COUNT, record_counter )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATE_ERROR_COUNT, error_counter )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATE_SUCCESS_COUNT, success_counter )
        status_OUT.set_detail_value( self.STATUS_PROP_UPDATED_RECORD_COUNT, update_counter )

        return status_OUT

    #-- END method process_records() --#


    def update_instance_from_record( self, instance_IN, record_IN, save_on_success_IN = True ):

        '''
        postconditions: StatusContainer returned here should contain:
        - ETLObjectLoader.PROP_WAS_INSTANCE_UPDATED ( "was_instance_updated" ) -
            set to True if instance was updated.
        - ETLObjectLoader.PROP_UPDATED_ATTR_LIST ( "updated_attr_list" ) - list
            of ETLAttribute instances of attributes that were updated.

        It can also contain (currently not set):
        - ETLObjectLoader.PROP_NO_CHANGE_ATTR_LIST ( "no_change_attr_list" )
        - ETLObjectLoader.PROP_ERROR_ATTR_LIST ( "error_attr_list" )
        - ETLObjectLoader.PROP_SUCCESS_STATUS_LIST ( "success_status_list" )
        - ETLObjectLoader.PROP_ERROR_STATUS_LIST ( "error_status_list" )
        '''

        # return reference
        status_OUT = None

        # status_OUT should contain a StatusContainer instance.

        # declare variables
        me = "update_instance_from_record"

        raise ETLError( "In abstract-ish method ETLDjangoModelLoader.{}(): OVERRIDE ME".format( me ) )

        return status_OUT

    #-- END method update_instance_from_record() --#


#-- END class ETLDjangoModelLoader --#
