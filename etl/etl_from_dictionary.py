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
import json
import logging
import sys
import time
import traceback

# django imports
from django.db import DataError

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

    # properties in a record - moved up to ETLProcessor
    #RECORD_PROP_NAME_LIST_VALUE = "list_value"


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


    def process_related(
        self,
        related_to_instance_IN,
        record_IN,
        related_key_to_spec_map_IN,
        save_on_success_IN = True
    ):

        '''
        Accepts the instance currently being processed, the current record being
            processed, and a mapping of the keys in that record containing
            related data to each attribute's related spec.

        For each key:
        - retrieves information on how to process the contents related to that
            key in the record (could be a JSON object, could be a list of JSON
            objects, etc.)
        - based on the details for the key, do the right thing. This could
            mean:
            - calling run_etl() on an instance of a specified class, passing
            it the contents of the JSON record for a given key.
            - passing the record to a method on the current instance, for
            special processing.
            - etc.
        '''

        # return reference
        status_OUT = None

        #----------------------------------------------------------------------#
        # ==> declare variables

        me = "process_related"
        my_debug_flag = None
        status_message = None
        my_etl_spec = None
        related_to_instance = None
        extract_record = None
        current_key = None
        current_attr_spec = None
        current_attr_value = None

        # declare variables - processing value
        related_record_list = None

        # declare variables - related child objects
        related_attr_to_spec_map = None
        related_class = None
        related_fk_id_attr_name = None
        related_processing_method_name = None
        related_method_pointer = None
        related_status = None

        # declare variables - status checking
        was_instance_updated = None
        is_ok_to_process = None
        error_status_list = None

        #----------------------------------------------------------------------#
        # ==> do work

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        my_etl_spec = self.get_etl_entity()
        related_to_instance = related_to_instance_IN
        extract_record = record_IN
        related_record_list = None
        related_attr_to_spec_map = related_key_to_spec_map_IN

        # store supporting information in status instance.
        status_OUT = self.init_status( status_OUT )

        # got an instance?
        if ( related_to_instance is not None ):

            # do we have a record?
            if ( extract_record is not None ):

                # and, do we have related?
                if ( ( related_attr_to_spec_map is not None ) and ( len( related_attr_to_spec_map ) > 0 ) ):

                    # got everything we need. do work!

                    # loop over keys that map to related objects, pulling in
                    #     both the keys and the attr spec for that key.
                    for current_key, current_attr_spec in related_attr_to_spec_map.items():

                        if ( my_debug_flag == True ):
                            status_message = "Processing related key \"{related_key}\"\n\n==> spec: {related_spec}\n\n==> record: {record}".format(
                                related_key = current_key,
                                related_spec = json.dumps( current_attr_spec.to_json(), indent = 4, sort_keys = True ),
                                record = json.dumps( extract_record, indent = 4, sort_keys = True ),
                            )
                            self.output_debug( status_message, method_IN = me, indent_with_IN = "\n====> ", do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                        # get information on related object.
                        related_status = None
                        is_ok_to_process = True
                        related_class = current_attr_spec.get_related_model_class()
                        related_processing_method_name = current_attr_spec.get_load_attr_related_model_method_name()

                        # create related record list.
                        try:

                            related_record_list = self.process_related_build_record_list(
                                related_to_instance,
                                extract_record,
                                current_attr_spec
                            )

                        except ETLError as ee:

                            # well, there was an error. Not OK to proceed.
                            is_ok_to_process = False

                            #... and what else should we do here? Raise on up?
                            #raise ee
                            status_OUT = self.process_attr_error( status_OUT, current_attr_spec, str( ee ) )

                        #-- END try...except around building related record list. --#

                        # get value for key from record.
                        current_attr_value = extract_record.get( current_key )

                        # is there a related class?
                        if ( related_class is not None ):

                            # got a related record list?
                            if ( ( related_record_list is not None ) and ( len( related_record_list ) > 0 ) ):

                                # OK to process?
                                if ( is_ok_to_process == True ):

                                    # call method
                                    related_status = self.process_related_call_method(
                                        related_to_instance,
                                        related_record_list,
                                        current_attr_spec
                                    )

                                    # regardless of call, check and process status of result.
                                    status_OUT = self.process_result_status(
                                        status_OUT,
                                        related_status,
                                        self.PROP_WAS_INSTANCE_UPDATED,
                                        details_IN = current_attr_spec
                                    )

                                #-- END check to see if OK to process. --#

                            else:

                                # error - no related record list...? Nothing to process.
                                status_message = "ERROR - No related record list? ( value = {current_value} ) for related type attribute ( {attr_spec} ). Nothing to process.".format(
                                    current_value = current_attr_value,
                                    attr_spec = current_attr_spec.to_json()
                                )
                                self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                                # process error
                                status_OUT = self.process_attr_error( status_OUT, current_attr_spec, status_message )

                            #-- END check if we have a value --#

                        else:

                            # error - no related class...? Nothing to process.
                            status_message = "ERROR - No related class in related type attribute ( {attr_spec} ). Nothing to process.".format(
                                attr_spec = current_attr_spec.to_json()
                            )
                            self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                            # process error
                            status_OUT = self.process_attr_error( status_OUT, current_attr_spec, status_message )

                        #-- END check if we have a related class --#

                    #-- END loop over attributes that map to related objects --#

                    # status - success?
                    error_status_list = status_OUT.get_detail_value( self.PROP_ERROR_STATUS_LIST, None )
                    if ( len( error_status_list ) == 0 ):

                        # success!
                        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                        status_message = "Success!"
                        status_OUT.add_message( status_message )

                        # All processed. Save?
                        was_instance_updated = status_OUT.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                        if ( ( was_instance_updated == True )
                            and ( save_on_success_IN == True ) ):

                            # changed, and we are saving...
                            related_to_instance.save()

                        #-- END check to see if we save(). --#

                        # TODO: related_to_instance.update_from_record_post_related()?

                    else:

                        # not success!
                        status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                        status_message = "One or more errors occurred updating instance, see nested \"error_status_list\" and \"error_attr_list\" for more details."
                        status_OUT.add_message( status_message )

                    #-- END check to see if success. --#

                else:

                    # no related_attr_to_spec_map. Not necessarily an error, but
                    #     nothing to do...
                    status_message = "WARNING - No related attributes passed in. Can't do anything."
                    self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.WARNING, do_print_OUT = my_debug_flag )
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


    def process_related_build_record_list(
        self,
        related_to_instance_IN,
        record_IN,
        attr_spec_IN
    ):

        '''
        Accepts the instance currently being processed, the current record being
            processed, and information on the particular attribute being
            processed.

        Based on the type of the related information, builds a list of the
            records that need to be processed as related instances for this
            attribute.

        Returns the list, or None if error. If big error, raises ETLError.
        '''

        # return reference
        record_list_OUT = None

        #----------------------------------------------------------------------#
        # ==> declare variables

        me = "process_related_build_record_list"
        my_debug_flag = None
        status_message = None
        my_etl_spec = None
        related_to_instance = None
        extract_record = None
        extract_record_output = None
        related_attr_spec = None
        related_attr_spec_output = None
        param_summary = None
        related_attr_key = None
        related_attr_value = None
        attr_value_type = None
        related_record_list = None

        # declare variables - processing value
        list_value = None
        current_related_record = None
        related_to_instance_id = None

        # declare variables - related child objects
        related_data_type = None # object, list, ...?
        related_type = None
        related_fk_attr_name = None
        related_fk_id_attr_name = None

        #----------------------------------------------------------------------#
        # ==> do work

        # init
        record_list_OUT = list()
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        my_etl_spec = self.get_etl_entity()
        related_to_instance = related_to_instance_IN

        # init - extract_record
        extract_record = record_IN
        if ( extract_record is not None ):
            extract_record_output = json.dumps( extract_record, indent = 4, sort_keys = True )
        else:
            extract_record_output = extract_record
        #-- END see if we can convert extract_record to JSON string. --#

        # init - related_attr_spec
        related_attr_spec = attr_spec_IN
        if ( related_attr_spec is not None ):
            related_attr_spec_output = json.dumps( related_attr_spec.to_json(), indent = 4, sort_keys = True )
        else:
            related_attr_spec_output = related_attr_spec
        #-- END see if we can convert related_attr_spec to JSON string. --#

        param_summary = "param summary\n\n- related_to_instance_IN: {instance}\n\n- record_IN:\n{record}\n\n- ==> attr_spec_IN:\n{related_spec}".format(
            instance = related_to_instance,
            record = extract_record_output,
            related_spec = related_attr_spec_output
        )

        # got an instance?
        if ( related_to_instance is not None ):

            # do we have a record?
            if ( extract_record is not None ):

                # and, do we have spec?
                if ( related_attr_spec is not None ):

                    # got everything we need. do work!

                    # get information on related object.
                    related_attr_key = related_attr_spec.get_extract_name()
                    related_data_type = related_attr_spec.get_load_attr_related_model_data_type()
                    related_fk_attr_name = related_attr_spec.get_load_attr_related_model_fk_attr_name()

                    # get value for key from record.
                    related_attr_value = extract_record.get( related_attr_key )

                    # got a value?
                    if ( related_attr_value is not None ):

                        # the value has something in it. What type of
                        #    thing are we processing?:
                        # - single item (JSON object - dictionary)
                        # - list of items (JSON list - list)
                        # and, does it match with the declared data type?
                        attr_value_type = type( related_attr_value )
                        related_type = ETLAttribute.RELATED_TYPE_VALUE_TO_TYPE_MAP.get( related_data_type, None )

                        if ( my_debug_flag == True ):
                            status_message = "Related type for type value \"{my_type_value}\" = {type_type} ( value: {attr_value} )".format(
                                my_type_value = related_data_type,
                                type_type = related_type,
                                attr_value = related_attr_value
                            )
                            self.output_debug( status_message, method_IN = me, indent_with_IN = "\n--------> ", do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                        # is value instance of related_type?
                        if ( isinstance( related_attr_value, related_type ) == True ):

                            # type is as expected. What is the type?
                            if ( related_data_type == ETLAttribute.RELATED_TYPE_DICT ):

                                # dictionary - add single item to record
                                #     list.
                                related_record_list = list()
                                related_record_list.append( related_attr_value )

                            elif ( ( related_data_type == ETLAttribute.RELATED_TYPE_LIST )
                                or ( related_data_type == ETLAttribute.RELATED_TYPE_LIST_OF_DICTS ) ):

                                # list of dictionaries - use it as related_record_list.
                                related_record_list = related_attr_value

                            elif ( related_data_type == ETLAttribute.RELATED_TYPE_LIST_OF_VALUES ):

                                # list of values. For each, make
                                #     dictionary and store the value
                                #     inside, with name "list_value".
                                related_record_list = list()
                                for list_value in related_attr_value:

                                    # make dictionary
                                    current_related_record = dict()

                                    # store value in dictionary.
                                    current_related_record[ self.RECORD_PROP_NAME_LIST_VALUE ] = list_value

                                    # add record to record list
                                    related_record_list.append( current_related_record )

                                #-- END loop over values in list. --#

                            else:

                                # error - unknown type.
                                related_record_list = None
                                status_message = "Unexpected ERROR - Unknown related record data type \"{related_record_type}\", skipping related item {attr_value}, attr spec: {attr_spec}.".format(
                                    related_record_type = related_data_type,
                                    attr_value = related_attr_value,
                                    attr_spec = related_attr_spec.to_json()
                                )

                                # raise exception
                                raise ETLError( status_message )

                            #-- END check to see type --#

                            # do we have a record list?
                            if ( related_record_list is not None ):

                                # we do. Do we have an FK name?
                                if ( ( related_fk_attr_name is not None ) and ( related_fk_attr_name != "" ) ):

                                    # we have FK name. Derive ID name...
                                    related_fk_id_attr_name = "{}_id".format( related_fk_attr_name )

                                    #  - add a property
                                    #     to each record named this set
                                    #     to the current instance's ID.
                                    for current_related_record in related_record_list:

                                        # sanity check - is fk field there now?
                                        if ( ( related_fk_id_attr_name in current_related_record ) == False ):

                                            # Add foreign key ID field.
                                            related_to_instance_id = related_to_instance.id
                                            current_related_record[ related_fk_id_attr_name ] = related_to_instance_id

                                        else:

                                            # error - FK field already present?
                                            status_message = "foreign key ID field \"{field_name}\" already in related record data. Skipping related item {related_data}, attr spec: {attr_spec}.".format(
                                                field_name = related_fk_id_attr_name,
                                                related_data = current_related_record,
                                                attr_spec = related_attr_spec.to_json()
                                            )

                                            # raise exception
                                            raise ETLError( status_message )

                                        #-- END check to see if fk field already in related data record. --#

                                    #-- END loop over related data records. --#

                                else:

                                    # error - no foreign key attribute
                                    #     name. Where do I store FK?
                                    status_message = "no foreign key field specified in attr spec: {attr_spec}.".format(
                                        attr_spec = related_attr_spec.to_json()
                                    )

                                    # raise exception
                                    raise ETLError( status_message )

                                #-- END check to see if attr name to store FK --#

                            else:

                                # error - no record list. Something went
                                #     wrong...
                                status_message = "ERROR - no foreign key field specified in attr spec: {attr_spec}.".format(
                                    attr_spec = related_attr_spec.to_json()
                                )
                                self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                                # raise exception
                                raise ETLError( status_message )

                            #-- END check if record list. --#

                        else:

                            # type of value doesn't match specification.
                            status_message = "ERROR - Type of value ( value = {current_value}: {value_type} ) does not match type in spec ( {data_type} - spec: {attr_spec} ). Nothing to process.".format(
                                current_value = related_attr_value,
                                value_type = attr_value_type,
                                data_type = related_data_type,
                                attr_spec = related_attr_spec.to_json()
                            )
                            self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                            # raise exception
                            raise ETLError( status_message )

                        #-- END check to see if value is the right type. --#

                    else:

                        # error - no value...? Nothing to process.
                        status_message = "ERROR - No value passed ( value = {current_value} ) for related type attribute ( {attr_spec} ). Nothing to process.".format(
                            current_value = related_attr_value,
                            attr_spec = related_attr_spec.to_json()
                        )
                        self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                        # raise exception
                        raise ETLError( status_message )

                    #-- END check if we have a value --#

                else:

                    # no related_attr_spec. Error.
                    status_message = "WARNING - No attribute specification passed in. Can't build related record list. {param_summary}".format(
                        param_summary = param_summary
                    )
                    self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.WARNING, do_print_OUT = my_debug_flag )
                    self.add_status_message( status_message )

                    # raise exception
                    raise ETLError( status_message )

                #-- END check to see if attribute spec. --#

            else:

                # no record passed in - log error, return error status.
                status_message = "ERROR - No record passed in to update. Can't build related record list. {param_summary}".format(
                    param_summary = param_summary
                )
                self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
                self.add_status_message( status_message )

                # raise exception
                raise ETLError( status_message )

            #-- END check to see if instance is not None --#

        else:

            # no instance passed in - log error, raise exception.
            status_message = "ERROR - No instance passed in to update. Can't build related record list. {param_summary}".format(
                param_summary = param_summary
            )
            self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
            self.add_status_message( status_message )

            # raise exception
            raise ETLError( status_message )

        #-- END check to see if instance is not None --#

        # return the list
        record_list_OUT = related_record_list

        return record_list_OUT

    #-- END method process_related_build_record_list() --#


    def process_related_call_method(
        self,
        related_to_instance_IN,
        related_record_list_IN,
        related_attr_spec_IN
    ):

        '''
        Accepts the instance currently being processed, the current record being
            processed, and a mapping of the keys in that record containing
            related data to each attribute's related spec.

        For each key:
        - retrieves information on how to process the contents related to that
            key in the record (could be a JSON object, could be a list of JSON
            objects, etc.)
        - based on the details for the key, do the right thing. This could
            mean:
            - calling run_etl() on an instance of a specified class, passing
            it the contents of the JSON record for a given key.
            - passing the record to a method on the current instance, for
            special processing.
            - etc.
        '''

        # return reference
        status_OUT = None

        #----------------------------------------------------------------------#
        # ==> declare variables

        me = "process_related_call_method"
        my_debug_flag = None
        status_message = None
        related_to_instance = None
        related_record_list = None
        related_attr_spec = None

        # declare variables - related child objects
        related_class = None
        related_processing_method_name = None
        related_method_pointer = None

        # declare variables - status checking
        was_instance_updated = None

        #----------------------------------------------------------------------#
        # ==> do work

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        my_debug_flag = self.debug_flag
        #my_debug_flag = True
        related_to_instance = related_to_instance_IN
        related_record_list = related_record_list_IN
        related_attr_spec = related_attr_spec_IN

        # got an instance?
        if ( related_to_instance is not None ):

            # do we have a record list?
            if ( ( related_record_list is not None ) and ( len( related_record_list ) > 0 ) ):

                # and, do we have a spec?
                if ( related_attr_spec is not None ):

                    # got everything we need. do work!

                    # get information on related object.
                    related_class = related_attr_spec.get_related_model_class()
                    related_processing_method_name = related_attr_spec.get_load_attr_related_model_method_name()

                    # is there a related class?
                    if ( related_class is not None ):

                        # got a related record list?
                        if ( ( related_record_list is not None ) and ( len( related_record_list ) > 0 ) ):

                            # what method do we call to process?

                            # is there a processing method name?
                            if ( ( related_processing_method_name is not None )
                                and ( related_processing_method_name != "" ) ):

                                # check if class has method
                                # - https://stackoverflow.com/questions/25295327/how-to-check-if-a-python-class-has-particular-method-or-not
                                if ( hasattr( related_class, related_processing_method_name ) == True ):

                                    # If so, call it as class method - https://stackoverflow.com/questions/3521715/call-a-python-method-by-name
                                    related_method_pointer = getattr( related_class, related_processing_method_name )
                                    status_OUT = related_method_pointer(
                                        related_to_instance,
                                        related_record_list,
                                        related_attr_spec,
                                        debug_flag_IN = my_debug_flag
                                    )

                                else:

                                    # error - requested method does not exist.
                                    status_message = "ERROR - related processing method \"{method_name}\" does not exist in related class \"{related_class}\" ( attr spec: {attr_spec} ).".format(
                                        method_name = related_processing_method_name,
                                        related_class = related_class,
                                        attr_spec = json.dumps( related_attr_spec.to_json(), indent = 4, sort_keys = True )
                                    )
                                    self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                                    # make status
                                    status_OUT = StatusContainer()
                                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                                    status_OUTv.add_message( status_message )

                                    # Exception - spec is broken.
                                    raise ETLError( status_message )

                                #-- END check to make sure method exists.

                            else:

                                # If not, call classmethod run_etl().
                                status_OUT = related_class.run_etl( related_record_list )

                            #-- END check which method we call --#

                        else:

                            # error - no related record list...? Nothing to process.
                            status_message = "ERROR - No related record list for related type attribute ( {attr_spec} ). Nothing to process.".format(
                                attr_spec = json.dumps( related_attr_spec.to_json(), indent = 4, sort_keys = True )
                            )
                            self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                            # error status
                            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                            status_OUT.add_message( status_message )

                        #-- END check if we have a value --#

                    else:

                        # error - no related class...? Nothing to process.
                        status_message = "ERROR - No related class in related type attribute ( {attr_spec} ). Nothing to process.".format(
                            attr_spec = related_attr_spec.to_json()
                        )
                        self.output_log_message( status_message, method_IN = me, indent_with_IN = "\n--------> ", log_level_code_IN = logging.ERROR, do_print_IN = my_debug_flag )

                        # error status
                        status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                        status_OUT.add_message( status_message )

                    #-- END check if we have a related class --#

                else:

                    # no related_attr_spec. ERROR.
                    status_message = "ERROR - No related attribute spec passed in. Can't do anything."
                    self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.WARNING, do_print_OUT = my_debug_flag )
                    self.add_status_message( status_message )

                    # error status
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                    status_OUT.add_message( status_message )

                #-- END check to see if attribute spec. --#

            else:

                # no record passed in - log error, return error status.
                status_message = "ERROR - No related record list passed in to update. Can't do anything."
                self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
                self.add_status_message( status_message )

                # error status
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_OUT.add_message( status_message )

            #-- END check to see if instance is not None --#

        else:

            # no instance passed in - log error, return error status.
            status_message = "ERROR - No instance passed in to update. Can't do anything."
            self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )
            self.add_status_message( status_message )

            # error status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )

        #-- END check to see if instance is not None --#

        return status_OUT

    #-- END method process_related_call_method() --#


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
        related_class_module = None
        related_class_name = None
        related_attr_to_spec_map = None
        related_status = None
        related_success = None
        were_related_updated = None

        # declare variables - status checking
        was_attr_updated = None
        was_instance_updated = None
        error_status_list = None

        # declare variables - debug
        json_string = None

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

        if ( my_debug_flag == True ):
            json_string = json.dumps( current_record, indent = 4, sort_keys = True )
            status_message = "current record JSON string:\n{json_string}".format(
                json_string = json_string
            )
            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
        #-- END DEBUG --#

        # store supporting information in status instance.
        status_OUT = self.init_status( status_OUT )

        # got an instance?
        if ( current_entry_instance is not None ):

            # init
            was_instance_updated = False
            related_class = None
            related_class_module = None
            related_class_name = None
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
            # ==> process record attributes (loop over names in dictionary)

            # loop over keys/names in current record to get values for
            #     each and store in instance.
            for current_key, current_value in current_record.items():

                #--------------------------------------------------------------#
                # ==> get attribute spec, name and value

                # start with attribute value set to column value
                current_attr_value = current_value

                # retrieve ETLAttribute for this index.
                my_etl_attribute = my_etl_spec.pull_attr_for_key( current_key )

                # TODO: deal with value being JSON that needs to be handed off to a child model.

                # got an attribute spec?
                if ( my_etl_attribute is not None ):

                    # ETLAttribute found.  Retrieve values and do
                    #     processing.

                    # is there a related class or related class name?
                    related_class = my_etl_attribute.get_related_model_class()
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

                #--------------------------------------------------------------#
                # ==> store attribute.

                # do we have an attribute name?
                if ( ( current_attr_name is not None ) and ( current_attr_name != "" ) ):

                    # store the value.
                    store_status = self.store_attribute( current_entry_instance, current_attr_name, current_attr_value )

                    # process status
                    store_update_details = store_status.get_detail_value( self.PROP_ATTR_UPDATE_DETAIL )
                    status_OUT = self.process_result_status(
                        status_OUT,
                        store_status,
                        self.PROP_WAS_ATTR_UPDATED,
                        details_IN = store_update_details
                    )

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

            if ( my_debug_flag == True ):
                status_message = "pre-save hook status ( changed: {changed} ): {status} ".format(
                    status = pre_save_custom_update_status,
                    changed = pre_save_custom_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED )
                )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

            # process status
            status_OUT = self.process_result_status(
                status_OUT,
                pre_save_custom_update_status,
                self.PROP_WAS_INSTANCE_UPDATED,
                details_IN = None
            )

            if ( my_debug_flag == True ):
                status_message = "OVERALL status ( changed: {changed} ): {status} ".format(
                    status = pre_save_custom_update_status,
                    changed = pre_save_custom_update_status.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED )
                )
                self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
            #-- END DEBUG --#

            #------------------------------------------------------------------#
            # ==> success thus far?

            # status - success?
            error_status_list = status_OUT.get_detail_value( self.PROP_ERROR_STATUS_LIST, None )
            if ( len( error_status_list ) == 0 ):

                # success!
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                status_message = "Success!"
                status_OUT.add_message( status_message )

                #--------------------------------------------------------------#
                # ==> save()?

                # All processed. Save?
                was_instance_updated = status_OUT.get_detail_value( self.PROP_WAS_INSTANCE_UPDATED, None )
                if ( ( was_instance_updated == True )
                    and ( save_on_success_IN == True ) ):

                    # changed, and we are saving...
                    try:

                        if ( my_debug_flag == True ):
                            status_message = "attempting save(): {}".format( current_entry_instance )
                            self.output_debug( status_message, method_IN = me, do_print_IN = my_debug_flag )
                        #-- END DEBUG --#

                        current_entry_instance.save()

                    except DataError as de:

                        # log the JSON for the current record...
                        status_message = "DataError caught save()-ing instance (probably type mismatch). Record:\n{record_json_string}".format(
                            record_json_string = json.dumps( current_record, indent = 4, sort_keys = True )
                        )
                        self.output_log_message(
                            status_message,
                            method_IN = me,
                            log_level_code_IN = logging.ERROR,
                            do_print_IN = True
                        )

                        # ...then raise the exception again.
                        raise de

                    #-- END try...except --#

                    # catching specific excpetions here as they arise. List:
                    # https://docs.djangoproject.com/en/3.2/ref/exceptions/#database-exceptions

                #-- END check to see if we save(). --#

                #--------------------------------------------------------------#
                # ==> post-save hook

                # call current_entry_instance.update_from_record_post_save(),
                #     which can be overridden in a particular class to do
                #     fancier processing for related records.
                post_save_custom_update_status = current_entry_instance.update_from_record_post_save( current_record )

                # process status
                status_OUT = self.process_result_status(
                    status_OUT,
                    post_save_custom_update_status,
                    self.PROP_WAS_INSTANCE_UPDATED,
                    details_IN = None
                )

                #--------------------------------------------------------------#
                # ==> related instances.

                # any related to process?
                if ( ( related_attr_to_spec_map is not None ) and ( len( related_attr_to_spec_map ) > 0 ) ):

                    # call process_related() method.
                    related_status = self.process_related(
                        current_entry_instance,
                        current_record,
                        related_attr_to_spec_map,
                        save_on_success_IN = save_on_success_IN
                    )

                    # process status
                    status_OUT = self.process_result_status(
                        status_OUT,
                        related_status,
                        self.PROP_WAS_INSTANCE_UPDATED,
                        details_IN = None
                    )

                #-- END check if related. --#

                # TODO - post-related hook?

            else:

                # not success!
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_message = "One or more errors occurred updating instance, see nested \"error_status_list\" and \"error_attr_list\" for more details."
                status_OUT.add_message( status_message )

            #-- END check to see if success. --#

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
