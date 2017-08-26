# python imports
import os
import site
import unittest

# import the things we are testing.

try:

    from python_utilities.integers.integer_helper import IntegerHelper

except ImportError as ie:

    # get current directory path
    current_directory_path = os.path.dirname( os.path.abspath( __file__ ) )

    # add to python path
    site.addsitedir( current_directory_path )
    
    # try local import
    from integer_helper import IntegerHelper

#-- END attempt to import IntegerHelper --#


class TestIntegerHelper(unittest.TestCase):

    def test_is_valid_integer( self ):

        # declare variables
        test_value = ""
        is_valid = False
        should_be = ""
        must_be_greater_than = -1
        
        # ! ----> test 1 - None
        test_value = None
        must_be_greater_than = -1
        is_valid = IntegerHelper.is_valid_integer( test_value, must_be_greater_than_IN = must_be_greater_than )
        should_be = False

        # and the assert
        self.assertEqual( is_valid, should_be )
        
        # ! ----> test 2 - a string
        test_value = "census soliloquy"
        must_be_greater_than = -1
        is_valid = IntegerHelper.is_valid_integer( test_value, must_be_greater_than_IN = must_be_greater_than )
        should_be = False

        # and the assert
        self.assertEqual( is_valid, should_be )
        
        # ! ----> test 3 - an integer, as a string.
        test_value = "7"
        must_be_greater_than = -1
        is_valid = IntegerHelper.is_valid_integer( test_value, must_be_greater_than_IN = must_be_greater_than )
        should_be = False

        # and the assert
        self.assertEqual( is_valid, should_be )

        # ! ----> test 4 - an integer
        test_value = 1000
        must_be_greater_than = -1
        is_valid = IntegerHelper.is_valid_integer( test_value, must_be_greater_than_IN = must_be_greater_than )
        should_be = True

        # and the assert
        self.assertEqual( is_valid, should_be )

    #-- END method test_is_valid_integer() --#

#-- END unittest class TestStringHelper --#


if __name__ == '__main__':
    unittest.main()