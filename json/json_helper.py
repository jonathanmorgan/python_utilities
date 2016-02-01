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
import json

# basic packages
import regex
import six # help with supporting both python 2 and 3.

# define JSONHelper class.
class JSONHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    
    # regular expression for quote escaping.
    REGEX_MATCH_UNESCAPED_QUOTES = regex.compile( r'(?<!\\)"' )


    #============================================================================
    # static methods
    #============================================================================


    @staticmethod
    def escape_json_value( json_value_IN, do_double_escape_quotes_IN = False ):

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
                value_OUT = REGEX_MATCH_UNESCAPED_QUOTES.sub( "\\\"", value_OUT )

                # take all '\\\"' and convert them to '\\\\\\\"'
                value_OUT = value_OUT.replace( "\\\"", "\\\\\\\"" )
                
            else:

                # precede all quotation marks with a backslash ( "\" )
                value_OUT = value_OUT.replace( "\"", "\\\"" )
                
            #-- END check to see if we double-escape quotes. --#
        
        else:
        
            # no return empty string.
            value_OUT = ""
        
        #-- END check to see if value passed in. --#
        
        return value_OUT

    #-- END escape_json_value() --#


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
    def pretty_print_json( json_IN ):
    
        '''
        Accepts JSON object.  Formats it nicely, returns the formatted string.
        '''
    
        # return reference
        string_OUT = ""
        
        string_OUT = json.dumps( json_IN, sort_keys = True, indent = 4, separators = ( ',', ': ' ) )
        
        return string_OUT
        
    #-- END method pretty_print_json() --#
    
    
    #============================================================================
    # !class methods
    #============================================================================


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
    

#-- END class JSONHelper --#