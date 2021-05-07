# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2015 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python_utilities is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/python_utilities.  If not, see
<http://www.gnu.org/licenses/>.
'''

'''
Usage:

# using JSON object json_object

# import JSONHelper
from python_utilities.json.json_helper import JSONHelper

# pretty print JSON object
pretty_json_string = JSONHelper.pretty_print_json( json_object )

'''

# Imports

# base python modules
import hashlib
import json
import logging

# basic packages
import regex
import six # help with supporting both python 2 and 3.

# python utilities
from python_utilities.json.python_utility_json_error import PythonUtilityJSONError
from python_utilities.logging.logging_helper import LoggingHelper

# define JSONHelper class.
class JSONHelper( object ):


    #============================================================================
    # ! ==> constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    MY_LOGGER = "python_utilities.json.JSONHelper"

    # regular expression for quote escaping.
    REGEX_MATCH_UNESCAPED_QUOTES = regex.compile( r'(?<!\\)"' )
    REGEX_MATCH_MULTIPLE_WHITE_SPACE = regex.compile( r'\s+' )

    # replace newline with...
    REPLACE_NEWLINE_WITH = "\\n"

    #============================================================================
    # ! ==> static methods
    #============================================================================


    @staticmethod
    def get_json_object_property( json_object_IN, name_IN, default_IN = None ):

        '''
        Accepts name of a JSON property that you expect to be contained in the
           JSON object passed in.  Returns property that corresponds to name. If
           not found, returns default value (which defaults to None).
        '''

        # return reference
        value_OUT = None

        # check if name is present.
        if name_IN in json_object_IN:

            # yes - return the JSON that is mapped to that name.
            value_OUT = json_object_IN[ name_IN ]

        else:

            # return default.
            value_OUT = default_IN

        #-- END check to see if name in root --#

        return value_OUT

    #-- END get_json_object_property() --#


    @staticmethod
    def pretty_print_json( json_IN, sort_keys_IN = True, indent_IN = 4, separators_IN = ( ',', ': ' ) ):

        '''
        Accepts JSON object.  Formats it nicely, returns the formatted string.
        '''

        # return reference
        string_OUT = ""

        string_OUT = json.dumps( json_IN, sort_keys = sort_keys_IN, indent = indent_IN, separators = separators_IN )

        return string_OUT

    #-- END method pretty_print_json() --#


    #============================================================================
    # !class methods
    #============================================================================


    @classmethod
    def create_standard_json_hash( cls, json_IN, hash_function_IN = hashlib.sha256 ):

        '''
        Accepts JSON object. Converts to standard format string by calling
            standardize_json_to_string(), then makes and a SHA256 hash of the
            standardized JSON string and returns the hexdigest of the hash.
        '''

        # return reference
        value_OUT = ""

        # declare variables.
        me = "create_standard_json_hash"
        status_message = None
        json_string = None
        json_bytes = None
        json_hash = None
        json_hash_hexdigest = None

        # something passed in?
        if ( json_IN is not None ):

            # convert
            json_string = cls.standardize_json_to_string( json_IN )

            # encode string (convert to bytes)
            json_bytes = json_string.encode()

            # create hash
            json_hash = hash_function_IN( json_bytes )

            # get hex digest of hash
            json_hash_hexdigest = json_hash.hexdigest()

            # return it.
            value_OUT = json_hash_hexdigest

        else:

            # error - nothing passed in, None returned.
            value_OUT = None
            status_message = "ERROR - In {method}(): nothing passed in ( \"{json_object}\" ), returning None.".format(
                method = me,
                json_object = json_IN
            )
            LoggingHelper.log_message(
                status_message,
                method_IN = me,
                logger_name_IN = cls.MY_LOGGER,
                do_print_IN = True,
                log_level_code_IN = LoggingHelper.LOG_LEVEL_CODE_ERROR
            )
            raise PythonUtilityJSONError( status_message )

        #-- END check to see if something passed in. --#

        return value_OUT

    #-- END method create_standard_json_hash() --#


    @classmethod
    def escape_all_string_json_values( cls, json_IN, do_double_escape_quotes_IN = False ):

        '''
        loops over all properties in JSON dictionary or list passed in.  If
           value is of type str, escapes the value.  If value is of type list or
           dict, recursively calls this function, passing it the value.  Returns
           updated dictionary.

        postconditions: updates in place - if strings found, json object passed
            in is altered once this method completes.
        '''

        # return reference
        json_OUT = None

        # declare variables
        json_name = ""
        json_value = ""
        json_list_index = -1
        json_result = None
        json_list_value = None

        # got anything passed in?
        if ( json_IN is not None ):

            # dictionary?
            if ( isinstance( json_IN, dict ) == True ):

                # make new dictionary to hold results.
                json_OUT = {}

                # loop over dictionary items.
                for json_name, json_value in six.iteritems( json_IN ):

                    # string?
                    if ( isinstance( json_value, str ) == True ):

                        # yes.  Escape, store value back in dict.
                        json_OUT[ json_name ] = cls.escape_json_value( json_value, do_double_escape_quotes_IN )

                    # no.  Dictionary?
                    elif ( isinstance( json_value, dict ) == True ):

                        # yes - call this method on the dictionary.
                        json_OUT[ json_name ] = cls.escape_all_string_json_values( json_value, do_double_escape_quotes_IN )

                    # no.  List?
                    elif ( isinstance( json_value, list ) == True ):

                        # it is a list - call this method on it.
                        json_OUT[ json_name ] = cls.escape_all_string_json_values( json_value, do_double_escape_quotes_IN )

                    else:

                        # not anything we know how to process.  Pass.
                        json_OUT[ json_name ] = json_value

                    #-- END check of type of value.

                #-- END loop over items in this dictionary --#

            elif ( isinstance( json_IN, list ) == True ):

                # list - make new list to hold result.
                json_OUT = []

                # loop over and process values.
                json_list_index = -1
                for json_value in json_IN:

                    # increment index
                    json_list_index += 1

                    # string?
                    if ( isinstance( json_value, str ) == True ):

                        # yes.  Escape, store value back in list at same index.
                        json_list_value = cls.escape_json_value( json_value, do_double_escape_quotes_IN )


                    # no.  Dictionary?
                    elif ( isinstance( json_value, dict ) == True ):

                        # yes - call this method on the dictionary.
                        json_list_value = cls.escape_all_string_json_values( json_value, do_double_escape_quotes_IN )

                    # no.  List?
                    elif ( isinstance( json_value, list ) == True ):

                        # it is a list - call this method on it.
                        json_list_value = cls.escape_all_string_json_values( json_value, do_double_escape_quotes_IN )

                    else:

                        # not anything we know how to process.  Pass.
                        json_list_value = json_value

                    #-- END check of type of value.

                    # append!
                    json_OUT.append( json_list_value )

                #-- END loop over JSON list items. --#

            else:

                # not anything we can process.  Pass.
                json_OUT = json_IN

            #-- END check of type of what was passed in. --#

        #-- END check to see if we have other than None. --#

        return json_OUT

    #-- END static method escape_all_string_json_values


    @classmethod
    def escape_json_value( cls,
                           json_value_IN,
                           do_double_escape_quotes_IN = False,
                           compact_white_space_IN = False ):

        '''
        Accepts a JSON value, adds a back slash in front of all quotation marks
           within the value.  Returns the escaped string.  Will add more things
           as I find them.
        '''

        # return reference
        value_OUT = None

        # got a value?
        if ( ( json_value_IN is not None ) and ( json_value_IN != "" ) ):

            # yes
            value_OUT = json_value_IN

            # do we double-escape quotes?
            if ( do_double_escape_quotes_IN == True ):

                # first, escape any naked quotes
                value_OUT = cls.REGEX_MATCH_UNESCAPED_QUOTES.sub( "\\\"", value_OUT )

                # take all '\\\"' and convert them to '\\\\\\\"'
                value_OUT = value_OUT.replace( "\\\"", "\\\\\\\"" )

            else:

                # precede all quotation marks with a backslash ( "\" )
                value_OUT = value_OUT.replace( "\"", "\\\"" )

            #-- END check to see if we double-escape quotes. --#

            # add a slash before newline characters - JSON doesn't like newlines
            #     inside values.
            if ( "\n" in value_OUT ):

                # so, back to what to do about a newline...
                #value_OUT += "NEWLINE!"
                value_OUT = value_OUT.replace( "\n", cls.REPLACE_NEWLINE_WITH )

            #-- END check to see if newline --#

            # compact white space?
            if ( compact_white_space_IN == True ):

                # replace multiple white space of all kinds with a single space.
                value_OUT = cls.REGEX_MATCH_MULTIPLE_WHITE_SPACE.sub( " ", value_OUT )

            #-- END check to see if compact white space. --#

        else:

            # no return empty string.
            value_OUT = ""

        #-- END check to see if value passed in. --#

        return value_OUT

    #-- END escape_json_value() --#


    @classmethod
    def load_json_from_file( cls, json_file_path_IN ):

        '''
        Accepts path to file that contains JSON.  Opens file, reads contents,
            and converts them to JSON. Returns result.
        '''

        # return reference
        json_OUT = ""

        # declare variables.
        me = "load_json_from_file"
        json_file = None

        # something passed in?
        if ( ( json_file_path_IN is not None ) and ( json_file_path_IN != "" ) ):

            # read from file and convert
            with open( json_file_path_IN ) as json_file:

                # load json from file.
                json_OUT = json.load( json_file )

            #-- END with open() as json_file --#

        else:

            # error - nothing passed in, None returned.
            json_OUT = None
            print( "ERROR - In {}(): nothing passed in ( \"{}\" ), returning None.".format( me, json_file_path_IN ) )

        #-- END check to see if something passed in. --#

        return json_OUT

    #-- END method load_json_from_file() --#


    @classmethod
    def standardize_json_to_string( cls, json_IN ):

        '''
        Accepts JSON object.  Formats it with keys sorted, 2 space indent, all
            white space trimmed from beginning and end, returns the formatted
            string.
        '''

        # return reference
        string_OUT = ""

        # declare variables.
        me = "standardize_json_to_string"

        # something passed in?
        if ( json_IN is not None ):

            # convert
            string_OUT = cls.pretty_print_json( json_IN, sort_keys_IN = True, indent_IN = 2 )

            # strip off any leading or trailing white space, just in case.
            string_OUT = string_OUT.strip()

        else:

            # error - nothing passed in, None returned.
            string_OUT = None
            print( "ERROR - In {}(): nothing passed in ( \"{}\" ), returning None.".format( me, json_IN ) )

        #-- END check to see if something passed in. --#

        return string_OUT

    #-- END method standardize_json_to_string() --#


#-- END class JSONHelper --#
