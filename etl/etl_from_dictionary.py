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

# python_utilities
from python_utilities.status.status_container import StatusContainer

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError
from python_utilities.etl.etl_processor import ETLProcessor
from python_utilities.etl.etl_object_loader import ETLObjectLoader
from python_utilities.etl.etl_django_model_loader import ETLDjangoModelLoader


#===============================================================================
# class ETLFromDictionary
#===============================================================================


# lineage: object --> ETLProcessor --> ETLObjectLoader --> ETLDjangoModelLoader
class ETLFromDictionary( ETLDjangoModelLoader ):


    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    #STATUS_SUCCESS = "Success!"
    #STATUS_PREFIX_ERROR = "ERROR: "

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.ETLFromDictionary"


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


    def update_instance_from_record( self, instance_IN, record_IN, save_on_success_IN = True ):

        # return reference
        status_OUT = None

        # declare variables
        me = "update_instance_from_record"
        my_debug_flag = None
        status_message = None
        my_etl_spec = None
        current_entry_instance = None
        current_record = None
        current_key = None
        current_value = None
        current_attr_name = None
        current_attr_value = None
        my_etl_attribute = None
        store_status = None
        store_update_details = None
        store_success = None
        custom_update_status = None
        custom_update_success = None
        related_update_status = None
        related_update_success = None
        did_custom_updates = False

        # declare variables - status checking
        was_attr_updated = None
        was_instance_updated = None
        updated_attr_list = None
        no_change_attr_list = None
        error_attr_list = None
        success_status_list = None
        error_status_list = None

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_debug_flag = self.debug_flag
        my_etl_spec = self.get_etl_entity()
        current_entry_instance = instance_IN
        current_record = record_IN

        # init status checking variables
        was_instance_updated = False
        updated_attr_list = []
        no_change_attr_list = []
        error_attr_list = []
        success_status_list = []
        error_status_list = []

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
                store_status = self.store_attribute( current_entry_instance, current_attr_name, current_attr_value )

                # success?
                store_success = store_status.is_success()
                store_update_details = store_status.get_detail_value( self.PROP_ATTR_UPDATE_DETAIL )
                if ( store_success == True ):

                    # success.
                    success_status_list.append( store_status )

                    # was attribute updated?
                    was_attr_updated = store_status.get_detail_value( self.PROP_WAS_ATTR_UPDATED, None )
                    if ( was_attr_updated == True ):

                        # updated.
                        was_instance_updated = True
                        updated_attr_list.append( store_update_details )

                    else:

                        # not updated.
                        no_change_attr_list.append( store_update_details )

                    #-- END check to see if attribute updated. --#

                else:

                    # error.
                    error_attr_list.append( store_update_details )
                    error_status_list.append( store_status )

                #-- END check to see if update was a success --#

            #-- END loop values in record --#

            # call current_entry_instance.update_from_record_pre_save(),
            #     which can be overridden in a particular class to do
            #     fancier processing than specification can hold.
            custom_update_status = current_entry_instance.update_from_record_pre_save( current_record )

            # success?
            custom_update_success = custom_update_status.is_success()
            if ( custom_update_success == True ):

                # success.
                success_status_list.append( custom_update_status )

                # was instance updated?
                was_custom_updated = custom_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                if ( was_custom_updated == True ):

                    # updated.
                    was_instance_updated = True

                #-- END check to see if attribute updated. --#

            else:

                # error.
                error_status_list.append( custom_update_status )

            #-- END check to see if update was a success --#

            # status - success?
            if ( len( error_status_list ) == 0 ):

                # success!
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                status_message = "Success!"
                status_OUT.add_message( status_message )

                # All processed. Save?
                if ( ( was_instance_updated == True )
                    and ( save_on_success_IN == True ) ):

                    # changed, and we are saving...
                    current_entry_instance.save()

                #-- END check to see if we save(). --#

                # call current_entry_instance.update_from_record_post_save(),
                #     which can be overridden in a particular class to do
                #     fancier processing for related records.
                related_update_status = current_entry_instance.update_from_record_post_save( current_record )

                # success?
                related_update_success = related_update_status.is_success()
                if ( related_update_success == True ):

                    # success.
                    success_status_list.append( related_update_status )

                    # was instance updated?
                    was_custom_updated = related_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                    if ( was_custom_updated == True ):

                        # updated.
                        was_instance_updated = True

                    #-- END check to see if attribute updated. --#

                else:

                    # error.
                    error_status_list.append( related_update_status )

                #-- END check to see if update was a success --#

            else:

                # not success!
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_message = "One or more errors occurred updating instance, see nested \"error_status_list\" and \"error_attr_list\" for more details."
                status_OUT.add_message( status_message )

            #-- END check to see if success. --#

            # store supporting information in status instance.
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, was_instance_updated )
            status_OUT.set_detail_value( self.PROP_UPDATED_ATTR_LIST, updated_attr_list )
            status_OUT.set_detail_value( self.PROP_NO_CHANGE_ATTR_LIST, no_change_attr_list )
            status_OUT.set_detail_value( self.PROP_ERROR_ATTR_LIST, error_attr_list )
            status_OUT.set_detail_value( self.PROP_SUCCESS_STATUS_LIST, success_status_list )
            status_OUT.set_detail_value( self.PROP_ERROR_STATUS_LIST, error_status_list )

        else:

            # no instance passed in - log error, return error status.
            status_message = "ERROR - No instance passed in to update. Can't do anything."
            self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
            self.add_status_message( status_message )

            # status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

        #-- END check to see if instance is not None --#

        return status_OUT

    #-- END method update_instance_from_record() --#


#-- END class ETLFromDictionary --#
