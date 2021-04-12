# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2021 Jonathan Morgan

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
    Either make and store an instance of this in a class, or extend it.
'''

# imports

# python standard libraries
import logging

class LoggingHelper( object ):

    '''
    This class encapsulates code for making, storing, and interacting with the
       standard python logging library.  It is very basic to start.  It is not
       intended to replace the logger that you get from logging.getLogger().  It
       is more an interface to programmatic configuration and use of logging.
    '''


    #============================================================================
    # ! ==> Constants-ish
    #============================================================================


    LOGGER_NAME = "python_utilities.logging.logging_helper"
    CLASS_RESOURCE_STRING = ""

    # log level codes:
    LOG_LEVEL_CODE_CRITICAL = logging.CRITICAL # 50
    LOG_LEVEL_CODE_ERROR = logging.ERROR       # 40
    LOG_LEVEL_CODE_WARNING = logging.WARNING   # 30
    LOG_LEVEL_CODE_INFO = logging.INFO         # 20
    LOG_LEVEL_CODE_DEBUG = logging.DEBUG       # 10
    LOG_LEVEL_CODE_NOTSET = logging.NOTSET     # 00

    # logging output defaults
    LOGGING_DEFAULT_LEVEL = logging.DEBUG
    LOGGING_DEFAULT_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    LOGGING_DEFAULT_FILENAME = "./django-log.txt"
    LOGGING_DEFAULT_FILEMODE = "a"


    #============================================================================
    # NOT Instance variables
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #============================================================================


    # all properties are stored in dictionaries.  There is also an optional
    #    description dictionary, for use in outputting.
    #m_logger = None
    #m_logger_name = ""


    #============================================================================
    # ! ==> Class methods
    #============================================================================


    @classmethod
    def add_to_class_resource_string( cls, resource_string_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables
        class_resource_string = ""

        # got a resource string passed in?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # yes - get class resource string
            class_resource_string = cls.CLASS_RESOURCE_STRING

            # add the value passed in to the tail end.
            class_resource_string += resource_string_IN

            # make sure the updated string is stored.
            cls.CLASS_RESOURCE_STRING = class_resource_string

        #-- END check to see if resource string. --#

        # return the entire resource string
        value_OUT = cls.CLASS_RESOURCE_STRING

        return value_OUT

    #-- END class method add_to_class_resource_string() --#


    @classmethod
    def get_a_logger( cls, logger_name_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables

        # make logger instance.
        if ( ( logger_name_IN is None ) or ( logger_name_IN == "" ) ):

            # no logger name.
            value_OUT = logging.getLogger()

        else:

            # there is a logger name.
            value_OUT = logging.getLogger( logger_name_IN )

        #-- END check to see how we make a logger. --#

        return value_OUT

    #-- END class method get_a_logger() --#


    @classmethod
    def initialize_logging_to_file( cls,
                                    level_IN = LOGGING_DEFAULT_LEVEL,
                                    format_IN = LOGGING_DEFAULT_FORMAT,
                                    filename_IN = LOGGING_DEFAULT_FILENAME,
                                    filemode_IN = LOGGING_DEFAULT_FILEMODE ):

        '''
        method for initializing logging, just so it is here for when I forget
            the basic logging init.
        '''

        logging.basicConfig(
            level = level_IN,
            format = format_IN,
            filename = filename_IN,
            filemode = filemode_IN # set to 'a' if you want to append, rather than overwrite each time.
        )
        print( "Logging initialized, to {}".format( filename_IN ) )

    #-- END method initialize_logging_to_file() --#


    @classmethod
    def is_logging_active( cls, resource_string_IN = None ):

        # return reference
        is_active_OUT = False

        # declare variables
        class_resource_string = ""

        # get class-level resource string.
        class_resource_string = cls.CLASS_RESOURCE_STRING

        # got a resource string passed in?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # yes.  See if the class-level resource string contains it.
            if ( resource_string_IN in class_resource_string ):

                # it does.  Logging is active at the class level.
                is_active_OUT = True

            else:

                # it does not.  Logging not active.
                is_active_OUT = False

            #-- END check to see if logging active.

        #-- END check to see if resource string --#

        return is_active_OUT

    #-- END method is_logging_active() --#


    @classmethod
    def log_message( cls,
                     message_IN,
                     method_IN = "",
                     indent_with_IN = "",
                     logger_name_IN = "",
                     do_print_IN = False,
                     resource_string_IN = None,
                     log_level_code_IN = None,
                     logger_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''

        # declare variables
        do_output = True
        my_message = ""
        my_logger = None
        my_logger_name = ""

        # got a resource string?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # check if resource string is in the class-level resource string.
            do_output = cls.is_logging_active( resource_string_IN )

        else:

            # if no resource string, do output.
            do_output = True

        #-- END check to see if resource string.

        # do we output?
        if ( do_output == True ):

            # got a message?
            if ( message_IN ):

                my_message = message_IN

                # got a method?
                if ( method_IN ):

                    # We do - append to front of message.
                    my_message = "In {}(): {}".format( method_IN, my_message )

                #-- END check to see if method passed in --#

                # indent?
                if ( indent_with_IN ):

                    my_message = indent_with_IN + my_message

                #-- END check to see if we indent. --#

                # debug is on.  Start logging rather than using print().
                #print( my_message )

                # get a logger
                if ( logger_IN is not None ):

                    my_logger = logger_IN

                else:

                    # got a logger name?
                    my_logger_name = cls.LOGGER_NAME
                    if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):

                        # use logger name passed in.
                        my_logger_name = logger_name_IN

                    #-- END check to see if logger name --#

                    # get logger
                    my_logger = cls.get_a_logger( my_logger_name )

                #-- END check to see if logger passed in. --#

                # log debug.
                if ( log_level_code_IN is not None ):

                    # log level passed in.  Use it.
                    my_logger.log( log_level_code_IN, my_message )

                else:

                    # just call debug.
                    my_logger.debug( my_message )

                #-- END check to see if desired log level passed in. --#

                # print also?
                if ( do_print_IN == True ):

                    # yes.
                    print( my_message )

                #-- END check to see if we print also. --#

            #-- END check to see if message. --#

        #-- END check to see if we do_output? --#

    #-- END method log_message() --#


    @classmethod
    def output_debug( cls,
                      message_IN,
                      method_IN = "",
                      indent_with_IN = "",
                      logger_name_IN = "",
                      do_print_IN = False,
                      resource_string_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''

        # call log_message()
        cls.log_message( message_IN,
                         method_IN = method_IN,
                         indent_with_IN = indent_with_IN,
                         logger_name_IN = logger_name_IN,
                         do_print_IN = do_print_IN,
                         resource_string_IN = resource_string_IN,
                         log_level_code_IN = LoggingHelper.LOG_LEVEL_CODE_DEBUG )

    #-- END method output_debug() --#


    @classmethod
    def remove_from_class_resource_string( cls, resource_string_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables
        class_resource_string = ""

        # got a resource string passed in?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # yes - get class resource string
            class_resource_string = cls.CLASS_RESOURCE_STRING

            # does the class resource string contain the string passed in?
            if ( resource_string_IN in class_resource_string ):

                # yes - replace with "".
                class_resource_string = class_resource_string.replace( resource_string_IN, "" )

                # make sure the updated string is stored.
                cls.CLASS_RESOURCE_STRING = class_resource_string

            #-- END check to see if the string is present --#

        #-- END check to see if resource string passed in. --#

        # return the entire resource string
        value_OUT = cls.CLASS_RESOURCE_STRING

        return value_OUT

    #-- END class method remove_from_class_resource_string() --#


    #============================================================================
    # ! ==> Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):

        # always call parent's __init__()
        super( LoggingHelper, self ).__init__()

        # initialize variables
        self.m_logger = None
        self.m_logger_name = self.LOGGER_NAME
        self.logger_debug_flag = True
        self.logger_also_print_flag = False
        self.logger_resource_string = ""

        # initialize variables - log output
        self.logging_level = self.LOGGING_DEFAULT_LEVEL
        self.logging_format = self.LOGGING_DEFAULT_FORMAT
        self.logging_filename = self.LOGGING_DEFAULT_FILENAME
        self.logging_filemode = self.LOGGING_DEFAULT_FILEMODE

    #-- END method __init__() --#


    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def add_to_my_resource_string( self, resource_string_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables
        my_resource_string = ""

        # got a resource string passed in?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # yes - get class resource string
            my_resource_string = self.logger_resource_string

            # add the value passed in to the tail end.
            my_resource_string += resource_string_IN

            # make sure the updated string is stored.
            self.logger_resource_string = my_resource_string

        #-- END check to see if resource string. --#

        # return the entire resource string
        value_OUT = self.logger_resource_string

        return value_OUT

    #-- END class method add_to_my_resource_string() --#


    def get_logger_name( self ):

        # return reference
        value_OUT = None

        # get value
        value_OUT = self.m_logger_name

        return value_OUT

    #-- END method get_logger_name --#


    def get_logger( self, logger_name_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables
        logger_name = ""
        logger_instance = None

        # get m_logger
        value_OUT = self.m_logger

        # got anything?
        if ( value_OUT is None ):

            # no.  Do we have an application string?
            if ( ( logger_name_IN is None ) or ( logger_name_IN == "" ) ):

                # no - see if there is one in instance.
                logger_name = self.get_logger_name()

            else:

                # yes - use it.
                logger_name = logger_name_IN

            #-- END check to see if app_name. --#

            #print( "logger name: " + logger_name )

            # make logger instance.
            logger_instance = LoggingHelper.get_a_logger( logger_name )

            # store the logger.
            self.set_logger( logger_instance )

            # get the logger.
            value_OUT = self.get_logger()

        #-- END check to see if logger initialized. --#

        return value_OUT

    #-- END method get_logger --#


    def init_logging_to_file( self ):

        '''
        method for initializing logging, just so it is here for when I forget
            the basic logging init.
        '''

        # declare variables
        me = "init_logging_to_file"
        my_level = None
        my_format = None
        my_filename = None
        my_filemode = None

        # retrieve from instance values from instance.
        my_level = self.logging_level
        my_format = self.logging_format
        my_filename = self.logging_filename
        my_filemode = self.logging_filemode

        # init
        self.initialize_logging_to_file(
            level_IN = my_level,
            format_IN = my_format,
            filename_IN = my_filename,
            filemode_IN = my_filemode # set to 'a' if you want to append, rather than overwrite each time.
        )
        print( "Logging initialized, to {}".format( filename_IN ) )

    #-- END method init_logging_to_file() --#


    def is_my_logging_active( self, resource_string_IN = None ):

        # return reference
        is_active_OUT = False

        # declare variables
        my_resource_string = ""

        # if debug flag is true, logging is active.
        if ( self.logger_debug_flag == True ):

            # logging is active
            is_active_OUT = True

        else:

            # got a resource string?
            if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

                # yes.  Does the class-level resource string contain it?
                is_active_OUT = self.is_logging_active( resource_string_IN )

                if ( is_active_OUT == False ):

                    # not active at class level.  How about instance level?
                    my_resource_string = self.logger_resource_string
                    if ( resource_string_IN in my_resource_string ):

                        # it is in instance string.  Logging is active.
                        is_active_OUT = True

                    else:

                        # not in instance strings.  Logging not active.
                        is_active_OUT = False

                    #-- END check to see if logging active.

                #-- END check to see if resource is present at class level --#

            else:

                # no resource string - not active.
                is_active_OUT = False

            #-- END check to see if resource string --#

        #-- END check to see if logger flag is True. --#

        return is_active_OUT

    #-- END method is_my_logging_active() --#


    def output_debug_message( self,
                              message_IN,
                              method_IN = "",
                              indent_with_IN = "",
                              logger_name_IN = "",
                              do_print_IN = False,
                              resource_string_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''

        # call output_message()
        self.output_message( message_IN,
                            method_IN = method_IN,
                            indent_with_IN = indent_with_IN,
                            logger_name_IN = logger_name_IN,
                            do_print_IN = do_print_IN,
                            resource_string_IN = resource_string_IN,
                            log_level_code_IN = LoggingHelper.LOG_LEVEL_CODE_DEBUG )

    #-- END method output_debug_message() --#


    def output_message( self,
                        message_IN,
                        method_IN = "",
                        indent_with_IN = "",
                        logger_name_IN = "",
                        do_print_IN = False,
                        resource_string_IN = None,
                        log_level_code_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''

        # declare variables
        my_message = ""
        my_logger = None
        my_logger_name = ""
        do_output = False

        # got a message?
        if ( message_IN ):

            # do output?
            do_output = self.is_my_logging_active( resource_string_IN )

            # only print if debug is on or resource_string_IN is found in the
            #     self.logger_resource_string variable contents.
            if ( do_output == True ):

                my_message = message_IN

                # got a method?
                if ( method_IN ):

                    # We do - append to front of message.
                    my_message = "In " + method_IN + "(): " + my_message

                #-- END check to see if method passed in --#

                # indent?
                if ( indent_with_IN ):

                    my_message = indent_with_IN + my_message

                #-- END check to see if we indent. --#

                # debug is on.  Start logging rather than using print().
                #print( my_message )

                # got a logger name?
                if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):

                    # use logger name passed in.
                    my_logger_name = logger_name_IN

                    # get logger
                    my_logger = LoggingHelper.get_a_logger( my_logger_name )

                else:

                    # no custom logger name - get nested logger.
                    my_logger = self.get_logger()

                #-- END check to see if logger name --#

                # log debug.
                if ( log_level_code_IN is not None ):

                    # log level passed in.  Use it.
                    my_logger.log( log_level_code_IN, my_message )

                else:

                    # just call debug.
                    my_logger.debug( my_message )

                #-- END check to see if desired log level passed in. --#


                # also print?
                if ( ( do_print_IN == True ) or ( self.logger_also_print_flag == True ) ):

                    # we have been requested to also print.
                    print( my_message )

                #-- END check to see if we also print. --#

            #-- END check to see if debug is on --#

        #-- END check to see if message. --#

    #-- END method output_message() --#


    def remove_from_my_resource_string( self, resource_string_IN = "" ):

        # return reference
        value_OUT = None

        # declare variables
        my_resource_string = ""

        # got a resource string passed in?
        if ( ( resource_string_IN is not None ) and ( resource_string_IN != "" ) ):

            # yes - get instance resource string
            my_resource_string = self.logger_resource_string

            # does the class resource string contain the string passed in?
            if ( resource_string_IN in my_resource_string ):

                # yes - replace with "".
                my_resource_string = my_resource_string.replace( resource_string_IN, "" )

                # make sure the updated string is stored.
                self.logger_resource_string = my_resource_string

            #-- END check to see if the string is present --#

        #-- END check to see if resource string passed in. --#

        # return the entire resource string
        value_OUT = self.logger_resource_string

        return value_OUT

    #-- END class method remove_from_my_resource_string() --#


    def set_logger_name( self, value_IN ):

        '''
        Accepts application name.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # store value.
        self.m_logger_name = value_IN

        # return it.
        value_OUT = self.get_logger_name()

        return value_OUT

    #-- END method set_logger_name() --#


    def set_logger( self, instance_IN ):

        '''
        Accepts logger.  Stores it and returns it.
        '''

        # return reference
        value_OUT = None

        # use store logger.
        self.m_logger = instance_IN

        # return it.
        value_OUT = self.m_logger

        return value_OUT

    #-- END method set_logger() --#


#-- END class LoggingHelper --#
