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
import six # help with supporting both python 2 and 3.

# define JSONHelper class.
class JSONHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False


    #============================================================================
    # static methods
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
    def pretty_print_json( json_IN ):
    
        '''
        Accepts JSON object.  Formats it nicely, returns the formatted string.
        '''
    
        # return reference
        string_OUT = ""
        
        string_OUT = json.dumps( json_IN, sort_keys = True, indent = 4, separators = ( ',', ': ' ) )
        
        return string_OUT
        
    #-- END method pretty_print_json() --#
    
    
#-- END class JSONHelper --#