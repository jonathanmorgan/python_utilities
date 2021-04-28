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
        my_worksheet = None
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
        my_worksheet = self.get_input_worksheet()

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

                if ( my_debug_flag == True ):
                    status_message = "Current ID key: {}".format( current_id_key )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # retrieve value for key.
                current_id_value = self.get_value_for_key( record_IN, current_id_key )

                if ( my_debug_flag == True ):
                    status_message = "- Current ID value: {}".format( current_id_value )
                    self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                #-- END DEBUG --#

                # retrieve attribute name for key.
                current_id_attr_name = my_etl_spec.pull_load_attr_name_for_key( current_id_key )

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


#-- END class ETLObjectLoader --#
