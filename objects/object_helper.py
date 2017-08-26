# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2012-2014 Jonathan Morgan

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

# imports
import inspect

class ObjectHelper( object ):


    @classmethod
    def get_type_name( cls, reference_IN, *args, **kwargs ):
        
        '''
        Accepts a reference to something.  Calls type() on the reference, then
            gets the __name__ of the type.  This is as much a reminder to me as
            it is a genuinely useful method.
        '''
        
        # return reference
        value_OUT = ""
        
        # declare variables
        reference_type = None
        type_name = ""
        
        # get type of reference passed in.
        reference_type = type( reference_IN )
        
        # get name of type.
        type_name = reference_type.__name__
        
        value_OUT = type_name
        
        return value_OUT
        
    #-- END class method get_type_name() --#


    @classmethod
    def get_user_attributes( cls, class_IN, exclude_boring_IN = True, *args, **kwargs ):

        '''
        Based on: http://stackoverflow.com/questions/4241171/inspect-python-class-attributes
        '''

        # declare variables
        boring = None
        attrs = None

        # get list of attributes of default object.
        boring = dir( type( 'dummy', ( object, ), {} ) )

        # initialize dictionary of attributes.
        attrs = {}

        # get base cases for current class.
        bases = reversed( inspect.getmro( class_IN ) )   

        # loop over base classes.
        for base in bases:
        
            # check for __dict__
            if hasattr( base, '__dict__' ):

                # update from __dict__
                attrs.update( base.__dict__ )

            # else, check for __slots__
            elif hasattr( base, '__slots__' ):
            
                if hasattr( base, base.__slots__[ 0 ] ): 

                    # We're dealing with a non-string sequence or one char string
                    for item in base.__slots__:

                        attrs[ item ] = getattr( base, item )
                        
                    #-- END loop over __slots__ --#

                else: 

                    # We're dealing with a single identifier as a string
                    attrs[ base.__slots__ ] = getattr( base, base.__slots__ )
                    
                #-- END check I don't necessarily understand as of yet. --#
                    
            #-- END check to see if __slots__ attribute. --#
        
        #-- END loop over base classes --#

        # remove anything that is in the "boring" list.
        if ( exclude_boring_IN == True ):
        
            for key in boring:
    
                del attrs[ key ]  # we can be sure it will be present so no need to guard this
                
            #-- END loop over boring --#
            
        #-- END check to see if we exclude boring --#

        return attrs

    #-- END method get_user_attributes() --#


#-- END class ObjectHelper --#