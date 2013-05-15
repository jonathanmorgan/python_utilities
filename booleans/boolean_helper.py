'''
Copyright 2012, 2013 Jonathan Morgan

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

# Imports

# define BooleanHelper class.
class BooleanHelper( object ):

    #===========================================================================
    # CONSTANTS-ish
    #===========================================================================


    TRUE_STRING_VALUES = [ '1', 't', 'true', 'y', 'yes' ]


    #===========================================================================
    # class methods
    #===========================================================================

    @classmethod
    def convert_value_to_boolean( cls, value_IN ):
        
        """
        Compares the value passed in to known representations of boolean True:
        - 1
        - t (any case)
        - true (any case)
        - actual boolean value True
        If any of these match, returns True.  If not, returns false.
        """
    
        # return reference
        value_OUT = False
        
        # declare variables
        value_cleaned = ""
        
        # got something?
        if ( ( value_IN ) and ( value_IN != None ) and ( value_IN != "" ) ):
            
            # clean value (strip, to lower case).
            value_cleaned = str( value_IN )
            value_cleaned = value_cleaned.strip()
            value_cleaned = value_cleaned.lower()
            
            # check for True values.
            if value_cleaned in cls.TRUE_STRING_VALUES:
                
                value_OUT = True
            
            else:
                
                value_OUT = False
                
            #-- END check to see if value is in our true values. --#

        else:
            
            # not one of our approved values, so False.
            value_OUT = False
            
        #-- END set of boolean checks. --#
    
        return value_OUT
    
    #-- END convert_value_to_boolean() function --#


#-- END class BooleanHelper --#