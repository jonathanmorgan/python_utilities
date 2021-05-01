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


    def update_extra_data_attr( self, attr_name_IN, attr_value_IN ):

        # declare variables
        me = "update_extra_data_attr"
        extra_data_json = None

        # get extra data JSONField
        extra_data_json = self.extra_data

        # got anything already?
        if ( ( extra_data_json is None ) or ( extra_data_json == "" ) ):

            # no - create dictionary.
            extra_data_json = dict()
            self.extra_data = extra_data_json

        #-- END check to see if initialized --#

        # update the value for this attribute in the dictionary.
        extra_data_json[ attr_name_IN ] = attr_value_IN

    #-- END method update_extra_data


#-- END abstract LoadableDjangoModel class --#
