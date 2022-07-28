# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2014 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

python_utilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/python_utilities. If not, see http://www.gnu.org/licenses/.
'''

'''
Usage:

    # import ParamContainer
    from python_utilities.parameters.param_container import ParamContainer

    # make an instance
    my_param_container = ParamContainer()

    # define parameters (for outputting debug, nothing more at this point)
    my_param_container.define_parameter( "test_int", ParamContainer.PARAM_TYPE_INT )
    my_param_container.define_parameter( "test_string", ParamContainer.PARAM_TYPE_STRING )
    my_param_container.define_parameter( "test_list", ParamContainer.PARAM_TYPE_LIST )

    # load parameters in a dict
    my_param_container.set_parameters( params )

    # load parameters from a django HTTP request
    my_param_container.set_request( request )

    # get parameter value - pass name and optional default if not present.
    test_int = my_param_container.get_param( "test_int", -1 )
    test_string = my_param_container.get_param( "test_string", "" )
    test_list = my_param_container.get_param( "test_list", [] )

    # get param as int
    test_int = my_param_container.get_param_as_int( "test_int", -1 )

    # get param as str
    test_string = my_param_container.get_param_as_str( "test_string", -1 )

    # get param as list - pass in name, optional default, list delimiter string (defaults to ",")
    test_int = my_param_container.get_param_as_list( "test_int", -1, delimiter_IN = "," )

'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================


