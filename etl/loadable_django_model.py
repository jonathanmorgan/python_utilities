'''
This class is an example "LoadableDjangoModel" interface-esque from
python_utilities/etl/loadable_django_model.py. This means it includes:
- extra_data = models.JSONField( blank = True, null = True )
- etl_spec class variable
- class methods:

    - get_etl_spec
    - initialize_etl
    - run_etl
    - set_etl_spec

- instance methods:

    - update_extra_data_attr

Django models that are intended to have data loaded into them by the ETL
    Framework can either:
    - extend this model (if in a simple object hierarchy, or if you are comfortable with mixins)
    - make sure that all the above stuff is in the class, or a parent abstract class within your object hierarchy.
'''

# python built-ins
import json
import logging

# django imports
from django.db import models

# python_utilities
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer

# ETL imports
from python_utilities.etl.etl_attribute import ETLAttribute
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError
from python_utilities.etl.etl_from_dictionary import ETLFromDictionary
from python_utilities.etl.etl_from_excel_with_headers import ETLFromExcelWithHeaders
from python_utilities.etl.etl_object_loader import ETLObjectLoader
from python_utilities.etl.etl_processor import ETLProcessor

class LoadableDjangoModel( models.Model ):

    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================

    # logger name
    MY_LOGGER_NAME = "python_utilities.etl.LoadableDjangoModel"

    # properties in a record
    RECORD_PROP_NAME_LIST_VALUE = ETLProcessor.RECORD_PROP_NAME_LIST_VALUE  # "list_value"

    # StatusContainer properties
    PROP_WAS_INSTANCE_UPDATED = ETLObjectLoader.PROP_WAS_INSTANCE_UPDATED

    #==========================================================================#
    # ! ==> model fields
    #==========================================================================#

    # extra data - store in JSON Field.
    extra_data = models.JSONField( blank = True, null = True )

    #==========================================================================#
    # ! ==> meta class
    #==========================================================================#

    # Meta-data for this class.
    class Meta:

        abstract = True

    #-- END class Meta --#

    #==========================================================================#
    # ! ==> class variables
    #==========================================================================#

    etl_spec = None
    MY_LOGGER_NAME = "python_utilities.etl.LoadableDjangoModel"

    #==========================================================================#
    # ! ==> class methods
    #==========================================================================#


    @classmethod
    def get_etl_spec( cls ):

        # return reference
        value_OUT = None

        # declare variables
        my_etl_spec = None

        # retrieve value
        my_etl_spec = cls.etl_spec

        # initialized?
        if ( my_etl_spec is None ):

            # no. Init, then return.
            my_etl_spec = cls.initialize_etl()

        #-- END check to see if initialized --#

        value_OUT = my_etl_spec

        return value_OUT

    #-- END method get_etl_spec() --#


    @classmethod
    def get_my_etl_loader_instance( cls ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_my_etl_loader_instance"
        my_etl_spec = None
        extract_storage_type = None

        # retrieve ETL spec
        my_etl_spec = cls.get_etl_spec()

        # got one?
        if ( my_etl_spec is not None ):

            # got one, retrieve type.
            extract_storage_type = my_etl_spec.get_extract_storage_type()

            # got a type?
            if ( ( extract_storage_type is not None )
                and ( extract_storage_type != "" )
                and ( extract_storage_type in ETLEntity.VALID_STORAGE_TYPE_LIST ) ):

                # we do - which type?
                if ( ( extract_storage_type == ETLEntity.STORAGE_TYPE_DICT )
                    or ( extract_storage_type == ETLEntity.STORAGE_TYPE_JSON ) ):

                    # ETLFromDictionary
                    instance_OUT = ETLFromDictionary()

                elif ( extract_storage_type == ETLEntity.STORAGE_TYPE_XLSX_WITH_HEADERS ):

                    # ETLFromExcelWithHeaders
                    instance_OUT = ETLFromExcelWithHeaders()

                else:

                    # default for everything else is ETLFromDictionary.
                    instance_OUT = ETLFromDictionary()

            else:

                # no storage type. Default to dictionary.
                instance_OUT = ETLFromDictionary()

            #-- END check if we have an extract storage type. --#

        else:

            # no spec - error.
            raise ETLError( "In LoadableDjangoModel.{}(): no ETL spec, can't retrieve appropriate ETL class based on spec.".format( me ) )

        #-- END check to see if spec --#

        return instance_OUT

    #-- END method get_my_etl_loader_instance() --#


    @classmethod
    def initialize_etl( cls, *args, **kwargs ):

        # return reference
        spec_OUT = None

        # declare variables
        me = "initialize_etl"
        my_etl_spec = None

        # create ETL spec
        my_etl_spec = ETLEntity()

        # ID fields

        # attribute specs - renames, transformations, etc.

        # related

        # store it.
        cls.set_etl_spec( my_etl_spec )
        spec_OUT = my_etl_spec

        raise ETLError( "In abstract-ish method LoadableDjangoModel.{}(): OVERRIDE ME".format( me ) )

        return spec_OUT

    #-- END class method initialize_etl() --#


    @classmethod
    def initialize_etl_loader( cls, etl_loader_IN, debug_flag_IN = False, *args, **kwargs ):

        '''
        Can be extended by a child class to further initialize the ETL loader
            as needed, depending on the type of loader and other needs of the
            class. Defaults to doing nothing.
        '''

        # return reference
        etl_loader_OUT = None

        # declare variables
        me = "initialize_etl_loader"

        # by default, pass back what is passed in.
        etl_loader_OUT = etl_loader_IN

        return etl_loader_OUT

    #-- END class method initialize_etl_loader() --#


    @classmethod
    def run_etl( cls,
                 record_list_IN = None,
                 start_index_IN = None,
                 row_count_IN = None,
                 debug_flag_IN = False,
                 default_time_zone_IN = None,
                 do_output_progress_IN = False,
                 allow_empty_record_list_IN = False,
                 *args,
                 **kwargs ):

        '''
        preconditions:
        - time_zone_IN should be a pytz timezone instance.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "run_etl"
        status_message = None
        my_debug_flag = None
        my_etl_spec = None
        json_string = None

        # declare variables - processing
        etl_instance = None
        my_start_row = None
        my_row_count = None
        process_status = None
        process_success = None
        process_message_list = None
        error_counter = None
        record_counter = None
        success_counter = None
        update_counter = None


        # init
        my_debug_flag = debug_flag_IN
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have a record list?
        if ( ( ( record_list_IN is not None )
                and ( len( record_list_IN ) > 0 ) )
             or ( allow_empty_record_list_IN == True ) ):

            # first, make sure ETL spec is initialized.
            cls.initialize_etl()

            # retrieve spec
            my_etl_spec = cls.get_etl_spec()

            if ( my_debug_flag == True ):
                spec_json = my_etl_spec.to_json()
                json_string = json.dumps( spec_json, indent = 4, sort_keys = True )
                status_message = "In {my_class}.{my_method}(): ETL spec JSON: {json_string}".format(
                    my_class = cls,
                    my_method = me,
                    json_string = json_string
                )
                LoggingHelper.output_debug( status_message, do_print_IN = True )
            #-- END DEBUG --#

            # create ETL instance
            etl_instance = cls.get_my_etl_loader_instance()
            etl_instance.debug_flag = my_debug_flag
            etl_instance.set_etl_entity( my_etl_spec )

            # call method to further initialize ETLLoader.
            etl_instance = cls.initialize_etl_loader( etl_instance )

            # default time zone?
            if ( default_time_zone_IN is not None ):

                # set time zone in ETLProcessor descendant.
                etl_instance.set_default_time_zone( default_time_zone_IN )

            #-- END check if time zone passed in. --#

            # list of records passed in?
            if ( record_list_IN is not None ):

                # store list of records.
                etl_instance.set_record_list( record_list_IN )

            #-- END check if record list passed in --#

            # loop over rrecords, processing each
            status_message = "In {my_class} - Starting {my_method}!".format(
                my_class = cls,
                my_method = me
            )
            LoggingHelper.output_debug(
                status_message,
                indent_with_IN = "==> ",
                do_print_IN = my_debug_flag
            )
            my_start_row = start_index_IN
            my_row_count = row_count_IN
            process_status = etl_instance.process_records(
                start_index_IN = my_start_row,
                record_count_IN = my_row_count,
                do_output_progress_IN = do_output_progress_IN
            )

            # retrieve status counts...
            error_counter = process_status.get_detail_value( ETLProcessor.STATUS_PROP_UPDATE_ERROR_COUNT )
            record_counter = process_status.get_detail_value( ETLProcessor.STATUS_PROP_PROCESSED_RECORD_COUNT )
            success_counter = process_status.get_detail_value( ETLProcessor.STATUS_PROP_UPDATE_SUCCESS_COUNT )
            update_counter = process_status.get_detail_value( ETLProcessor.STATUS_PROP_UPDATED_RECORD_COUNT )

            # ...and use them to update the output status
            status_OUT.set_detail_value( ETLProcessor.STATUS_PROP_PROCESSED_RECORD_COUNT, record_counter )
            status_OUT.set_detail_value( ETLProcessor.STATUS_PROP_UPDATE_ERROR_COUNT, error_counter )
            status_OUT.set_detail_value( ETLProcessor.STATUS_PROP_UPDATE_SUCCESS_COUNT, success_counter )
            status_OUT.set_detail_value( ETLProcessor.STATUS_PROP_UPDATED_RECORD_COUNT, update_counter )

            # store process status info in return status
            status_OUT.add_status_container( process_status )
            process_message_list = process_status.get_message_list()
            status_OUT.add_messages_from_list( process_message_list )

            # error?
            process_success = process_status.is_success()
            if ( process_success == False ):

                # error
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )

            #-- END check to see if update was a success --#

        else:

            # no instance passed in - log error, return error status.
            status_message = "ERROR - No record list passed in. Can't do anything."
            LoggingHelper.log_message(
                status_message,
                method_IN = me,
                logger_name_IN = cls.MY_LOGGER_NAME,
                do_print_IN = True,
                log_level_code_IN = logging.WARNING
            )

            # status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )

        #-- END check to see if we actually do work. --#

        return status_OUT

    #-- END class method run_etl() --#


    @classmethod
    def set_etl_spec( cls, value_IN ):

        # return reference
        value_OUT = None

        cls.etl_spec = value_IN

        value_OUT = cls.get_etl_spec()

        return value_OUT

    #-- END method set_etl_spec() --#


    #==========================================================================#
    # ! ==> instance methods
    #==========================================================================#


    def get_extra_data_attr_value( self, attr_name_IN ):

        # return reference
        value_OUT = None

        # declare variables
        extra_data_json = None
        current_value = None

        # get extra data JSONField
        extra_data_json = self.extra_data

        # got anything already?
        if ( extra_data_json is not None ):

            # is name already in extra data?
            if ( attr_name_IN in extra_data_json ):

                # yes - retrieve current value
                value_OUT = extra_data_json.get( attr_name_IN, None )

            else:

                # no - return None.
                value_OUT = None

            #-- END check to see if name in JSON --#

        else:

            # no extra data, return None
            value_OUT = None

        #-- END check to see if initialized --#

        return value_OUT

    #-- END method get_extra_data_attr_value() --#


    def update_extra_data_attr( self, attr_name_IN, attr_value_IN ):

        # return reference
        is_changed_OUT = False

        # declare variables
        me = "update_extra_data_attr"
        extra_data_json = None
        current_value = None

        # get extra data JSONField
        extra_data_json = self.extra_data

        # got anything already?
        if ( ( extra_data_json is None ) or ( extra_data_json == "" ) ):

            # no - create dictionary.
            extra_data_json = dict()
            self.extra_data = extra_data_json

        #-- END check to see if initialized --#

        # is name already in extra data?
        if ( attr_name_IN in extra_data_json ):

            # retrieve current value
            current_value = extra_data_json.get( attr_name_IN )

            # is new same as existing?
            if ( current_value != attr_value_IN ):

                # not the same - update
                extra_data_json[ attr_name_IN ] = attr_value_IN
                is_changed_OUT = True

            else:

                # existing value for this key is same as new value. Not changed.
                is_changed_OUT = False

            #-- END check to see if value as changed for known atribute. --#

        else:

            # not already there - set the value for this attribute
            extra_data_json[ attr_name_IN ] = attr_value_IN
            is_changed_OUT = True

        #-- END check to see if name in JSON --#

        return is_changed_OUT

    #-- END method update_extra_data_attr() --#


    def update_from_record_pre_save( self, record_IN, debug_flag_IN = False ):

        '''
        Accepts current record, can be extended by a particular model
            to do non-standard processing.

        Preconditions: assumes you'll pass something in to every argument. A
            None in any of them will cause errors.

        Postconditions: Also outputs error log message if there was a problem.
            Could throw exception on incorrect calls, but for now, we'll just
            make sure there is a good error message logged.

        - Also, in StatusContainer that is returned, expects
            self.PROP_WAS_INSTANCE_UPDATED to be set to True if
            updates occurred, False if not.

        Returns: StatusContainer with information on results.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "update_from_record_pre_save"
        status_message = None
        update_status = None
        update_success = None

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have record?
        if ( record_IN is not None ):

            # for base method, nothing to do, so SUCCESS!
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

        else:

            # no record passed in - log error, return false.
            status_message = "ERROR - No record passed in ( {} ).".format( record_IN )
            self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )

            # status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

        #-- END check to see if record is not None --#

        return status_OUT

    #-- END method update_from_record_pre_save()


    def update_from_record_post_save( self, record_IN, debug_flag_IN = False ):

        '''
        Accepts current record, can be extended by a particular model
            to do non-standard processing to update related information. This
            method will be called in processing stream after the instance is
            saved, so it will have an ID and can be referenced in ForeignKeys.

        Preconditions: assumes you'll pass something in to every argument. A
            None in any of them will cause errors.

        Postconditions: Also outputs error log message if there was a problem.
            Could throw exception on incorrect calls, but for now, we'll just
            make sure there is a good error message logged.

        - Also, in StatusContainer that is returned, expects
            self.PROP_WAS_INSTANCE_UPDATED to be set to True if updates
            occurred, False if not.

        Returns: StatusContainer with information on results.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "update_from_record_post_save"
        status_message = None
        update_status = None
        update_success = None

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have record?
        if ( record_IN is not None ):

            # for base method, nothing to do, so SUCCESS!
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

        else:

            # no record passed in - log error, return false.
            status_message = "ERROR - No json dictionary passed in ( {} ).".format( record_IN )
            self.output_log_message( status_message, method_IN = me, log_level_code_IN = logging.ERROR )

            # status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )
            status_OUT.set_detail_value( self.PROP_WAS_INSTANCE_UPDATED, False )

        #-- END check to see if record is not None --#

        return status_OUT

    #-- END method update_from_record_post_save()


#-- END abstract LoadableDjangoModel class --#
