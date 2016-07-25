# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2014 Jonathan Morgan

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

'''
Usage:

# using string test_string

# import StringHelper
from python_utilities.strings.string_helper import StringHelper

# check to see if unicode
is_unicode = StringHelper.is_unicode( test_string )

# if not unicode, convert to unicode.
if ( is_unicode == False ):

    # use convert_to_unicode method to convert.
    test_string = StringHelper.convert_to_unicode( test_string )

#-- END check to see if unicode --#

# check if there are non-ASCII characters
has_non_ascii = StringHelper.has_non_ascii_characters( test_string )

# if there are non-ASCII characters, get a map of index of each in string to the
#    character itself.
if ( has_non_ascii == True ):

    # there are non-ASCII characters.  Find specifics.
    non_ascii_char_map = StringHelper.map_non_ascii_characters( test_string )
    
    # replace "\xa0" with "<BLARG!>", all else with " ".
    repl_map = { u"\xa0" : "<BLARG!>" }
    test_fixed = StringHelper.replace_non_ascii_characters( test_string, default_replacement_IN = " ", replacement_map_IN = repl_map )

#-- END check to see if non-ASCII characters --#

'''

# Imports

# base python modules
import six # help with supporting both python 2 and 3.

# Beautiful Soup
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

# import bleach for HTML cleaning
import bleach

# import w3lib for HTML cleaning (since bleach isn't compatible with latest html5lib)
#import w3lib

# define HTMLHelper class.
class HTMLHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def filter_attributes( cls, string_IN, allowed_attrs_IN, bs_parser_IN = "", string_bs_IN = None, *args, **kwargs ):
        
        """
        filters attributes in HTML string passed in.  Accepts
           map of element names to attribute names of attributes to leave in.
           For elements in the map, removes any attributes not in the attribute
           list associated with the element.

        Example - only let <p> tags have "id" attributes:
           
           allowed_attrs = {
               'p' : [ 'id', ],
           }
           cleaned_string = HTMLHelper.filter_attributes( html_string, allowed_attrs )
        """
    
        # return reference
        string_OUT = ""
        
        # declare variables
        string_bs = None
        allowed_tags = None
        tag_name = ""
        allowed_attribute_list = None
        tag_list_bs = None
        current_tag = None
        attribute_dict = None
        attr_name = ""
        attr_value = ""
        
        # String passed in?
        if ( ( string_IN is not None ) and ( string_IN != "" ) ):

            # yes - have we been asked to white list certain tags and attributes?
            if ( ( allowed_attrs is not None ) and ( len( allowed_attrs ) > 0 ) ):
            
                # use Beautiful Soup to filter attributes.
                
                # already BeautifulSoup-ed?
                if ( string_bs_IN is not None ):
                
                    # yes.  Use it.
                    string_bs = string_bs_IN
                
                else:

                    # particular parser requested?
                    if ( ( bs_parser_IN is not None ) and ( bs_parser_IN != "" ) ):
    
                        # yes.  Request it.
                        string_bs = BeautifulSoup( string_IN, bs_parser_IN )
    
                    else:
    
                        # no.  Let BeautfiulSoup pick.
                        string_bs = BeautifulSoup( string_IN )
    
                    #-- END check to see if specific parser requested. --#
                    
                #-- END check to see if BeautifulSoup instance with HTML already in it passed in --#
                
                # ! TODO - loop over elements in the dictionary.
                for tag_name, allowed_attribute_list in six.iteritems( allowed_attrs ):
                
                    # get all the instances of the current tag.
                    tag_list_bs = string_bs.find_all( tag_name )
                    
                    # loop over tag instances.
                    for current_tag in tag_list_bs:
                    
                        # get attributes.
                        attribute_dict = current_tag.attrs
                        
                        # loop over list of keys in the attribute list.
                        attr_name_list = list( attribute_dict.keys() )
                        for attr_name in attr_name_list:
                        
                            # is attribute name in the allowed_attribute_list?
                            if ( attr_name not in allowed_attribute_list ):
                            
                                # no.  Remove the attribute.
                                attribute_dict.pop( attr_name )
                            
                            #-- END check to see if attribute in allowed list. --#
                        
                        #-- END loop over attributes. --#
                    
                    #-- END loop over tag instances --#
                
                #-- END loop over tag to allowed attributes map --#
                
                # convert back to string.
                string_OUT = str( string_bs )
                
            else:
            
                # no attribute filters defined, so just return what was passed
                #     in.
                string_OUT = string_IN
                
            #-- END check to see if we have attributes to filter. --#
            
        #-- END check to make sure we have a string passed in. --#

        return string_OUT
    
    #-- END filter_attributes() function --#


    @classmethod
    def remove_html( cls, string_IN, allowed_tags_IN = [], allowed_attrs_IN = {}, bs_parser_IN = "", string_bs_IN = None, *args, **kwargs ):
        
        """
        strips out HTML from string.  Accepts list of attributes to leave in, and
           map of element names to attribute names of attributes to leave in.
           Defaults to not leaving in any tags, or, if tags are specified,
           removing all attributes.

        Example - leave in <p> tags, and let <p> tags have "id" attributes:
           
           allowed_tags = [ 'p', ]
           allowed_attrs = {
               'p' : [ 'id', ],
           }
           cleaned_string = HTMLHelper.remove_html( html_string, allowed_tags, allowed_attrs )
        """
    
        # return reference
        string_OUT = ""
        
        # declare variables
        string_bs = None
        text_list = None
        allowed_tags = None
        
        # String passed in?
        if ( ( string_IN is not None ) and ( string_IN != "" ) ):

            # yes - have we been asked to white list certain tags and attributes?
            if ( len( allowed_tags_IN ) > 0 ):
            
                # yes - call the bleach.clean() method.
                string_OUT = bleach.clean( string_IN, allowed_tags_IN, allowed_attrs_IN, strip = True )
                
                '''
                # use w3lib
                allowed_tags = tuple( allowed_tags_IN )
                string_OUT = w3lib.html.remove_tags( string_IN, keep = allowed_tags )
                
                # filter attributes?
                if ( ( allowed_attrs_IN is not None ) and ( len( allowed_attrs_IN ) > 0 ) ):

                    string_OUT = cls.filter_attributes( string_OUT, allowed_attrs_IN, bs_parser_IN = bs_parser_IN, string_bs_IN = string_bs_IN )

                #-- END check to see if we need to filter attributes --#
                '''
                
            else:
            
                # no - use Beautiful Soup to strip HTML.

                # already BeautifulSoup-ed?
                if ( string_bs_IN is not None ):
                
                    # yes.  Use it.
                    string_bs = string_bs_IN
                
                else:

                    # particular parser requested?
                    if ( ( bs_parser_IN is not None ) and ( bs_parser_IN != "" ) ):
    
                        # yes.  Request it.
                        string_bs = BeautifulSoup( string_IN, bs_parser_IN )
    
                    else:
    
                        # no.  Let BeautfiulSoup pick.
                        string_bs = BeautifulSoup( string_IN, allowed_attrs_IN )
    
                    #-- END check to see if specific parser requested. --#
                    
                #-- END check to see if BeautifulSoup instance with HTML already in it passed in --#
                
                # parse out all text
                #text_list = string_bs.findAll( text = True )
                
                # OR
                text_list = string_bs.get_text( " ", strip = True )
                
                # join text fragments together.
                string_OUT = ''.join( text_list )
            
            #-- END check to see if we have to leave any HTML in. --#
            
        #-- END check to make sure we have a string passed in. --#

        return string_OUT
    
    #-- END remove_html() function --#


#-- END class HTMLHelper --#