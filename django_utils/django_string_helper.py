# python_utilities includes.
import python_utilities.strings.string_helper

# django includes
import django.utils.encoding

# start to python 3 support:
from __future__ import unicode_literals

class DjangoStringHelper( python_utilities.strings.string_helper.StringHelper ):
    

    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def convert_to_unicode( cls, string_IN, encoding_IN = "", *args, **kwargs ):
        
        """
        Converts string to unicode.  Uses django.utils.encoding.smart_text
           instead of unicode().
        
        Based in part on:
        http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        http://nedbatchelder.com/text/unipain.html
        """
    
        # return reference
        string_OUT = ""
        
        # decode from external encoding to unicode (probably is UTF-8).

        # dp we have an encoding passed in?
        if ( ( encoding_IN ) and ( encoding_IN != None ) and ( encoding_IN != "" ) ):
        
            # encoding passed in.  Use it.
            string_OUT = django.utils.encoding.smart_text( string_IN, encoding_IN )
        
        else:
            
            # no encoding - use default.
            string_OUT = django.utils.encoding.smart_text( string_IN )
            
        #-- END see if encoding is passed in. --#
        
        return string_OUT
    
    #-- END convert_to_unicode() function --#


#-- END class DjangoStringHelper --#