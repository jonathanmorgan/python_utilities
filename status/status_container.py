# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

python_utilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/python_utilities. If not, see http://www.gnu.org/licenses/.
'''

'''
Usage:

    # import StatusContainer
    from python_utilities.status.status_container import StatusContainer

    # make an instance
    my_status_container = StatusContainer()

    # set status code
    my_status_container.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

    # set non-standard status code
    my_status_container.set_status_code( "banana", require_known_IN = False )

    # add a status message
    status_message = "This is totally a success!"
    my_status_container.add_message( status_message )

    # add a tag
    my_status_container.add_tag( "linux" )

    # you can also build a dictionary of name-value pair details.
    my_status_container.set_detail_value( "detail_name_1", "detail_value_1" )
    my_status_container.set_detail_value( "detail_name_2", "2" )
    my_status_container.set_detail_value( "detail_name_3", "detail_value_3" )
    my_status_container.set_detail_value( "detail_name_4", [ "a", "b", "c" ] )

    # and, nest other status containers if you want...
    other_status = tell_me_a_status()
    my_status_container.add_status_container( other_status )

    # is it a success?
    is_success = my_status_container.is_success()

    # is it a warning?
    is_warning = my_status_container.is_warning()

    # is it an error?
    is_error = my_status_container.is_error()

    # get list of status messages
    my_status_message_list = my_status_container.get_message_list()

    # get detail values
    detail_1 = my_status_container.get_detail_value( "detail_name_1" )
    detail_2 = my_status_container.get_detail_value_as_int( "detail_name_2" )
    detail_3 = my_status_container.get_detail_value_as_str( "detail_name_3" )
    detail_4 = my_status_container.get_detail_value_as_list( "detail_name_4" )

'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================


# python_utilities
from python_utilities.dictionaries.dict_helper import DictHelper


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================


