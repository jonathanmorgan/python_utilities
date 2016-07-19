# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2016-present Jonathan Morgan

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

#================================================================================
# imports
#================================================================================


import six # help with supporting both python 2 and 3.


#================================================================================
# class definitions
#================================================================================


# define ListHelper class.
class ListHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    STATUS_ERROR_PREFIX = "Error: "


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def get_value_as_list( cls, value_IN, delimiter_IN = ',' ):
        
        # return reference
        list_OUT = []
        
        # declare variables
        me = "get_value_as_list"
        list_param_value = ""
        working_list = []
        current_value = ""
        current_value_clean = ""
        
        # store value 
        list_param_value = value_IN
        
        # check if list...
        if ( isinstance( list_param_value, list ) == True ):
        
            # already a list - return it.
            list_OUT = list_param_value
            
        # ...check if string...
        elif ( isinstance( list_param_value, six.string_types ) == True ):
        
            # string.  Empty?
            if ( list_param_value == "" ):
        
                # empty string - return empty list
                list_OUT = []
        
            else:
            
                # not an empty string - split on delimiter into a list
                working_list = list_param_value.split( delimiter_IN )
                
                # loop over the items in the list, strip()-ing each then
                #     appending it to list_OUT.
                list_OUT = []
                for current_value in working_list:
             
                    # strip
                    current_value_clean = current_value.strip()
                    list_OUT.append( current_value_clean )
        
                #-- END loop over items in list --#
                
            #-- END check to see if empty string.
            
        # ...check if None...
        elif ( list_param_value is None ):
        
            # if None, just return None, don't wrap it in a list.
            list_OUT = list_param_value
        
        else:
        
            # not list or string or None, take the thing and put it in a list.
            list_OUT = [ list_param_value ]
        
        #-- END check to see if already a list --#
        
        return list_OUT
        
    #-- END method get_value_as_list() --#
    

#-- END class ListHelper --#
