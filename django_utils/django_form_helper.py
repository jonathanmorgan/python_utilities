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

# python 3 support:
from __future__ import unicode_literals

# import six for Python 2 and 3 compatibility.
import six

# django imports
from django.db.models.query import QuerySet
from django import forms

# python_utilities includes.
from python_utilities.logging.logging_helper import LoggingHelper

class DjangoFormHelper( LoggingHelper ):
    

    #============================================================================
    # ! ==> constants-ish
    #============================================================================


    LOGGER_NAME = "python_utilities.django_utils.DjangoFormHelper"
    IAMEMPTY = "IAMEMPTY"


    #============================================================================
    # ! ==> class methods
    #============================================================================


    @classmethod
    def is_form_empty( cls, form_IN, logger_name_IN = "", *args, **kwargs ):
        
        '''
        Accepts django Form or ModelForm in form_IN.  Goes through the fields in
            the form and checks to see if any has been populated.  If not,
            returns True (it is empty!).  If there is a value in any of them,
            returns False (not empty).
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
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


    @classmethod
    def data_to_html_as_hidden_inputs( cls, form_IN, logger_name_IN = "", *args, **kwargs ):

        '''
        Accepts django Form or ModelForm in form_IN.  Goes through the fields in
            the form and for each, creates HTML string of a hidden input that
            contains the value.  If no data, returns empty string.  If error
            returns None.
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        html_OUT = ""

        # declare variables
        me = "data_to_html_as_hidden_inputs"
        my_logger_name = ""
        debug_message = ""
        my_cleaned_data = None
        input_counter = -1
        current_key = None
        current_value = None
        current_value_string = ""
        input_html = ""
        is_value_empty = False
        value_list = None
        current_instance = None
        current_id = -1
        
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
            for current_key in six.iterkeys( my_cleaned_data ):
            
                # increment counter
                input_counter += 1
    
                # get value.
                current_value = my_cleaned_data.get( current_key, cls.IAMEMPTY )
                
                debug_message = "input " + str( input_counter ) + ": key = " + str( current_key ) + "; value = \"" + str( current_value ) + "\" ( class = \"" + str( current_value.__class__ ) + "\" )"
                LoggingHelper.output_debug( debug_message, method_IN = me, logger_name_IN = my_logger_name )
                
                # default current_value_string to current_value
                current_value_string = current_value
                
                # empty?
                is_value_empty = cls.is_value_empty( current_value )
                if ( is_value_empty == True ):
                
                    # value is empty.  Set to empty string.
                    current_value_string = ""
                
                else:
                
                    # not empty - convert value to string if needed.
                    if ( current_value is not None ):
                    
                        # got a QuerySet?
                        if ( isinstance( current_value, QuerySet ) == True ):
                            
                            # yes.  anything in it?
                            if ( current_value.count() > 0 ):
    
                                debug_message = "QuerySet IS NOT empty."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                
                                # ! convert QuerySet to list of IDs?
                                value_list = []
                                for current_instance in current_value:
                                
                                    # add string ID value to list.
                                    current_id = current_instance.id
                                    value_list.append( str( current_id ) )
                                    
                                #-- END loop over instances in QuerySet --#
                                
                                # and, combine into a comma-delimited string list
                                current_value_string = ",".join( value_list )
                        
                            else:
                            
                                debug_message = "QuerySet is EMPTY."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                
                                # set value string to ""
                                current_value_string = ""
                            
                            #-- END check to see if anything in QuerySet. --#
            
                        elif ( isinstance( current_value, list ) == True ):
                            
                            # yes.  Is there anything in list?
                            if ( len( current_value ) > 0 ):
                                    
                                debug_message = "LIST IS NOT empty."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                
                                # combine into a comma-delimited string list.
                                current_value_string = ",".join( current_value )
            
                            else:
                                    
                                debug_message = "LIST is EMPTY."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                    
                                # set value string to ""
                                current_value_string = ""
                            
                            #-- END check to see if anything in list. --#
                                
                        else:
                            
                            # not list - probably a string.
                            if ( ( current_value != "" ) and ( current_value != cls.IAMEMPTY ) ):
                                
                                debug_message = "STRING IS NOT empty."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                
                                # just use the value as-is
                                current_value_string = current_value
            
                            else:
                                
                                debug_message = "STRING is EMPTY."
                                LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                                
                                # set value string to ""
                                current_value_string = ""                            
                                
                            #-- END check to see if empty string, or set to cls.IAMEMPTY --#
                            
                        #-- END check to see if list. --#
                    
                    else:
                    
                        # empty.
                        debug_message = "Value is None, and so EMPTY."
                        LoggingHelper.output_debug( debug_message, method_IN = me, indent_with_IN = "====> ", logger_name_IN = my_logger_name )
                        
                        # set value string to ""
                        current_value_string = ""                            
                    
                    #-- END check to see if None. --#
                
                #-- END check to see if value is empty...else not empty --#

                # render <input> HTML
                input_html = "<input type=\"hidden\" name=\"" + str( current_key ) +  "\" value=\"" + str( current_value_string ) + "\" />"

                # add to HTML
                html_OUT += input_html

            #-- END loop over keys in data dictionary --#
            
        else:
        
            # no form passed in.  No HTML returned.
            html_OUT = ""
        
        #-- END check to see if form passed in. --#

        return html_OUT

    #-- END class method data_to_html_as_hidden_inputs() --#


    #============================================================================
    # ! ==> Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # always call parent's __init__()
        super( DjangoFormHelper, self ).__init__()
        
        # initialize variables
        self.form = None
        self.set_logger_name( self.LOGGER_NAME )

    #-- END method __init__() --#


    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def get_form( self ):
    
        # return reference
        value_OUT = None
        
        # get value
        value_OUT = self.form
                
        return value_OUT
    
    #-- END method get_form --#

    
    def is_my_form_empty( self, *args, **kwargs ):

        '''
        Uses nested django Form or ModelForm.  Goes through the fields in
            the form and checks to see if any has been populated.  If not,
            returns True (it is empty!).  If there is a value in any of them,
            returns False (not empty).
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        is_empty_OUT = ""

        # declare variables
        me = "is_my_form_empty"
        my_logger_name = ""
        my_form = None
        
        # get logger name and form.
        my_form = self.get_form()
        my_logger_name = self.get_logger_name()
        
        # call class method.
        html_OUT = self.is_form_empty( my_form, logger_name_IN = my_logger_name )
        
        return html_OUT

    #-- END method to_html_as_hidden_inputs() --#


    def is_my_value_empty( self, *args, **kwargs ):

        '''
        Looks at value passed in, decides if it is empty.  Returns True if
            empty, False if not.
        '''
        
        # return reference
        html_OUT = ""

        # declare variables
        me = "is_my_value_empty"
        my_logger_name = ""
        my_form = None
        
        # get logger name and form.
        my_form = self.get_form()
        my_logger_name = self.get_logger_name()
        
        # call class method.
        html_OUT = self.is_value_empty( my_form, logger_name_IN = my_logger_name )
        
        return html_OUT

    #-- END method to_html_as_hidden_inputs() --#


    def set_form( self, instance_IN ):
        
        '''
        Accepts form.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # store instance.
        self.form = instance_IN
        
        # return it.
        value_OUT = self.form
        
        return value_OUT
        
    #-- END method set_form() --#


    def to_html_as_hidden_inputs( self, *args, **kwargs ):

        '''
        Goes through the fields in the form and for each, creates HTML string of
            a hidden input that contains the value.  If no data, returns empty
            string.  If error returns None.
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        html_OUT = ""

        # declare variables
        me = "to_html_as_hidden_inputs"
        my_logger_name = ""
        my_form = None
        
        # get logger name and form.
        my_form = self.get_form()
        my_logger_name = self.get_logger_name()
        
        # call class method.
        html_OUT = self.data_to_html_as_hidden_inputs( my_form, logger_name_IN = my_logger_name )
        
        return html_OUT

    #-- END method to_html_as_hidden_inputs() --#


#-- END class DjangoFormHelper --#


class FormParent( forms.Form ):


    #--------------------------------------------------------------------------#
    # instance methods
    #--------------------------------------------------------------------------#
    
        
    def am_i_empty( self, *args, **kwargs ):
        
        '''
        Goes through the fields in the form and checks to see if any has been
            populated.  If not, returns True (it is empty!).  If there is a
            value in any of them, returns False (not empty).

        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        is_empty_OUT = True
        
        # declare variables
        me = "am_i_empty"
        my_logger_name = "python_utilities.django_utils.django_form_helper.FormParent"
        debug_message = ""
        
        # use DjangoFormHelper method
        is_empty_OUT = DjangoFormHelper.is_form_empty( self )

        return is_empty_OUT

    #-- END method am_i_empty() --#
    

    def to_html_as_hidden_inputs( self, *args, **kwargs ):
        
        '''
        Goes through the fields in the form and for each, creates HTML string of
            a hidden input that contains the value.  If no data, returns empty
            string.  If error returns None.
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        html_OUT = ""
        
        # declare variables
        me = "to_html_as_hidden_inputs"
        my_logger_name = "python_utilities.django_utils.django_form_helper.FormParent"
        debug_message = ""
        
        # use DjangoFormHelper method
        html_OUT = DjangoFormHelper.data_to_html_as_hidden_inputs( self, logger_name_IN = my_logger_name )

        return html_OUT

    #-- END method to_html_as_hidden_inputs() --#
    

#-- END Form class FormParent --#


class ModelFormParent( forms.ModelForm ):


    #--------------------------------------------------------------------------#
    # instance methods
    #--------------------------------------------------------------------------#
    
        
    def am_i_empty( self, *args, **kwargs ):
        
        '''
        Goes through the fields in the form and checks to see if any has been
            populated.  If not, returns True (it is empty!).  If there is a
            value in any of them, returns False (not empty).

        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        is_empty_OUT = True
        
        # declare variables
        me = "am_i_empty"
        my_logger_name = "python_utilities.django_utils.django_form_helper.ModelFormParent"
        debug_message = ""
        
        # use DjangoFormHelper method
        is_empty_OUT = DjangoFormHelper.is_form_empty( self )

        return is_empty_OUT

    #-- END method am_i_empty() --#
    

    def to_html_as_hidden_inputs( self, *args, **kwargs ):
        
        '''
        Goes through the fields in the form and for each, creates HTML string of
            a hidden input that contains the value.  If no data, returns empty
            string.  If error returns None.
            
        Preconditions: Must be called after is_valid() is called on the form.
            If not, there will not be any "cleaned_data".
        '''
        
        # return reference
        html_OUT = ""
        
        # declare variables
        me = "to_html_as_hidden_inputs"
        my_logger_name = "python_utilities.django_utils.django_form_helper.ModelFormParent"
        debug_message = ""
        
        # use DjangoFormHelper method
        html_OUT = DjangoFormHelper.data_to_html_as_hidden_inputs( self, logger_name_IN = my_logger_name )

        return html_OUT

    #-- END method to_html_as_hidden_inputs() --#
    

#-- END Form class ModelFormParent --#

