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
    

    BS_CLASS_TAG = "Tag"
    BS_CLASS_NAVIGABLE_STRING = "NavigableString"


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
                if ( current_class_name == self.BC_CLASS_NAVIGABLE_STRING ):
                
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
    
    #-- END method bs_get_child_text() --#


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
            is_navigable_text_OUT = self.bs_is_instance_of_class( instance_IN, self.BS_CLASS_NAVIGABLE_TEXT )
            
        #-- END check to see if instance passed in --#
        
        return is_navigable_text_OUT
    
    #-- END method bs_is_navigable_text() --#


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