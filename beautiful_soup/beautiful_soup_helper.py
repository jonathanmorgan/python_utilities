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

# HTML parsing
from bs4 import BeautifulSoup

# SAX parser utilities
from xml.sax import saxutils

#================================================================================
# BeautifulSoupHelper class
#================================================================================

# define BeautifulSoupHelper class.
class BeautifulSoupHelper( object ):

    '''
    This class is a helper for Crawling and processing files.
    '''

    #============================================================================
    # Constants-ish
    #============================================================================
    

    # BeautifulSoup classes
    BS_CLASS_COMMENT = "Comment"
    BS_CLASS_NAVIGABLE_STRING = "NavigableString"
    BS_CLASS_TAG = "Tag"
    
    # element name constants.
    BS_ELEMENT_NAME_COMMENT = BS_CLASS_COMMENT
    BS_ELEMENT_NAME_TEXT = BS_CLASS_NAVIGABLE_STRING

    # HTML parsers
    BS_PARSER_HTML5LIB = "html5lib"


    #============================================================================
    # Instance methods
    #============================================================================


    def bs_get_child_text( self, tag_IN, separator_IN = " " ):
    
        '''
        Accepts a tag, gets all text that is a direct child of tag passed in
           (but not of nested elements), concatenates it, and returns it.
           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        text_OUT = ""
        
        # declare variables
        bs_current_element = None
        current_class_name = ""
        
        
        # got a tag?
        if ( tag_IN ):
        
            # loop over contents of that parent tag, looking for text (not white-space).
            for bs_current_element in tag_IN:
            
                # first, see what type of class we have.  Only need to deal with tags.
                current_class_name = bs_current_element.__class__.__name__
                
                # print( "<<< current_class_name: " + current_class_name )
                
                # got a tag?
                if ( current_class_name == self.BS_CLASS_NAVIGABLE_STRING ):
                
                    # get current string value
                    current_string = bs_current_element.string
                    
                    # trim off any white space
                    current_string = current_string.strip()

                    # anything left?
                    if ( current_string != "" ):
                    
                        # append value to pub_date string
                        text_OUT += current_string
                        
                    #-- END check to see if anything in current string.
                    
                #-- END check to see if NavigableString --#
                
            #-- END loop over elements inside div that contains paper and pub-date. --#

        #-- END check to see if tag passed in --#
        
        return text_OUT
    
    #-- END method bs_get_child_text() --#


    def bs_get_cleaned_direct_child_text( self, tag_IN, separator_IN = "" ):
    
        '''
        Accepts a tag, gets all text that is a direct child of tag passed in
           (but not of nested elements), concatenates it, and returns it.
           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        text_OUT = ""
        
        # declare variables
        bs_current_element = None
        current_class_name = ""
        
        
        # got a tag?
        if ( tag_IN ):
        
            # Retrieve all text directly below the element passed in, not 
            #    including a recursive path through children of children, etc.
            text_OUT = separator_IN.join( tag_IN.findAll( text = True, recursive = False ) )
            
            # strip the result.
            text_OUT = text_OUT.strip()

        #-- END check to see if tag passed in --#
        
        return text_OUT
    
    #-- END method bs_get_cleaned_direct_child_text() --#


    def bs_get_element_name( self, instance_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If instance of NavigableString, returns
            self.BS_ELEMENT_NAME_TEXT.  Otherwise, returns instance_IN.name.  
           
        Preconditions: None
        
        Postconditions: None.
        '''
    
        # return reference
        name_OUT = ""
                
        # declare variables
        
        is_tag = ""
        
        # Got anything passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):

            # is the instance a tag?
            is_tag = self.bs_is_tag( instance_IN )
            if ( is_tag == True ):
            
                # yes - get name of element.
                name_OUT = instance_IN.name

            else:
            
                # no.  What is it?
                is_text = self.bs_is_navigable_string( instance_IN )
                is_comment = self.bs_is_comment( instance_IN )

                if ( is_text == True ):
                
                    # yes - say name is text.
                    name_OUT = self.BS_ELEMENT_NAME_TEXT
                    
                elif ( is_comment == True ):
                
                    # yes - say name is text.
                    name_OUT = self.BS_ELEMENT_NAME_COMMENT
                    
                #-- END check to see what non-Tag object we have --#
                
            #-- END check to see if navigable tag. --#
            
        #-- END check to make sure instance_IN is not None --#
        
        return name_OUT
    
    #-- END method bs_get_element_name() --#


    def bs_is_comment( self, instance_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If it is an instance of Comment, returns
            true.  If not, returns false.
           
        Preconditions: None
        
        Postconditions: If element passed in is an instance of Comment, returns true.  If not, returns false.
        '''
    
        # return reference
        is_class_OUT = False
                
        # got an element?
        if ( instance_IN ):
        
            # check if it is instance of class.
            is_class_OUT = self.bs_is_instance_of_class( instance_IN, self.BS_CLASS_COMMENT )
            
        #-- END check to see if instance passed in --#
        
        return is_class_OUT
    
    #-- END method bs_is_comment() --#
    
    
    def bs_is_instance_of_class( self, instance_IN, class_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If it is an instance of Tag, returns
            true.  If not, returns false.
           
        Preconditions: None
        
        Postconditions: If element passed in is an instance of Tag, returns true.  If not, returns false.
        '''
    
        # return reference
        is_member_OUT = False
                
        # declare variables
        current_class_name = ""
        
        
        # got an instance and a class?
        if ( ( instance_IN ) and ( class_IN ) ):
        
            # get class name.
            current_class_name = instance_IN.__class__.__name__
                
            # print( "<<< current_class_name: " + current_class_name )
                
            # is instance's class name same as class name passed in?
            if ( current_class_name == class_IN ):
            
                # same.  return True.
                is_member_OUT = True
                
            else:
            
                # not the same.  return False.
                is_member_OUT = False
                
            #-- END check to see if same class --#

        #-- END check to see if required data passed in --#
        
        return is_member_OUT
    
    #-- END method bs_is_instance_of_class() --#


    def bs_is_navigable_text( self, instance_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If it is an instance of NavigableText,
           returns true.  If not, returns false.
           
        Preconditions: None
        
        Postconditions: If element passed in is an instance of NavigableText, returns true.  If not, returns false.
        '''
    
        # return reference
        is_navigable_text_OUT = False
                
        # got an element?
        if ( instance_IN ):
        
            # get class name.
            is_navigable_text_OUT = self.bs_is_navigable_string( instance_IN )
            
        #-- END check to see if instance passed in --#
        
        return is_navigable_text_OUT
    
    #-- END method bs_is_navigable_text() --#


    def bs_is_navigable_string( self, instance_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If it is an instance of NavigableText,
           returns true.  If not, returns false.
           
        Preconditions: None
        
        Postconditions: If element passed in is an instance of NavigableText, returns true.  If not, returns false.
        '''
    
        # return reference
        is_navigable_text_OUT = False
                
        # got an element?
        if ( instance_IN ):
        
            # get class name.
            is_navigable_text_OUT = self.bs_is_instance_of_class( instance_IN, self.BS_CLASS_NAVIGABLE_STRING )
            
        #-- END check to see if instance passed in --#
        
        return is_navigable_text_OUT
    
    #-- END method bs_is_navigable_string() --#


    def bs_is_tag( self, instance_IN ):
    
        '''
        Accepts a BeautifulSoup object.  If it is an instance of Tag, returns
            true.  If not, returns false.
           
        Preconditions: None
        
        Postconditions: If element passed in is an instance of Tag, returns true.  If not, returns false.
        '''
    
        # return reference
        is_tag_OUT = False
                
        # got an element?
        if ( instance_IN ):
        
            # get class name.
            is_tag_OUT = self.bs_is_instance_of_class( instance_IN, self.BS_CLASS_TAG )
            
        #-- END check to see if instance passed in --#
        
        return is_tag_OUT
    
    #-- END method bs_is_tag() --#
    
    
    def convert_html_entities( self, string_IN = "" ):
        
        # return reference
        string_OUT = ""
        
        # store incoming string in the return reference
        string_OUT = string_IN
        
        # replace ampersands surrounded by spaces ( " &amp; " ) with "and".
        string_OUT = string_OUT.replace( " &amp; ", " and " )
        
        # then, use the SAX parser to replace others.
        string_OUT = saxutils.unescape( string_OUT )
                
        return string_OUT
    
    #-- END method convert_html_entities() --#


#-- END class BeautifulSoupHelper --#