"""
This file contains helpers for implementers of django.test.TestCase.  Extend
    this class instead of django.test.TestCase to use these helpers.
"""

# base Python imports
import difflib
import json
import logging
import os
import sys

# import six
import six

# django imports
import django.test

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper


class DjangoTestCaseHelper( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False
    LOGGER_NAME = "python_utilities.django_utils.django_test_case_helper.DjangoTestCaseHelper"

    # CLASS NAME
    CLASS_NAME = "DjangoTestCaseHelper"
    
    #----------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - setup
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - shared methods
    #----------------------------------------------------------------------------


    def validate_string_against_file_contents( self, test_string_IN, reference_file_path_IN ):

        # declare variables
        me = "validate_string_against_file_contents"
        debug_flag = None
        test_data = None
        reference_data_file_path = None
        reference_data_file = None
        reference_data = None
        test_value = None
        should_be = None
        error_string = None
        
        # declare variables - diff
        temp_data = None
        test_data_lines = None
        test_data_line_count = None
        reference_data_lines = None
        reference_data_line_count = None
        diff_output_line = None
        diff_count = None
        test_data_line = None
        reference_data_line = None
        
        # init
        debug_flag = self.DEBUG
        test_data = test_string_IN
        reference_data_file_path = reference_file_path_IN
        
        # load the data file that contains the goal output.
        try:
        
            # yes.  Output to file.
            with open( reference_data_file_path ) as reference_data_file:
            
                # read contents of file
                reference_data = reference_data_file.read()
                
            #-- END with open( reference_data_file_path, "w" ) as reference_data_file --#
            
        except:
        
            # Could not read reference data.
            status_message = "ERROR - Exception thrown reading network data from {}.".format( reference_data_file_path )
            exception_instance = sys.exc_info()[0]
            ExceptionHelper.log_exception( exception_instance,
                                           message_IN = status_message,
                                           method_IN = me,
                                           logger_name_IN = self.LOGGER_NAME,
                                           do_print_IN = debug_flag,
                                           log_level_code_IN = logging.ERROR )
            
        #-- END try...except around writing output to file --#

        # lengths and content should be the same.        
        reference_data_char_count = len( reference_data )
        
        # diff
        temp_data = test_data.strip()
        test_data_lines = temp_data.splitlines()
        temp_data = reference_data.strip()
        reference_data_lines = temp_data.splitlines()
        diff_count = 0
        for diff_output_line in difflib.unified_diff( test_data_lines,
                                                      reference_data_lines,
                                                      fromfile = 'test_data',
                                                      tofile = 'reference_data',
                                                      lineterm = '' ):
        
            # print the line
            print( diff_output_line )
            diff_count += 1
            
        #-- END loop over diff output. --#
        
        # diff_count should be 0
        test_value = diff_count
        should_be = 0
        error_string = "diff count was {}, should be {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # line counts?
        test_data_line_count = len( test_data_lines )
        reference_data_line_count = len( reference_data_lines )
        test_value = test_data_line_count
        should_be = reference_data_line_count
        error_string = "line counts are not equal. test: {}; reference: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # loop and compare line-by-line
        for line_index in range( test_data_line_count ):
        
            # get lines
            test_data_line = test_data_lines[ line_index ]
            reference_data_line = reference_data_lines[ line_index ]
                
            # lines should be the same
            test_value = test_data_line
            should_be = reference_data_line
            error_string = "data line not equal:\n- test: {}\n- reference: {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over lines in file --#

    #-- END test method validate_string_against_file_contents() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods - tests
    #----------------------------------------------------------------------------


#-- END test class DjangoTestCaseHelper --#
