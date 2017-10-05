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

# import HTMLHelper
from python_utilities.strings.html_helper import HTMLHelper

html_string = "<p id=\"1\" class=\"very\">test</p>"
allowed_attrs = {
   'p' : [ 'id', ],
}
cleaned_string = HTMLHelper.filter_attributes( html_string, allowed_attrs )

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
import w3lib.html

# define HTMLHelper class.
class HTMLHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    
    # FILTER_METHODS
    HTML_FILTER_LIBRARY_BLEACH = "bleach"
    HTML_FILTER_LIBRARY_W3LIB = "w3lib"


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
           
           html_string = "<p id=\"1\" class=\"very\">test</p>"
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
            if ( ( allowed_attrs_IN is not None ) and ( len( allowed_attrs_IN ) > 0 ) ):
            
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
                        string_bs = BeautifulSoup( string_IN, "html.parser" )
    
                    #-- END check to see if specific parser requested. --#
                    
                #-- END check to see if BeautifulSoup instance with HTML already in it passed in --#
                
                # ! TODO - loop over elements in the dictionary.
                for tag_name, allowed_attribute_list in six.iteritems( allowed_attrs_IN ):
                
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
    def remove_html( cls, 
                     string_IN,
                     allowed_tags_IN = [],
                     allowed_attrs_IN = {},
                     bs_parser_IN = "",
                     string_bs_IN = None,
                     remove_method_IN = HTML_FILTER_LIBRARY_W3LIB,
                     *args,
                     **kwargs ):
        
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
        work_string = ""
        
        # String passed in?
        if ( ( string_IN is not None ) and ( string_IN != "" ) ):

            # yes - have we been asked to white list certain tags and attributes?
            if ( len( allowed_tags_IN ) > 0 ):
            
                # what remove method do we use?
                if ( remove_method_IN == cls.HTML_FILTER_LIBRARY_BLEACH ):
            
                    # yes - call the bleach.clean() method.
                    string_OUT = bleach.clean( string_IN, allowed_tags_IN, allowed_attrs_IN, strip = True )
                    
                elif ( remove_method_IN == cls.HTML_FILTER_LIBRARY_W3LIB ):
                
                    # set work string
                    work_string = string_IN
                
                    # filter attributes?
                    if ( ( allowed_attrs_IN is not None ) and ( len( allowed_attrs_IN ) > 0 ) ):
    
                        work_string = cls.filter_attributes( work_string, allowed_attrs_IN, bs_parser_IN = bs_parser_IN, string_bs_IN = string_bs_IN )
    
                    #-- END check to see if we need to filter attributes --#
    
                    # use w3lib
                    allowed_tags = tuple( allowed_tags_IN )
                    work_string = w3lib.html.remove_tags( work_string, keep = allowed_tags )
                    
                    # store work_string in string_OUT
                    string_OUT = work_string
                    
                else:
                
                    # default - call the bleach.clean() method (for now).
                    string_OUT = bleach.clean( string_IN, allowed_tags_IN, allowed_attrs_IN, strip = True )                    
                    
                #-- END check of which remove method to use. --#
                
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