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

def get_dict_value( dict_IN, name_IN, default_IN = None ):

    '''
    Accepts dictionary, name, and optional default value (if no default provided,
       default is None).  If dictionary or name missing, returns default.  If
       name not present in dictionary, returns default.  If name in dictionary,
       returns whatever is mapped to name.
       
    Parameters:
    - dict_IN - dictionary we are looking in.
    - name_IN - name we are looking for in dictionary.
    - default_IN (defaults to None) - default value to return if problem or not found in dict.
    
    Returns:
    - value_OUT - value mapped to name_IN in dict_IN, else the default value if problems or if not found in dict.
    '''

    # return reference
    value_OUT = None
    
    # first, make sure we have all the stuff we need.  If stuff missing, return
    #    default.
    if ( dict_IN ):
    
        # got dictionary.  Got name?
        if ( name_IN ):
        
            # see if name in dictionary.
            if ( name_IN in dict_IN ):
            
                # name is in dictionary.  Get value, return it.
                value_OUT = dict_IN[ name_IN ]
            
            else:
            
                # no matching key in dictionary.  Return default.
                value_OUT = default_IN
            
            #-- END check to see if name in dictionary. --#
        
        else:
        
            # no name.  Return default.
            value_OUT = default_IN
        
        #-- END check to see if name. --#
    
    else:
    
        # no dictionary.  Return default.
        value_OUT = default_IN
        
    #-- END check to see if dictionary passed in. --#
    
    return value_OUT

#-- END function get_dict_value --#