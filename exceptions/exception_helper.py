from __future__ import unicode_literals

'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

python_utilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/python_utilities. If not, see http://www.gnu.org/licenses/.
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# base python libraries
import datetime
import logging
import sys
import time
import traceback

# site-specific imports.
#site_path = '/home/socs/socs_reddit/'
#if site_path not in sys.path:
#    sys.path.append( site_path )

# python_utilities
from python_utilities.email.email_helper import EmailHelper
from python_utilities.logging.logging_helper import LoggingHelper

#================================================================================
# class ExceptionHelper
#================================================================================

class ExceptionHelper( LoggingHelper ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "
    
    # DEBUG - changed to instance variable.
    #DEBUG_FLAG = False


    #============================================================================
    # instance variables
    #============================================================================


    # email helpers.
    email_helper = None
    email_status_address = ""
    
    # last exception details
    last_exception_details = ""
    
    # debug_flag
    debug_flag = False
    
    # logging
    logging_level = logging.ERROR
    
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # call parent's __init__()
        super( ExceptionHelper, self ).__init__()

        # email
        self.email_helper = None
        self.email_status_address = ""
        
        # last exception description
        self.last_exception_details = ""
        
        # debug
        self.debug_flag = False
        
        # logging
        
        # set logger name (for LoggingHelper parent class: (LoggingHelper -->
        #    BasicRateLimited --> ArticleCoder).
        self.set_logger_name( "python_utilities.exceptions.exception_helper" )
        
        # log level
        self.logging_level = logging.ERROR

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def email_initialize( self, smtp_host_IN = "localhost", smtp_port_IN = -1, smtp_use_ssl_IN = False, smtp_username_IN = "", smtp_password_IN = "", *args, **kwargs ):
    
        '''
        Accepts properties that can be used to initialize an email helper
           instance.  Initializes object, stores it in instance variable.
        '''
    
        # declare variables
        my_email_helper = None
        
        # create email helper
        my_email_helper = EmailHelper()
        
        # set host.
        my_email_helper.set_smtp_server_host( smtp_host_IN )

        # set port?
        if ( ( smtp_port_IN ) and ( smtp_port_IN != None ) and ( smtp_port_IN > 0 ) ):
        
            my_email_helper.set_smtp_server_port( smtp_port_IN )
        
        #-- END check to see if port passed in. --#
        
        # use ssl?
        my_email_helper.set_smtp_server_use_SSL( smtp_use_ssl_IN )
        
        # set username?
        if ( ( smtp_username_IN ) and ( smtp_username_IN != None ) and ( smtp_username_IN != "" ) ):
        
            my_email_helper.set_smtp_server_username( smtp_username_IN )
        
        #-- END check to see if username passed in --#

        # set password?
        if ( ( smtp_password_IN ) and ( smtp_password_IN != None ) and ( smtp_password_IN != "" ) ):
        
            my_email_helper.set_smtp_server_password( smtp_password_IN )
        
        #-- END check to see if password passed in --#
        
        # store in instance variable.
        self.email_helper = my_email_helper
        
    #-- END method email_initialize() --#    
    
    
    def email_send( self, message_IN = None, subject_IN = None, from_address_IN = None, to_address_IN = None, *args, **kwargs ):

        '''
        Uses nested email_helper instance to send email.  Returns status message.
           If status returned is email_helper.STATUS_SUCCESS, then success, if
           anything else, it is an error message explaining why the email was not
           sent.
        '''
    
        # return reference
        status_OUT = ""
    
        # declare variables
        my_email_helper = None
        
        # get email helper
        my_email_helper = self.email_helper
        
        # got a helper?
        if ( ( my_email_helper ) and ( my_email_helper != None ) ):

            # yes - send email
            status_OUT = my_email_helper.send_email( message_IN, subject_IN, from_address_IN, to_address_IN )
            
        else:
        
            # no - error.
            status_OUT = "ERROR - no email helper present, so can't send email."
        
        #-- END check to see if we have an email helper. --#
        
        return status_OUT
    
    #-- END method email_send() --#
    
    
    def email_send_status( self, message_IN = None, subject_IN = None, *args, **kwargs ):

        '''
        If email helper and status email are set, uses nested email_helper
           instance to send email to status email.  Returns status message.
           If status returned is email_helper.STATUS_SUCCESS, then success, if
           anything else, it is an error message explaining why the email was not
           sent.
        '''
    
        # return reference
        status_OUT = ""
    
        # declare variables
        my_email_helper = None
        my_status_email = ""
        
        # get email helper and status address
        my_email_helper = self.email_helper
        my_status_email = self.email_status_address
        
        # got a helper?
        if ( ( my_email_helper ) and ( my_email_helper != None ) ):

            # yes.  Got a status email address?
            if ( ( my_status_email ) and ( my_status_email != None ) and ( my_status_email != "" ) ):

                # yes - send email
                status_OUT = my_email_helper.send_email( message_IN, subject_IN, my_status_email, my_status_email )
                
            else:
            
                # no status email address set.
                status_OUT = "ERROR - no email address set for sending status messages.  Can't send email status."
            
            #-- END check to see if status email present --#
            
        else:
        
            # no - error.
            status_OUT = "ERROR - no email helper present, so can't send email."
        
        #-- END check to see if we have a mail helper. --#
        
        return status_OUT
    
    #-- END method email_send_status() --#
    
    
    def get_logging_level( self ):
    
        # return reference
        value_OUT = None
        
        # get value
        value_OUT = self.logging_level
                
        return value_OUT
    
    #-- END method get_logger_name --#

    
    def log_exception_info( self, message_IN, log_level_IN = "" ):
    
        '''
        Accepts message string.  If debug is on, passes it to print().  If not,
           does nothing for now.
        '''
        
        # declare variables
        my_logger = None
        my_log_level = ""
    
        # got a message?
        if ( message_IN ):
        
            # get logger
            my_logger = self.get_logger()
            
            # Do we have a log level?
            if ( ( log_level_IN is None ) or ( log_level_IN == "" ) ):
            
                # no - see if there is one in instance.
                my_log_level = self.get_logging_level()
            
            else:
            
                # yes - use it.
                my_log_level = log_level_IN
            
            #-- END check to see if app_name. --#
           
            # log the message.
            my_logger.log( my_log_level, message_IN )
        
        #-- END check to see if message. --#
    
    #-- END method log_exception_info() --#


    def process_exception( self, exception_IN = None, message_IN = "", send_email_IN = False, email_subject_IN = "", print_details_IN = True, *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_logger = None
        exception_type = ""
        exception_value = ""
        exception_traceback = ""
        exception_details = ""
        temp_exception_string = ""
        error_email_subject = ""
        error_email_message = ""
        
        # got an exception?
        if ( ( exception_IN ) and ( exception_IN != None ) ):
        
            # get logger.
            my_logger = self.get_logger()
            
            # get exception details:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            
            exception_details = ""

            #-------------------------------------------------------------------#
            # intro
            #-------------------------------------------------------------------#
            
            # got a message?
            if ( ( message_IN ) and ( message_IN != "" ) ):
    
                # create current line of text.
                temp_exception_string = "====> " + message_IN

                # add to details.
                exception_details += temp_exception_string

                # print?
                if ( print_details_IN == True ):

                    self.log_exception_info( temp_exception_string )

                #-- END check to see if we should print details --#

            else:
            
                # create current line of text.
                temp_exception_string = "====> Exception caught"

                # add to details.
                exception_details += temp_exception_string
            
                # print?
                if ( print_details_IN == True ):

                    self.log_exception_info( temp_exception_string )

                #-- END check to see if we should print details --#

            #-- END check to see if we have a message --#
            
            #-------------------------------------------------------------------#
            # arguments
            #-------------------------------------------------------------------#

            # create current line of text.
            temp_exception_string = "      - args = " + str( exception_IN.args )

            # add to details.
            exception_details += "\n" + temp_exception_string
    
            # print?
            if ( print_details_IN == True ):

                self.log_exception_info( temp_exception_string )

            #-- END check to see if we should print details --#

            #-------------------------------------------------------------------#
            # exception type
            #-------------------------------------------------------------------#

            # create current line of text.
            temp_exception_string = "      - type = " + str( exception_type )

            # add to details.
            exception_details += "\n" + temp_exception_string
            
            #-------------------------------------------------------------------#
            # exception value
            #-------------------------------------------------------------------#

            # create current line of text.
            temp_exception_string = "      - value = " + str( exception_value )
            self.log_exception_info( temp_exception_string )

            # add to details.
            exception_details += "\n" + temp_exception_string
            
            #-------------------------------------------------------------------#
            # exception stack trace
            #-------------------------------------------------------------------#

            # create current line of text.
            temp_exception_string = "      - traceback = " + str( traceback.format_exc() )
            self.log_exception_info( temp_exception_string )

            # add to details.
            exception_details += "\n" + temp_exception_string

            #-------------------------------------------------------------------#
            # email?
            #-------------------------------------------------------------------#

            # do we send email?
            if ( send_email_IN == True ):
    
                # yes - send email.
                error_email_subject = email_subject_IN
                error_email_message = exception_details
                status_OUT = self.email_send_status( error_email_message, error_email_subject )
                self.log_exception_info( "====> Error email status: " + status_OUT )
                
            #-- END check to see if we've exceeded error limit. --#
        
        else:
        
            status_OUT = self.STATUS_ERROR_PREFIX + "no exception passed in, can't process exception."
        
        #-- END check to make sure exception passed in --#
        
        # store details, in case someone wants programmatic access to them.
        self.last_exception_details = exception_details
        
        return status_OUT
    
    #-- END method process_exception() --#


    def set_logging_level( self, value_IN ):
        
        '''
        Accepts logging level.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # store value.
        self.logging_level = value_IN
        
        # return it.
        value_OUT = self.get_logging_level()
        
        return value_OUT
        
    #-- END method set_logging_level() --#


#-- END class ExceptionHelper --#