class StatusContainer( object ):


    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------

    # status code values
    STATUS_CODE_SUCCESS = "success"
    STATUS_CODE_WARNING = "warning"
    STATUS_CODE_ERROR = "error"
    VALID_STATUS_LIST = [ STATUS_CODE_SUCCESS, STATUS_CODE_WARNING, STATUS_CODE_ERROR ]


    #---------------------------------------------------------------------------
    # ! ==> __init__() and __str__() methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # declare variables
        self.process_name = ""
        self.status_code = None
        self.status_tag_list = []
        self.status_message_list = []
        self.status_details_dict = {}
        self.status_container_list = []

        # and a place to store a return reference
        self.return_reference = None

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        string_OUT = str( self.status_code ) + ": tags = " + str( self.status_tag_list ) + "; messages = " + str( self.status_message_list )

        return string_OUT

    #-- END method __str__() --#


    #---------------------------------------------------------------------------
    # ! ==> instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def add_message( self, value_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        message_list = None

        # got something (no sense appending empty messages).
        if ( ( value_IN is not None ) and ( value_IN != "" ) ):

            # retrieve the message list.
            message_list = self.status_message_list

            # add message to the list
            message_list.append( value_IN )

        #-- END check to see if message passed in. --#

        value_OUT = value_IN

        return value_OUT

    #-- END method add_message() --#


    def add_messages_from_list( self, list_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        message_list = None

        # got something (no sense appending empty messages).
        if ( ( list_IN is not None ) and ( len( list_IN ) > 0 ) ):

            # retrieve the message list.
            message_list = self.status_message_list

            # add message to the list
            message_list.extend( list_IN )

        #-- END check to see if message passed in. --#

        value_OUT = message_list

        return value_OUT

    #-- END method add_messages_from_list() --#


    def add_tag( self, value_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        tag_list = None

        # got something (no sense appending empty tags).
        if ( ( value_IN is not None ) and ( value_IN != "" ) ):

            # retrieve the list.
            tag_list = self.status_tag_list

            # add value to the list
            tag_list.append( value_IN )

        #-- END check to see if message passed in. --#

        value_OUT = value_IN

        return value_OUT

    #-- END method add_tag() --#


    def add_status_container( self, instance_IN, *args, **kwargs ):

        # return reference
        instance_OUT = ""

        # declare variables
        status_instance_list = None

        # got something (no sense appending empty messages).
        if ( ( instance_IN is not None ) and ( isinstance( instance_IN, StatusContainer ) == True ) ):

            # retrieve the status container list.
            status_instance_list = self.status_container_list

            # add message to the list
            status_instance_list.append( instance_IN )

        #-- END check to see if message passed in. --#

        instance_OUT = instance_IN

        return instance_OUT

    #-- END method add_status_container() --#


    def get_details_dict( self, *args, **kwargs ):

        # return reference
        dict_OUT = ""

        # declare variables
        details_dict = None

        # retrieve value
        details_dict = self.status_details_dict

        # None?
        if ( details_dict is None ):

            # None.  Make one.
            details_dict = {}

            # store it.
            self.set_details( details_dict )

            # get it
            details_dict = self.get_details_dict()

        #-- END check to see if dictionary --#

        dict_OUT = details_dict

        return dict_OUT

    #-- END method get_details_dict() --#


    def get_detail_value( self, name_IN, default_IN = None, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        my_dict = None

        # try to retrieve value - for now, reference nested parameters.
        my_dict = self.get_details_dict()
        value_OUT = DictHelper.get_dict_value( my_dict, name_IN, default_IN )

        return value_OUT

    #-- END method get_detail_value() --#


    def get_detail_value_as_int( self, name_IN, default_IN = -1, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        my_dict = None

        # call get_param()
        my_dict = self.get_details_dict()
        value_OUT = DictHelper.get_dict_value_as_int( my_dict, name_IN, default_IN )

        return value_OUT

    #-- END method get_detail_value_as_int() --#


    def get_detail_value_as_list( self, name_IN, default_IN = [], delimiter_IN = ',', *args, **kwargs ):

        # return reference
        list_OUT = []

        # declare variables
        my_dict = None

        # get params
        my_dict = self.get_details_dict()

        # call get_dict_value_as_list()
        list_OUT = DictHelper.get_dict_value_as_list( my_dict, name_IN, default_IN, delimiter_IN )

        return list_OUT

    #-- END method get_detail_value_as_list() --#


    def get_detail_value_as_str( self, name_IN, default_IN = '', *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        my_dict = None

        # call get_details_dict()
        my_dict = self.get_details_dict()
        value_OUT = DictHelper.get_dict_value_as_str( my_dict, name_IN, default_IN )

        return value_OUT

    #-- END method get_detail_value_as_str() --#


    def get_message_list( self, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables

        # retrieve value
        value_OUT = self.status_message_list

        return value_OUT

    #-- END method get_message_list() --#


    def get_status_code( self, *args, **kwargs ):

        # return reference
        value_OUT = ""

        value_OUT = self.status_code

        return value_OUT

    #-- END method get_status_code() --#


    def get_tag_count( self, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        tag_list = None

        # retrieve tag list.
        tag_list = self.get_tag_list()

        # get len()
        value_OUT = len( tag_list )

        return value_OUT

    #-- END method get_tag_count() --#


    def get_tag_list( self, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables

        # retrieve value.
        value_OUT = self.status_tag_list

        return value_OUT

    #-- END method get_tag_list() --#


    def has_tag( self, value_IN, *args, **kwargs ):

        # return reference
        value_OUT = False

        # declare variables
        my_tag_list = None

        # get status code.
        my_tag_list = self.status_tag_list

        # is value_IN in list?
        if ( value_IN in my_tag_list ):

            # it is.
            value_OUT = True

        else:

            # nope.
            value_OUT = False

        #-- END check to see if value is in list. --#

        return value_OUT

    #-- end method has_tag() --#


    def is_error( self, *args, **kwargs ):

        # return reference
        value_OUT = False

        # declare variables
        my_status_code = ""

        # get status code.
        my_status_code = self.status_code

        # is it STATUS_CODE_ERROR?
        if ( my_status_code == self.STATUS_CODE_ERROR ):

            # it is.  Error!
            value_OUT = True

        else:

            # nope.
            value_OUT = False

        #-- END check to see if error. --#

        return value_OUT

    #-- end method is_error() --#


    def is_success( self, *args, **kwargs ):

        # return reference
        value_OUT = False

        # declare variables
        my_status_code = ""

        # get status code.
        my_status_code = self.status_code

        # is it STATUS_CODE_SUCCESS?
        if ( my_status_code == self.STATUS_CODE_SUCCESS ):

            # it is.  Success!
            value_OUT = True

        else:

            # nope.
            value_OUT = False

        #-- END check to see if success. --#

        return value_OUT

    #-- end method is_success() --#


    def is_warning( self, *args, **kwargs ):

        # return reference
        value_OUT = False

        # declare variables
        my_status_code = ""

        # get status code.
        my_status_code = self.status_code

        # is it v?
        if ( my_status_code == self.STATUS_CODE_WARNING ):

            # it is.  Warning!
            value_OUT = True

        else:

            # nope.
            value_OUT = False

        #-- END check to see if warning. --#

        return value_OUT

    #-- end method is_warning() --#


    def set_details( self, dict_IN, *args, **kwargs ):

        """
            Method: set_details()

            Purpose: accepts a dict of status details, stores it in instance.

            Params:
            - dict_IN - dict of parameter names mapped to values.
        """

        # declare variables

        # got a request?
        if ( dict_IN ):

            # store params
            self.status_details_dict = dict_IN

        #-- END check to see if we have a dictionary --#

    #-- END method set_details() --#


    def set_detail_value( self, name_IN, value_IN, *args, **kwargs ):

        # return reference
        value_OUT = ""

        # declare variables
        my_dict = None

        # call get_param()
        my_dict = self.get_details_dict()
        my_dict[ name_IN ] = value_IN
        value_OUT = value_IN

        return value_OUT

    #-- END method get_detail_value_as_str() --#


    def set_status_code( self, value_IN, require_known_IN = True, *args, **kwargs ):

        # return reference
        status_code_OUT = None

        # declare variables

        # require a known status?
        if ( require_known_IN == True ):

            # see if known
            if ( value_IN in self.VALID_STATUS_LIST ):

                # known.  set it.
                self.status_code = value_IN
                status_code_OUT = self.get_status_code()

            else:

                # no known.
                status_code_OUT = None

            #-- END check if status code is known. --#

        else:

            # no.  Set it.
            self.status_code = value_IN

            status_code_OUT = self.get_status_code()

        #-- END check to see if we require a known status --#

        return status_code_OUT

    #-- END method set_status_code() --#


#-- END class ParamContainer --#
