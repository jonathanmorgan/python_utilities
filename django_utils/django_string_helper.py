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

# start to python 3 support:
from __future__ import unicode_literals

# python_utilities includes.
import python_utilities.strings.string_helper

# django includes
import django.utils.encoding

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