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