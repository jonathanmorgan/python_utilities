# python imports
import os
import site
import unittest

# import the things we are testing.

try:
    from python_utilities.strings.string_helper import StringHelper
except ImportError as ie:

    # get current directory path
    current_directory_path = os.path.dirname( os.path.abspath( __file__ ) )

    # add to python path
    site.addsitedir( current_directory_path )
    
    # try local import
    from string_helper import StringHelper

#-- END attempt to import StringHelper --#

try:
    from python_utilities.strings.html_helper import HTMLHelper
except ImportError as ie:

    # get current directory path
    current_directory_path = os.path.dirname( os.path.abspath( __file__ ) )

    # add to python path
    site.addsitedir( current_directory_path )
    
    # try local import
    from html_helper import HTMLHelper

#-- END attempt to import HTMLHelper --#

class TestStringHelper(unittest.TestCase):

    def test_replace_white_space( self ):

        # declare variables
        start_string = ""
        test_string = ""
        expected_string = ""
        
        # initialize
        start_string = "one bird   two  shoes     and a cat"
        expected_string = "one bird two shoes and a cat"
        
        # do work
        test_string = StringHelper.replace_white_space( start_string, replace_with_IN = " " )
        
        # and the assert
        self.assertEqual( test_string, expected_string )
        
    #-- END method test_replace_white_space() --#

#-- END unittest class TestStringHelper --#


class TestHTMLHelper(unittest.TestCase):
    
    # shared variables
    TEST_HTML_FRAGMENT_PARAGRAPHS = "<p id=\"1\">The dark sky was <em><strong>pierced</strong></em> by a <div>blade</div> of light.</p><p id=\"2\" class=\"awesome\" style=\"tisktisk;\">one bird <blink>two shoes</blink> and a cat</p>"

    def test_filter_attributes( self ):
        
        # declare variables
        start_string = ""
        allowed_attributes = ""
        test_string = ""
        expected_string = ""
        error_message = ""
        
        # initialize
        start_string = TestHTMLHelper.TEST_HTML_FRAGMENT_PARAGRAPHS
        allowed_attributes = {
               'p' : [ 'id', ],
           }
        expected_string = "<p id=\"1\">The dark sky was <em><strong>pierced</strong></em> by a <div>blade</div> of light.</p><p id=\"2\">one bird <blink>two shoes</blink> and a cat</p>"
        
        # do work - default beautifulsoup parser
        error_message = "error with default BS parser"
        test_string = HTMLHelper.filter_attributes( start_string, allowed_attributes )
        
        # and the assert
        self.assertEqual( test_string, expected_string, msg = error_message )
        
        # do work - "html5lib" beautifulsoup parser - this breaks
        error_message = "error with html5lib BS parser"
        test_string = HTMLHelper.filter_attributes( start_string,
                                                    allowed_attributes,
                                                    bs_parser_IN = "html5lib" )
        
        # and the assert
        self.assertNotEqual( test_string, expected_string, msg = error_message )
        
    #-- END method test_filter_attributes() --#
    
    def test_remove_html_bleach( self ):
        
        # declare variables
        start_string = ""
        allowed_tags = []
        allowed_attributes = {}
        test_string = ""
        expected_string = ""
        error_message = ""
        
        # initialize
        start_string = TestHTMLHelper.TEST_HTML_FRAGMENT_PARAGRAPHS
        allowed_tags = [ 'p', ]
        allowed_attributes = {
               'p' : [ 'id', ],
           }
        expected_string = "<p id=\"1\">The dark sky was pierced by a blade of light.</p><p id=\"2\">one bird two shoes and a cat</p>"
        
        # do work - test bleach library - should break - https://github.com/mozilla/bleach/issues/280
        error_message = "bleach library error"
        test_string = HTMLHelper.remove_html( start_string,
                                              allowed_tags,
                                              allowed_attributes,
                                              bs_parser_IN = "html.parser",
                                              remove_method_IN = HTMLHelper.HTML_FILTER_LIBRARY_BLEACH )
        
        # and the assert
        self.assertNotEqual( test_string, expected_string, msg = error_message )
                
    #-- END method test_remove_html_bleach() --#


    def test_remove_html_w3lib( self ):
        
        # declare variables
        start_string = ""
        allowed_tags = []
        allowed_attributes = {}
        test_string = ""
        expected_string = ""
        error_message = ""
        
        # initialize
        start_string = TestHTMLHelper.TEST_HTML_FRAGMENT_PARAGRAPHS
        allowed_tags = [ 'p', ]
        allowed_attributes = {
               'p' : [ 'id', ],
           }
        expected_string = "<p id=\"1\">The dark sky was pierced by a blade of light.</p><p id=\"2\">one bird two shoes and a cat</p>"
        
        # do work - test w3lib library
        error_message = "w3lib library error"
        test_string = HTMLHelper.remove_html( start_string,
                                              allowed_tags,
                                              allowed_attributes,
                                              remove_method_IN = HTMLHelper.HTML_FILTER_LIBRARY_W3LIB )
        
        # and the assert
        self.assertEqual( test_string, expected_string, msg = error_message )
        
        # do work - test w3lib library with html5lib parser - this breaks
        error_message = "w3lib library error with html5lib beautifulsoup parser"
        test_string = HTMLHelper.remove_html( start_string,
                                              allowed_tags,
                                              allowed_attributes,
                                              bs_parser_IN = "html5lib",
                                              remove_method_IN = HTMLHelper.HTML_FILTER_LIBRARY_W3LIB )
        
        # and the assert
        self.assertNotEqual( test_string, expected_string, msg = error_message )
        
    #-- END method test_remove_html_w3lib() --#


#-- END unittest class TestHTMLHelper --#

if __name__ == '__main__':
    unittest.main()