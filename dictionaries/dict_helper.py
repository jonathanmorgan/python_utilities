# start to support python 3:
from __future__ import unicode_literals

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

#================================================================================
# imports
#================================================================================

# standard library
import decimal

import six # help with supporting both python 2 and 3.

# python_utilities.lists.list_helper - ListHelper
from python_utilities.lists.list_helper import ListHelper


#================================================================================
# class definitions
#================================================================================


# define DictHelper class.
class DictHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    STATUS_ERROR_PREFIX = "Error: "


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def get_dict_value( cls, dict_IN, name_IN, default_IN = None ):
    
        '''
        Accepts dictionary, name, and optional default value (if no default
           provided, default is None).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name.
           
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
        if ( cls.is_dict( dict_IN ) == True ):
        
            # got dictionary.  Got name?
            if ( name_IN ):
            
                # see if name in dictionary.
                if ( name_IN in dict_IN ):
                
                    # name is in dictionary.  Get value, return it.
                    value_OUT = dict_IN.get( name_IN, default_IN )
                
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


    @classmethod
    def get_dict_value_as_decimal( cls, dict_IN, name_IN, default_IN = decimal.Decimal( -1 ) ):
    
        '''
        Accepts dictionary, name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a decimal.Decimal instance
           through call to decimal.Decimal().
           
        Parameters:
        - dict_IN - dictionary we are looking in.
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to -1) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to int(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # first, get value.
        value_OUT = cls.get_dict_value( dict_IN, name_IN, default_IN )
        
        # convert to int unless value is None.
        if ( value_OUT != None ):

            # value is not None.
            value_OUT = decimal.Decimal( value_OUT )
            
        #-- END check to see if default was None --#
        
        return value_OUT
    
    #-- END function get_dict_value_as_decimal --#


    @classmethod
    def get_dict_value_as_float( cls, dict_IN, name_IN, default_IN = float( -1 ) ):
    
        '''
        Accepts dictionary, name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a
           float through call to float().
           
        Parameters:
        - dict_IN - dictionary we are looking in.
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to int(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # first, get value.
        value_OUT = cls.get_dict_value( dict_IN, name_IN, default_IN )
        
        # convert to float unless value is None.
        if ( value_OUT != None ):

            # value is not None.
            value_OUT = float( value_OUT )
            
        #-- END check to see if default was None --#
        
        return value_OUT
    
    #-- END function get_dict_value_as_float --#



    @classmethod
    def get_dict_value_as_int( cls, dict_IN, name_IN, default_IN = -1 ):
    
        '''
        Accepts dictionary, name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to an
           integer through call to int().
           
        Parameters:
        - dict_IN - dictionary we are looking in.
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to int(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # first, get value.
        value_OUT = cls.get_dict_value( dict_IN, name_IN, default_IN )
        
        # convert to int unless value is None.
        if ( value_OUT != None ):

            # value is not None.
            value_OUT = int( value_OUT )
            
        #-- END check to see if default was None --#
        
        return value_OUT
    
    #-- END function get_dict_value_as_int --#


    @classmethod
    def get_dict_value_as_list( cls, dict_IN, name_IN, default_IN = [], delimiter_IN = ',' ):
        
        # return reference
        list_OUT = []
        
        # declare variables
        me = "get_dict_value_as_list"
        list_param_value = ""
        working_list = []
        current_value = ""
        current_value_clean = ""
        missing_string = "get_list_param-missing"
        
        # first, try getting raw param, see if it is already a list.
        
        # get raw value
        list_param_value = cls.get_dict_value( dict_IN, name_IN, None )
        
        # check if list
        if ( isinstance( list_param_value, list ) == True ):
        
            # already a list - return it.
            list_OUT = list_param_value
            
        elif ( ( isinstance( list_param_value, six.string_types ) == True ) and ( list_param_value == "" ) ):
        
            # empty string - return empty list
            list_OUT = []
        
        else:
        
            # not a list.  assume string.
        
            # get list param's original value
            list_param_value = cls.get_dict_value_as_str( dict_IN, name_IN, missing_string )
            
            # print( "====> list param value: " + list_param_value )
            
            # got a value?
            if ( ( list_param_value != "" ) and ( list_param_value != missing_string ) ):
            
                # yes - use ListHelper to convert to list.
                list_OUT = ListHelper.get_value_as_list( list_param_value, delimiter_IN )
            
            elif list_param_value == "":
            
                # return empty list.
                list_OUT = []
                
            elif list_param_value == missing_string:
            
                # return default
                list_OUT = default_IN
                
            else:
            
                # not sure how we got here - return default.
                list_OUT = default_IN
            
            #-- END check to see what was in value. --#
            
        #-- END check to see if already a list --#
        
        return list_OUT
        
    #-- END method get_dict_value_as_list() --#
    

    @classmethod
    def get_dict_value_as_str( cls, dict_IN, name_IN, default_IN = "" ):
    
        '''
        Accepts dictionary, name, and optional default value (if no default
           provided, default is "").  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a
           string through call to str().
           
        Parameters:
        - dict_IN - dictionary we are looking in.
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to "") - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to str(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # first, get value.
        value_OUT = cls.get_dict_value( dict_IN, name_IN, default_IN )
        
        # convert to str unless value is None.
        if ( value_OUT != None ):

            # value is not None.
            value_OUT = str( value_OUT )
            
        #-- END check to see if default was None --#
        
        return value_OUT
    
    #-- END function get_dict_value_as_str --#


    @classmethod
    def increment_decimal_dict_value( cls, dict_IN, name_IN, value_IN = decimal.Decimal( 1 ), *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as decimal.Decimal, adds value_IN to it, then
           stores and returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_value = -1
        value_to_add = -1
        
        # got dict?
        if ( cls.is_dict( dict_IN ) == True ):
        
            # yes.  Got name?
            if ( ( name_IN ) and ( name_IN != None ) ):
            
                # yes.  Retrieve value for name as decimal.Decimal.
                my_value = cls.get_dict_value_as_decimal( dict_IN, name_IN )
                
                # make sure value_IN is a decimal.Decimal.
                value_to_add = decimal.Decimal( value_IN )
                
                # add value_IN
                my_value = my_value + value_to_add
                
                # store result and set return value
                value_OUT = cls.set_dict_value( dict_IN, name_IN, my_value )
            
            else:
            
                # no name.  error - return None
                value_OUT = None
            
            #-- END check to see if name --#

        else:
        
            # error - no dict.  Return None.
            value_OUT = None
        
        #-- END check to see if dict. --#
        
        return value_OUT
        
    #-- END method increment_decimal_dict_value() --#


    @classmethod
    def increment_float_dict_value( cls, dict_IN, name_IN, value_IN = float( 1 ), *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as float, adds value_IN to it, then stores and
           returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_value = -1
        value_to_add = -1
        
        # got dict?
        if ( cls.is_dict( dict_IN ) == True ):
        
            # yes.  Got name?
            if ( ( name_IN ) and ( name_IN != None ) ):
            
                # yes.  Retrieve value for name as float.
                my_value = cls.get_dict_value_as_float( dict_IN, name_IN )
                
                # make sure value_IN is a float.
                value_to_add = float( value_IN )
                
                # add value_IN
                my_value = my_value + value_to_add
                
                # store result and set return value
                value_OUT = cls.set_dict_value( dict_IN, name_IN, my_value )
            
            else:
            
                # no name.  error - return None
                value_OUT = None
            
            #-- END check to see if name --#

        else:
        
            # error - no dict.  Return None.
            value_OUT = None
        
        #-- END check to see if dict. --#
        
        return value_OUT
        
    #-- END method increment_float_dict_value() --#


    @classmethod
    def increment_int_dict_value( cls, dict_IN, name_IN, value_IN = 1, *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as int, adds value_IN to it, then stores and
           returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        value_to_add = -1
        
        # declare variables
        my_value = -1
        
        # got dict?
        if ( cls.is_dict( dict_IN ) == True ):
        
            # yes.  Got name?
            if ( ( name_IN ) and ( name_IN != None ) ):
            
                # yes.  Retrieve value for name as int.
                my_value = cls.get_dict_value_as_int( dict_IN, name_IN )
                
                # make sure value_IN is an int.
                value_to_add = int( value_IN )
                
                # add value_IN
                my_value = my_value + value_to_add
                                
                # store result and set return value
                value_OUT = cls.set_dict_value( dict_IN, name_IN, my_value )
            
            else:
            
                # no name.  error - return None
                value_OUT = None
            
            #-- END check to see if name --#

        else:
        
            # error - no dict.  Return None.
            value_OUT = None
        
        #-- END check to see if dict. --#
        
        return value_OUT
        
    #-- END method increment_int_dict_value() --#


    @classmethod
    def is_dict( cls, dict_IN ):
    
        # return reference
        is_dict_OUT = False
        
        # check.
        if ( ( dict_IN != None ) and ( isinstance( dict_IN, dict ) == True ) ):
        
            # yes.  Return True.
            is_dict_OUT = True
        
        else:
        
            # appears not.  Return False.
            is_dict_OUT = False
        
        #-- END check to see if the thing passed in is a dict. --#
        
        return is_dict_OUT
    
    #-- END method is_dict() --#
    
    
    @classmethod
    def set_dict_value( cls, dict_IN, name_IN, value_IN ):
    
        '''
        Accepts dictionary, name, and value.  If dictionary or name missing,
           returns error message prefixed by STATUS_ERROR_PREFIX.  If dict and
           name set, places value_IN, whatever it is, in dict with name as key.
           
        Parameters:
        - dict_IN - dictionary we are looking in.
        - name_IN - name we are looking for in dictionary.
        - value_IN - value to associate in dict with name passed in.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, else an error message if problems.  To check for success, check if value_IN = value_OUT.  If not, error.
        '''
    
        # return reference
        value_OUT = None
        
        # first, make sure we have all the stuff we need.  If stuff missing, return
        #    default.
        if ( cls.is_dict( dict_IN ) == True ):
        
            # got dictionary.  Got name?
            if ( ( name_IN ) and ( name_IN != None ) ):
            
                # yup - store value.
                dict_IN[ name_IN ] = value_IN
                value_OUT = cls.get_dict_value( dict_IN, name_IN )            

            else:
            
                # no name.  Return error.
                value_OUT = cls.STATUS_ERROR_PREFIX + "No name passed in, can't set value."
            
            #-- END check to see if name. --#
        
        else:
        
            # no dictionary.  Return error.
            value_OUT = cls.STATUS_ERROR_PREFIX + "No dictionary passed in, can't set value."
            
        #-- END check to see if dictionary passed in. --#
        
        return value_OUT
    
    #-- END function set_dict_value --#


    #============================================================================
    # ! ==> Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # initialize variables
        self.m_dictionary = {}

    #-- END method __init__() --#


    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def get_dictionary( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        dict_instance = None
        
        # get m_dictionary
        value_OUT = self.m_dictionary
        
        # got anything?
        if ( value_OUT is None ):
        
            # make dictionary instance.
            dict_instance = {}
            
            # store the instance.
            self.set_dictionary( dict_instance )
            
            # get the instance.
            value_OUT = self.get_dictionary()
        
        #-- END check to see if dictionary initialized. --#
        
        return value_OUT
    
    #-- END method get_dictionary --#


    def get_value( self, name_IN, default_IN = None ):
    
        '''
        Accepts name, and optional default value (if no default
           provided, default is None).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name.
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None        
        
        # get dictionary
        my_dictionary = self.get_dictionary()

        # call corresponding class method.
        value_OUT = DictHelper.get_dict_value( my_dictionary, name_IN, default_IN )
                
        return value_OUT
    
    #-- END function get_value --#


    def get_value_as_decimal( self, name_IN, default_IN = decimal.Decimal( -1 ) ):
    
        '''
        Accepts name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a
           decimal.Decimal instance through call to decimal.Decimal().
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to decimal.Decimal, else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_value_as_decimal"
        my_dictionary = None
        
        # get dictionary
        my_dictionary = self.get_dictionary()

        # call corresponding class method.
        value_OUT = DictHelper.get_dict_value_as_decimal( my_dictionary, name_IN, default_IN )

        return value_OUT
    
    #-- END function get_value_as_decimal --#


    def get_value_as_float( self, name_IN, default_IN = float( -1 ) ):
    
        '''
        Accepts name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a
           float through call to float().
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to float, else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_value_as_float"
        my_dictionary = None
        
        # get dictionary
        my_dictionary = self.get_dictionary()

        # call corresponding class method.
        value_OUT = DictHelper.get_dict_value_as_float( my_dictionary, name_IN, default_IN )

        return value_OUT
    
    #-- END function get_value_as_float --#


    def get_value_as_int( self, name_IN, default_IN = -1 ):
    
        '''
        Accepts name, and optional default value (if no default
           provided, default is -1).  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to an
           integer through call to int().
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to None) - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in dict_IN, converted to int(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        me = "get_value_as_int"
        my_dictionary = None
        
        # get dictionary
        my_dictionary = self.get_dictionary()

        # call corresponding class method.
        value_OUT = DictHelper.get_dict_value_as_int( my_dictionary, name_IN, default_IN )

        return value_OUT
    
    #-- END function get_value_as_int --#


    def get_value_as_list( self, name_IN, default_IN = [], delimiter_IN = ',' ):
        
        # return reference
        list_OUT = []
        
        # declare variables
        me = "get_value_as_list"
        my_dictionary = None
        list_param_value = ""

        # get dictionary
        my_dictionary = self.get_dictionary()

        # call corresponding class method.
        list_OUT = DictHelper.get_dict_value_as_list( my_dictionary, name_IN, default_IN, delimiter_IN )
        
        return list_OUT
        
    #-- END method get_value_as_list() --#
    

    def get_value_as_str( self, name_IN, default_IN = "" ):
    
        '''
        Accepts name, and optional default value (if no default
           provided, default is "").  If dictionary or name missing, returns
           default.  If name not present in dictionary, returns default.  If name
           in dictionary, returns whatever is mapped to name, converted to a
           string through call to str().
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - default_IN (defaults to "") - default value to return if problem or not found in dict.
        
        Returns:
        - value_OUT - value mapped to name_IN in my_dictionary, converted to str(), else the default value if problems or if not found in dict.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None
        
        # call class method with nested dictionary.
        my_dictionary = self.get_dictionary()
        value_OUT = DictHelper.get_dict_value_as_str( my_dictionary, name_IN, default_IN )
        
        return value_OUT
    
    #-- END function get_value_as_str --#


    def increment_decimal_value( self, name_IN, value_IN = decimal.Decimal( 1 ), *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as decimal.Decimal, adds value_IN to it, then
           stores and returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None
        
        # got dict?
        my_dictionary = self.get_dictionary()
        
        # call class method.
        value_OUT = DictHelper.increment_decimal_dict_value( my_dictionary, name_IN, value_IN, *args, **kwargs )
        
        return value_OUT
        
    #-- END method increment_decimal_value() --#


    def increment_float_value( self, name_IN, value_IN = float( 1 ), *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as float, adds value_IN to it, then stores and
           returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None
        
        # got dict?
        my_dictionary = self.get_dictionary()
        
        # call class method.
        value_OUT = DictHelper.increment_float_dict_value( my_dictionary, name_IN, value_IN, *args, **kwargs )
        
        return value_OUT
        
    #-- END method increment_float_value() --#


    def increment_int_value( self, name_IN, value_IN = 1, *args, **kwargs ):
        
        '''
        Accepts name, and optional increment value.  Increment value defaults to
           1.  Retrieves value as int, adds value_IN to it, then stores and
           returns the result.  Returns None if error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None
        
        # got dict?
        my_dictionary = self.get_dictionary()
        
        # call class method.
        value_OUT = DictHelper.increment_int_dict_value( my_dictionary, name_IN, value_IN, *args, **kwargs )
        
        return value_OUT
        
    #-- END method increment_int_value() --#


    def set_dictionary( self, instance_IN ):
        
        '''
        Accepts dictionary.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_dictionary = instance_IN
        
        # return it.
        value_OUT = self.m_dictionary
        
        return value_OUT
        
    #-- END method set_dictionary() --#


    def set_value( self, name_IN, value_IN ):
    
        '''
        Accepts name, and value.  If dictionary or name missing,
           returns error message prefixed by STATUS_ERROR_PREFIX.  If dict and
           name set, places value_IN, whatever it is, in dict with name as key.
           
        Parameters:
        - name_IN - name we are looking for in dictionary.
        - value_IN - value to associate in dict with name passed in.
        
        Returns:
        - value_OUT - value mapped to name_IN in m_dictionary, else an error message if problems.  To check for success, check if value_IN = value_OUT.  If not, error.
        '''
    
        # return reference
        value_OUT = None
        
        # declare variables
        my_dictionary = None
        
        # get nested dictionary
        my_dictionary = self.m_dictionary
        
        # first, make sure we have all the stuff we need.  If stuff missing, return
        #    default.
        if ( DictHelper.is_dict( my_dictionary ) == True ):
        
            # got dictionary.  Got name?
            if ( ( name_IN ) and ( name_IN != None ) ):
            
                # yup - store value.
                my_dictionary[ name_IN ] = value_IN
                value_OUT = self.get_value( name_IN )            

            else:
            
                # no name.  Return error.
                value_OUT = DictHelper.STATUS_ERROR_PREFIX + "No name passed in, can't set value."
            
            #-- END check to see if name. --#
        
        else:
        
            # no dictionary.  Return error.
            value_OUT = DictHelper.STATUS_ERROR_PREFIX + "No dictionary passed in, can't set value."
            
        #-- END check to see if dictionary passed in. --#
        
        return value_OUT
    
    #-- END function set_value --#


#-- END class LoggingHelper --##-- END class DictHelper --#


#================================================================================
# ! functions
#================================================================================

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
    
    # call the method in DictHelper
    value_OUT = DictHelper.get_dict_value( dict_IN, name_IN, default_IN )
            
    return value_OUT

#-- END function get_dict_value --#