# python_utilities
from python_utilities.dictionaries.dict_helper import DictHelper


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class ParamContainer( object ):


    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------

    # types of params.
    PARAM_TYPE_INT = 'int'
    PARAM_TYPE_LIST = 'list'
    PARAM_TYPE_STRING = 'string'

    # PARAMS object types
    PARAMS_OBJECT_TYPE_DJANGO_QUERY_DICT = "<class 'django.http.request.QueryDict'>"


    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # declare variables
        self.request = None
        self.params_dictionary = {}
        self.param_name_to_type_dict = {}

    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def debug_parameters( self ):

        # return reference
        string_OUT = ''

        # declare variables
        params_IN = None
        expected_params = None
        param_name = ''
        param_type = ''
        param_value_raw = ''
        param_value = ''
        param_value_list = None
        param_output_string = ''
        output_string_list = []
        list_separator_string = ""

        # retrieve parameters
        params_IN = self.get_parameters()

        # got params?
        if ( params_IN ):

            # get list of expected params
            expected_params = self.param_name_to_type_dict

            # loop over expected parameters, grabbing each and adding it to the
            #    output string.
            for param_name, param_type in expected_params.items():

                # initialize this param's output string.
                param_output_string = param_name + " = "

                # get raw param value
                param_value_raw = self.get_param( param_name, None )
                param_output_string += "\"" + str( param_value_raw ) + "\""

                # see if we have a string or a list.
                if ( param_type == ParamContainer.PARAM_TYPE_STRING ):

                    # get param value
                    param_value = self.get_param_as_str( param_name, '' )

                    # append to output string list.
                    param_output_string += "\n----> typeof str: \"" + param_value + "\""

                elif ( param_type == ParamContainer.PARAM_TYPE_LIST ):

                    # get param value list
                    param_value_list = self.get_param_as_list( param_name )

                    param_output_string += "\n----> typeof list: \"" + str( param_value_list ) + "\""

                    # output list of values
                    #for param_value in param_value_list:

                    #    param_output_string += param_value + ", "

                    #-- END loop over values in list. --#

                    #param_output_string += "\""

                #-- END handle different types of parameters appropriately --#

                # append closing semicolon.
                param_output_string += ";"

                # then append output string to output string list.
                output_string_list.append( param_output_string )

            #-- END loop over parameters --#

            # initialize output string.
            string_OUT = "Parameters:\n-----------------------------\n"

            # now, join the parameters together for each, separated by "\n".
            list_separator_string = "\n"
            string_OUT += list_separator_string.join( output_string_list )

        #-- END check to see if we have params --#

        return string_OUT

    #-- end method debug_parameters() ------------------------------------------


    def define_parameter( self, name_IN, type_IN = PARAM_TYPE_STRING ):

        """
            Method: define_parameter()

            Purpose: accepts the name and type of a parameter, adds them to the
            internal dict that maps param names to their types.

            Params:
            - name_IN - name of parameter we are defining.
            - type_IN - type of parameter - should be one of the PARAM_TYPE_* constants-ish.
        """

        # declare variables
        name_to_type_dict = None

        # get dict
        name_to_type_dict = self.param_name_to_type_dict

        # add parameter
        name_to_type_dict[ name_IN ] = type_IN

    #-- END method define_parameter() --#


    def get_parameters( self ):

        # return reference
        dict_OUT = ""

        # declare variables

        # try to retrieve value - for now, reference nested request.POST
        dict_OUT = self.params_dictionary

        return dict_OUT

    #-- END method get_parameters() --#


    def get_param( self, param_name_IN, default_IN = None ):

        # return reference
        value_OUT = ""

        # declare variables
        my_params = None

        # try to retrieve value - for now, reference nested parameters.
        my_params = self.get_parameters()
        value_OUT = DictHelper.get_dict_value( my_params, param_name_IN, default_IN )

        return value_OUT

    #-- END method get_param() --#


    def get_param_as_boolean( self, param_name_IN, default_IN = None ):

        # return reference
        value_OUT = ""

        # declare variables
        my_value = None

        # call get_param()
        my_value = self.get_param( param_name_IN, default_IN = None )
        value_OUT = BooleanHelper.convert_value_to_boolean( my_value, default_IN = default_IN )

        return value_OUT

    #-- END method get_param_as_boolean() --#


    def get_param_as_int( self, param_name_IN, default_IN = -1 ):

        # return reference
        value_OUT = ""

        # call get_param()
        my_params = self.get_parameters()
        value_OUT = DictHelper.get_dict_value_as_int( my_params, param_name_IN, default_IN )

        return value_OUT

    #-- END method get_string_param() --#


    def get_param_as_list( self, param_name_IN, default_IN = [], delimiter_IN = ',' ):

        # return reference
        list_OUT = []

        # declare variables
        my_params = None
        #params_type = None
        #params_type_string = None
        my_request = None

        # get params
        my_params = self.get_parameters()

        # got a request?  Because of special way that request.POST and
        #    request.GET behave in terms of list parameters, if you have a
        #    request and might have multi-valued inputs, you need to use the
        #    request and its child objects to retrieve the multi-valued input
        #    as a list.  It must be that the way it stores them stores each input
        #    independently, even when multiple have the same name.  It is aware
        #    that these can sometimes be considered lists, but only returns a
        #    list if asked, otherwise only returns the first or last value it.
        my_request = self.request
        if ( my_request is not None ):

            #print( "request!"  )

            # get list using request.POST.getlist()/request.GET.getlist()
            list_OUT = my_params.getlist( param_name_IN, [] )

            # if input is present but empty, returns list that has a single
            #    element in it, an empty string.  Want an empty list.
            if ( ( len( list_OUT ) == 1 ) and ( list_OUT[ 0 ] == "" ) ):

                # list with an empty string in it.  Return empty list.
                list_OUT = []

            #-- END check to see if it is a list with a single empty string in it. --#

        else:

            #print( "NO request!"  )

            # not a request object - call get_dict_value_as_list()
            list_OUT = DictHelper.get_dict_value_as_list( my_params, param_name_IN, default_IN, delimiter_IN )

        #-- END check to see if request or not. --#

        #print( "list_OUT = " + str( list_OUT ) )

        return list_OUT

    #-- END method get_param_as_list() --#


    def get_param_as_str( self, param_name_IN, default_IN = '' ):

        # return reference
        value_OUT = ""

        # call get_param()
        my_params = self.get_parameters()
        value_OUT = DictHelper.get_dict_value_as_str( my_params, param_name_IN, default_IN )

        return value_OUT

    #-- END method get_param_as_str() --#


    def get_param_type( self, param_name_IN, default_IN = None ):

        # return reference
        value_OUT = ""

        # declare variables
        name_to_type_map = None

        # try to retrieve type - for now, reference nested parameters.
        name_to_type_map = self.param_name_to_type_dict
        value_OUT = DictHelper.get_dict_value( name_to_type_map, param_name_IN, default_IN )

        return value_OUT

    #-- END method get_param_type() --#


    def get_string_param_as_list( self, param_name_IN, default_IN = [], delimiter_IN = ',' ):

        # return reference
        list_OUT = []

        # declare variables
        my_params = None
        my_request = None

        # get params
        my_params = self.get_parameters()

        # call get_dict_value_as_list()
        list_OUT = DictHelper.get_dict_value_as_list( my_params, param_name_IN, default_IN, delimiter_IN )

        #print( "list_OUT = " + str( list_OUT ) )

        return list_OUT

    #-- END method get_string_param_as_list() --#


    def set_parameter_value( self, name_IN, value_IN ):

        """
            Method: set_parameter_value()

            Purpose: accepts parameter name and value, stores value in nested
                parameter dictionary for that parameter name.

            Postconditions: Returns value set for name.

            Params:
            - name_IN - name of parameter we are setting.
            - value_IN - value to store for that param name.
        """

        # return reference
        value_OUT = None

        # declare variables
        param_type = None
        param_dictionary = None

        # got a param name?
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):

            # yes.  Got a type?
            param_type = self.get_param_type( name_IN )

            # get parameter dictionary
            param_dictionary = self.get_parameters()

            # store the value in the name.
            param_dictionary[ name_IN ] = value_IN

        #-- END check to see if we have a name --#

        value_OUT = self.get_param( name_IN )

        return value_OUT

    #-- END method set_parameter_value() --#


    def set_parameters( self, dict_IN ):

        """
            Method: set_parameters()

            Purpose: accepts a dict of parameters, stores it in instance.

            Params:
            - dict_IN - dict of parameter names mapped to values.
        """

        # declare variables

        # got a request?
        if ( dict_IN ):

            # store params
            self.params_dictionary = dict_IN

        #-- END check to see if we have a dictionary --#

    #-- END method set_parameters() --#


    def set_request( self, request_IN ):

        """
            Method: set_request()

            Purpose: accepts a request, stores it in instance, then grabs the
                POST from the request and stores that as the params.

            Params:
            - request_IN - django HTTPRequest instance.
        """

        # declare variables
        params_IN = None

        # got a request?
        if ( request_IN ):

            # store request
            self.request = request_IN

            # get params
            params_IN = request_IN.POST

            # store params
            self.set_parameters( params_IN )

        #-- END check to see if we have a request --#

    #-- END method set_request() --#


#-- END class ParamContainer --#
