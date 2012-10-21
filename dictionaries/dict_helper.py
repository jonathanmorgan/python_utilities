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