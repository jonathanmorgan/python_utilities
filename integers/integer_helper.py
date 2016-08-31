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


# define IntegerHelper class.
class IntegerHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    STATUS_ERROR_PREFIX = "Error: "


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def is_valid_integer( cls, value_IN, must_be_greater_than_IN = -1 ):
        
        '''
        Checks to see if the value passed in is:
        - not None
        - an integer
        - greater than must_be_greater_than_IN
        
        If all are True, returns True.  If any are False, returns False.
        '''
        
        # return reference
        is_valid_OUT = True
        
        # declare variables
        me = "is_valid_integer"
        
        # Is value None?
        if ( value_IN is not None ):

            # Not None - check if integer...
            if ( isinstance( value_IN, six.integer_types ) == True ):
            
                # it is an integer - greater than must_be_greater_than_IN
                if ( must_be_greater_than_IN is not None ):

                    if ( value_IN > must_be_greater_than_IN ):
                    
                        # valid
                        is_valid_OUT = True
                        
                    else:
                    
                        # not greater-than enough.
                        is_valid_OUT = False
                    
                    #-- END check to see if value large enough --#
                
                else:
                
                    # no indicator of required value magnitude.  OK!
                    is_valid_OUT = True
                    
                #-- END check to see if must_be_greater_than_IN value --#
                
            else:
            
                # value is not of integer type.  Not a valid integer.
                is_valid_OUT = False
                
            #-- END check to see if integer type.
                
        else:
        
            # None - not a valid integer.
            is_valid_OUT = False
            
        #-- END check to see if None. --# 
        
        return is_valid_OUT
        
    #-- END method is_valid_integer() --#
    

#-- END class IntegerHelper --#
