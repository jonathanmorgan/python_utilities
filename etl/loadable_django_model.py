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

from django.db import models

# ETL imports
from python_utilities.etl.etl_entity import ETLEntity
from python_utilities.etl.etl_error import ETLError
from python_utilities.etl.etl_attribute import ETLAttribute

class LoadableDjangoModel( models.Model ):

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
    def run_etl( cls, *args, **kwargs ):

        # return reference
        status_OUT = None

        # declare variables
        me = "run_etl"

        raise ETLError( "In abstract-ish method LoadableDjangoModel.{}(): OVERRIDE ME".format( me ) )

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


    def update_from_record( self, record_IN ):

        '''
        Accepts current record, can be extended by a particular model
            to do non-standard processing.

        Preconditions: assumes you'll pass something in to every argument. A
            None in any of them will cause errors.

        Postconditions: Also outputs error log message if there was a problem.
            Could throw exception on incorrect calls, but for now, we'll just
            make sure there is a good error message logged.

        Returns: StatusContainer with information on results.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "update_from_record"
        status_message = None
        update_status = None
        update_success = None

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # do we have json?
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

    #-- END method update_from_record()


#-- END abstract LoadableDjangoModel class --#
