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


    def process_related( self, instance_IN, record_IN, related_key_to_spec_map_IN ):

        # return reference
        status_OUT = None

        #----------------------------------------------------------------------#
        # ==> declare variables

        me = "process_related"
        my_debug_flag = None
        status_message = None
        my_etl_spec = None
        current_entry_instance = None
        current_record = None
        current_key = None
        current_attr_spec = None
        current_value = None
        current_attr_name = None
        current_attr_value = None
        attr_value_type = None
        my_etl_attribute = None

        # declare variables - processing value
        record_list = None
        store_status = None
        store_update_details = None
        store_success = None

        # declare variables - related child objects
        related_attr_to_spec_map = None
        related_class = None
        related_data_type = None # object, list, ...?
        related_type = None
        related_fk_attr_name = None
        #related_processing_method_name = None
        related_status = None

        # declare variables - status checking
        was_attr_updated = None
        was_instance_updated = None
        updated_attr_list = None
        no_change_attr_list = None
        error_attr_list = None
        success_status_list = None
        error_status_list = None

        #----------------------------------------------------------------------#
        # ==> do work

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_debug_flag = self.debug_flag
        my_etl_spec = self.get_etl_entity()
        current_entry_instance = instance_IN
        current_record = record_IN
        record_list = None
        related_attr_to_spec_map = related_key_to_spec_map_IN

        # init status checking variables
        was_instance_updated = False
        updated_attr_list = []
        no_change_attr_list = []
        error_attr_list = []
        success_status_list = []
        error_status_list = []

        # got an instance?
        if ( current_entry_instance is not None ):

            # do we have a record?
            if ( current_record is not None ):

                # and, do we have related?
                if ( ( related_attr_to_spec_map is not None ) and ( len( related_attr_to_spec_map ) > 0 ) ):

                    # got everything we need. do work!

                    # loop over keys that map to related objects, pulling in
                    #     both the keys and the attr spec for that key.
                    for current_key, current_attr_spec in related_attr_to_spec_map.items():

                        # get information on related object.
                        related_class = my_etl_attribute.get_load_attr_related_model_class()
                        related_data_type = my_etl_attribute.get_load_attr_related_model_data_type()
                        related_fk_attr_name = my_etl_attribute.get_load_attr_related_model_fk_attr_name()
                        related_processing_method_name = my_etl_attribute.get_load_attr_related_model_method_name()

                        # get value for key from record.
                        current_attr_value = current_record.get( current_key )

                        # is there a related class?
                        if ( related_class is not None ):

                            # got a value?
                            if ( current_attr_value is not None ):

                                # the value has something in it. What type of
                                #    thing are we processing?:
                                # - single item (JSON object - dictionary)
                                # - list of items (JSON list - list)
                                # and, does it match with the declared data type?
                                attr_value_type = type( current_attr_value )
                                related_type = ETLAttribute.RELATED_TYPE_VALUE_TO_TYPE_MAP.get( related_data_type, None )

                                # is value instance of related_type?
                                if ( isinstance( current_attr_value, related_type ) == True ):

                                    # type is as expected. What is the type?
                                    if ( related_data_type == ETLAttribute.RELATED_TYPE_DICT ):

                                        # dictionary - add single item to record
                                        #     list.
                                        record_list = list()
                                        record_list.append( current_attr_value )

                                    elif ( related_data_type == ETLAttribute.RELATED_TYPE_LIST ):

                                        # list - use it as record_list.
                                        record_list = current_attr_value

                                    else:

                                        # TODO - error - unknown type.
                                        record_list = None

                                    #-- END check to see type --#

                                    # do we have a record list?
                                    if ( record_list is not None ):

                                        # we do. Do we have an FK name?
                                        if ( ( related_fk_attr_name is not None ) and ( related_fk_attr_name != "" ) ):

                                            # we have FK name - add a property
                                            #     to each record named this set
                                            #     to the current instance.
                                            # TODO - set FK value
                                            pass

                                        else:

                                            # error - no foreign key attribute
                                            #     name. Where do I store FK?
                                            # TODO - error.
                                            pass

                                        #-- END check to see if attr name to store FK --#

                                        # TODO - OK to process?
                                        # TODO - is there a processing method name?
                                        # TODO - If so, call it as class method - https://stackoverflow.com/questions/3521715/call-a-python-method-by-name
                                        # TODO - If not, call classmethod run_etl().
                                        # TODO - regardless of call, check and process status of result.

                                    else:

                                        # error - no record list. Something went
                                        #     wrong...
                                        # TODO - error
                                        pass

                                    #-- END check if record list. --#

                                else:

                                    # type of value doesn't match specification.
                                    #     TODO - Error.
                                    pass

                                #-- END check to see if value is the right type. --#

                            else:

                                # error - no value...? Nothing to process.
                                #     TODO - Error.
                                pass

                            #-- END check if we have a value --#

                        else:

                            # error - no related class...? Nothing to process.
                            #     TODO - Error.
                            pass

                        #-- END check if we have a related class --#

                    #-- END loop over attributes that map to related objects --#

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

                        # TODO: current_entry_instance.update_from_record_post_related()?

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

                    # no related_attr_to_spec_map. Not necessarily an error, but
                    #     nothing to do...
                    status_message = "WARNING - No related attributes passed in. Can't do anything."
                    self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.WARNING )
                    self.add_status_message( status_message )

                    # status
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_WARNING )
                    status_OUT.add_message( status_message )
                    status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

                #-- END check to see if attribute spec. --#

            else:

                # no record passed in - log error, return error status.
                status_message = "ERROR - No record passed in to update. Can't do anything."
                self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
                self.add_status_message( status_message )

                # status
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_OUT.add_message( status_message )
                status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

            #-- END check to see if instance is not None --#

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

    #-- END method process_related() --#


    def update_instance_from_record( self, instance_IN, record_IN, save_on_success_IN = True ):

        # return reference
        status_OUT = None

        #----------------------------------------------------------------------#
        # ==> declare variables

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
        pre_save_custom_update_status = None
        pre_save_custom_update_success = None
        was_updated_pre_save = None
        post_save_custom_update_status = None
        post_save_custom_update_success = None
        was_updated_post_save = None

        # declare variables - related child objects
        related_class = None
        related_attr_to_spec_map = None
        related_status = None
        related_success = None
        were_related_updated = None

        # declare variables - status checking
        was_attr_updated = None
        was_instance_updated = None
        updated_attr_list = None
        no_change_attr_list = None
        error_attr_list = None
        success_status_list = None
        error_status_list = None

        #----------------------------------------------------------------------#
        # ==> do work

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_debug_flag = self.debug_flag
        my_etl_spec = self.get_etl_entity()
        current_entry_instance = instance_IN
        current_record = record_IN
        related_attr_to_spec_map = dict()

        # init status checking variables
        was_instance_updated = False
        updated_attr_list = []
        no_change_attr_list = []
        error_attr_list = []
        success_status_list = []
        error_status_list = []

        # got an instance?
        if ( current_entry_instance is not None ):

            # init
            was_instance_updated = False
            related_class = None
            store_status = None
            store_success = False
            pre_save_custom_update_status = None
            pre_save_custom_update_success = False
            was_updated_pre_save = False
            post_save_custom_update_status = None
            post_save_custom_update_success = False
            was_updated_post_save = False
            related_status = None
            related_success = False
            were_related_updated = False

            #------------------------------------------------------------------#
            # ==> process record attributes (loop)

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

                    # is there a related class?
                    related_class = my_etl_attribute.get_load_attr_related_model_class()
                    if ( related_class is not None ):

                        # related class! Add attribute name to list for
                        #     processing at end, after save.
                        related_attr_to_spec_map[ current_key ] = my_etl_attribute

                        # no current attr name, so we skip processing this field
                        #     until later.
                        #current_attr_name = None

                        # if we want to store the contents of this attribute in
                        #    extra data, just in case, then set attribute name
                        #    here to current_key
                        current_attr_name = current_key

                    else:

                        # no related class, process attribute.
                        current_attr_name = my_etl_attribute.get_load_attr_name()

                        # process value.
                        current_attr_value = self.process_value( current_attr_value, my_etl_attribute, current_entry_instance )

                    #-- END check to see if related class. --#

                else:

                    # no ETLAttribute instance. Direct, untranslated
                    #     load to instance.
                    current_attr_name = current_key

                #-- END check to see if attribute spec. --#

                # do we have an attribute name?
                if ( ( current_attr_name is not None ) and ( current_attr_name != "" ) ):

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

                else:

                    # no attribute name, if not related, then error.
                    if ( related_class is None ):

                        # TODO - error
                        # No related class, and no attribute name - error.
                        pass

                    #-- END check to see if related class present... --#

                #-- END check to see if attribute name to update. --#

            #-- END loop values in record --#

            #------------------------------------------------------------------#
            # ==> pre-save hook

            # call current_entry_instance.update_from_record_pre_save(),
            #     which can be overridden in a particular class to do
            #     fancier processing than specification can hold.
            pre_save_custom_update_status = current_entry_instance.update_from_record_pre_save( current_record )

            # success?
            pre_save_custom_update_success = pre_save_custom_update_status.is_success()
            if ( pre_save_custom_update_success == True ):

                # success.
                success_status_list.append( pre_save_custom_update_status )

                # was instance updated?
                was_updated_pre_save = pre_save_custom_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                if ( was_updated_pre_save == True ):

                    # updated.
                    was_instance_updated = True

                #-- END check to see if attribute updated. --#

            else:

                # error.
                error_status_list.append( pre_save_custom_update_status )

            #-- END check to see if pre-save update was a success --#

            #------------------------------------------------------------------#
            # ==> success thus far?

            # status - success?
            if ( len( error_status_list ) == 0 ):

                # success!
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                status_message = "Success!"
                status_OUT.add_message( status_message )

                #--------------------------------------------------------------#
                # ==> save()?

                # All processed. Save?
                if ( ( was_instance_updated == True )
                    and ( save_on_success_IN == True ) ):

                    # changed, and we are saving...
                    current_entry_instance.save()

                #-- END check to see if we save(). --#

                #--------------------------------------------------------------#
                # ==> post-save hook

                # call current_entry_instance.update_from_record_post_save(),
                #     which can be overridden in a particular class to do
                #     fancier processing for related records.
                post_save_custom_update_status = current_entry_instance.update_from_record_post_save( current_record )

                # success?
                post_save_custom_update_success = post_save_custom_update_status.is_success()
                if ( post_save_custom_update_success == True ):

                    # success.
                    success_status_list.append( post_save_custom_update_status )

                    # was instance updated?
                    was_updated_post_save = post_save_custom_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                    if ( was_updated_post_save == True ):

                        # updated.
                        was_instance_updated = True

                    #-- END check to see if attribute updated. --#

                else:

                    # error.
                    error_status_list.append( related_update_status )

                #-- END check to see if update was a success --#

                #--------------------------------------------------------------#
                # ==> related instances.

                # any related to process?
                if ( ( related_attr_to_spec_map is not None ) and ( len( related_attr_to_spec_map ) > 0 ) ):

                    # call process_related() method.
                    related_status = self.process_related(
                        current_entry_instance,
                        current_record,
                        related_attr_to_spec_map
                    )

                    # success?
                    related_success = related_status.is_success()
                    if ( related_success == True ):

                        # success.
                        success_status_list.append( related_status )

                        # was instance updated?
                        were_related_updated = related_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                        if ( were_related_updated == True ):

                            # updated.
                            was_instance_updated = True

                        #-- END check to see if attribute updated. --#

                    else:

                        # error.
                        error_status_list.append( related_status )

                    #-- END check to see if related processing was a success --#

                #-- END check if related. --#

                # TODO - post-related hook?

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
