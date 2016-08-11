'''
Copyright 2016 to present (currently 2016) Jonathan Morgan

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

# import six for Python 2 and 3 compatibility.
import six

# django imports
from django.db.models.query import QuerySet

# python_utilities includes.
from python_utilities.logging.logging_helper import LoggingHelper

class DjangoFormHelper( object ):
    

    #============================================================================
    # constants-ish
    #============================================================================


    LOGGER_NAME = "python_utilities.django_utils.DjangoFormHelper"
    IAMEMPTY = "IAMEMPTY"


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def is_form_empty( cls, form_IN, logger_name_IN = "", *args, **kwargs ):
        
        '''
        Accepts django Form or ModelForm in form_IN.  Goes through the fields in
            the form and checks to see if any has been populated.  If not,
            returns True (it is empty!).  If there is a value in any of them,
            returns False (not empty).
        '''
        
        # return reference
        is_empty_OUT = True
        
        # declare variables
        me = "is_form_empty"
        my_logger_name = ""
        debug_message = ""
        my_cleaned_data = None
        input_counter = -1
        current_key = None
        current_value = None
        is_value_empty = False
        
        # set logger name.
        if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
        
            # got one - use it.
            my_logger_name = logger_name_IN
        
        else:
        
            # not set.  Use default.
            my_logger_name = cls.LOGGER_NAME
        
        #-- END check to see if loger name passed in. --#
        
        # got a form?
        if ( form_IN is not None ):
        
            # get cleaned data.
            my_cleaned_data = form_IN.cleaned_data
            
            # loop over keys
            input_counter = 0
            is_empty_OUT = True
            for current_key in six.iterkeys( my_cleaned_data ):
            
                # increment counter
                input_counter += 1
    
                # get value.
                current_value = my_cleaned_data.get( current_key, cls.IAMEMPTY )
                
                debug_message = "input " + str( input_counter ) + ": key = " + str( current_key ) + "; value = \"" + str( current_value ) + "\" ( class = \"" + str( current_value.__class__ ) + "\" )"
                LoggingHelper.output_debug( debug_message, method_IN = me, logger_name_IN = my_logger_name )
                
                # empty?
                is_value_empty = cls.is_value_empty( current_value )
                if ( is_value_empty == False ):
                
                    # value is not empty, so form is not empty.
                    is_empty_OUT = False
                    
                #-- END check to see if value is empty --#

            #-- END loop over keys in data dictionary --#
            
        else:
        
            # no form passed in.  I'd call that empty...
            is_empty_OUT = True
        
        #-- END check to see if form passed in. --#

        return is_empty_OUT
        
    #-- END method is_form_empty() --#


    @classmethod
    def is_value_empty( cls, value_IN, logger_name_IN = "", *args, **kwargs ):
        
        """
        Looks at value passed in, decides if it is empty.  Returns True if
            empty, False if not.
        """
    
        # return reference
        is_empty_OUT = True
        
        # declare variables
        me = "is_value_empty"
        my_logger_name = ""
        debug_message = ""
        current_value = None
    
        # set logger name.
        if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
        
            # got one - use it.
            my_logger_name = logger_name_IN
        
        else:
        
            # not set.  Use default.
            my_logger_name = cls.LOGGER_NAME
        
        #-- END check to see if loger name passed in. --#
        
        # get value.
        current_value = value_IN
        
        debug_message = "value = \"" + str( current_value ) + "\" ( class = \"" + str( current_value.__class__ ) + "\" )"
        LoggingHelper.output_debug( debug_message, method_IN = me, logger_name_IN = my_logger_name )
        
        # empty?
        is_empty_OUT = True
        if ( current_value is not None ):
            
            # got a QuerySet?
            if ( isinstance( current_value, QuerySet ) == True ):
                
                # yes.  anything in it?
                if ( current_value.count() > 0 ):
                
                    is_empty_OUT = False
                    
                    debug_message = "QuerySet IS NOT empty."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
            
                else:
                
                    debug_message = "QuerySet is EMPTY."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                
                #-- END check to see if anything in list. --#

            elif ( isinstance( current_value, list ) == True ):
                
                # yes.  Is there anything in list?
                if ( len( current_value ) > 0 ):
                        
                    is_empty_OUT = False
                        
                    debug_message = "LIST IS NOT empty."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )

                else:
                        
                    debug_message = "LIST is EMPTY."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                        
                #-- END check to see if anything in list. --#
                    
            else:
                
                # not list - probably a string.
                if ( ( current_value != "" ) and ( current_value != cls.IAMEMPTY ) ):
                    
                    # not an empty string.
                    is_empty_OUT = False
                    
                    debug_message = "STRING IS NOT empty."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )

                else:
                    
                    debug_message = "STRING is EMPTY."
                    LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                    
                #-- END check to see if empty string, or set to cls.IAMEMPTY --#
                
            #-- END check to see if list. --#
        
        else:
        
            # empty.
            debug_message = "Value is None, and so EMPTY."
            LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
            is_empty_OUT = True
        
        #-- END check to see if empty. --#
        
        return is_empty_OUT
        
    #-- END method is_value_empty() --#

#-- END class DjangoFormHelper --#