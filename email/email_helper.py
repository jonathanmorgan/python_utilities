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

'''
This class encapsulates code for sending emails in python.  It ain't that hard,
   but I only want to have to write it once with all the error checking, etc.
   I want.

Example of what this class does under the hood:

    # make message
    email_message = MIMEText( message_IN )
    email_message[ 'Subject' ] = 'Test message'
    email_message[ 'From' ] = 'morga125@msu.edu'
    email_message[ 'To' ] = 'jonathan.morgan.007@gmail.com'
    
    # Make Non-SSL connection to SMTP server
    #my_smtp_server = smtplib.SMTP('localhost')
    
    # OR SSL connection to SMTP server
    my_smtp_server = smtplib.SMTP_SSL( 'localhost', 465 )
    
    # log in to SMTP server.
    my_smtp_server.login( my_smtp_username, my_smtp_password )
    
    # Send mail
    my_smtp_server.sendmail( 'morga125@msu.edu', 'jonathan.morgan.007@gmail.com', email_message.as_string() )
    
    # close connection.
    my_smtp_server.quit()

Usage Example:

    from email_helper import EmailHelper
    email = EmailHelper()
    email.set_smtp_server_host( 'localhost' )
    email.set_to_address( 'jonathan.morgan.007@gmail.com,jonathan@nieonline.com' )
    email.set_from_address( 'morga125@msu.edu' )
    email.set_subject( 'test email - 2011-12-03 - 22.26' )
    email.set_message( 'test message.' )
    email.send_email()

More examples, for the future:
http://docs.python.org/library/email-examples.html

'''

# smtp import
import smtplib

# MIME types for emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#================================================================================
# EmailHelper class
#================================================================================

# define EmailHelper class.
class EmailHelper( object ):


    '''
    This class encapsulates code for sending emails in python.  It ain't that
       hard, but I only want to have to write it once.
    '''


    #============================================================================
    # Constants-ish
    #============================================================================


    # MIME type constants
    MIME_TYPE_TEXT = "text/plain"
    MIME_TYPE_HTML = "text/html"

    # email field constants
    EMAIL_SUBJECT = "Subject"
    EMAIL_FROM = "From"
    EMAIL_TO = "To"
    
    # status constants
    STATUS_SUCCESS = "Success!"


    #============================================================================
    # Instance variables
    #============================================================================


    m_smtp_server = None
    m_smtp_server_host = ""
    m_smtp_server_port = -1
    m_smtp_server_username = ""
    m_smtp_server_password = ""
    m_smtp_server_use_SSL = False
    m_from_address = ""
    m_to_address = ""
    m_subject = ""
    m_message = None


    #============================================================================
    # Built-in Instance methods
    #============================================================================


    def __del__( self ):
    
        # see if we have an SMTP server instance.
        if ( self.m_smtp_server ):
        
            # Got one.  "quit()" it.
            self.m_smtp_server.quit()
        
        #-- END check to see if we have an SMTP server instance --#
    
    #-- END method __del__() --#


    #============================================================================
    # Instance methods
    #============================================================================


    def get_smtp_server( self, *args, **kwargs ):
    
        # return reference
        instance_OUT = None
        
        # declare variables
        my_server = None
        
        # got one stored already?
        my_server = self.m_smtp_server
        if ( ( my_server) and ( my_server != None ) ):
        
            # yes - return it.
            instance_OUT = my_server
        
        else:
        
            # initialize server, return result.
            instance_OUT = self.initialize_smtp_server()
        
        #-- END check to see if server already in instance. --#
        
        return instance_OUT
    
    #-- END method get_smtp_server --#


    def initialize_smtp_server( self, *args, **kwargs ):

        # return reference
        instance_OUT = None
        
        # declare variables
        my_smtp_server = None
        use_SSL = False
        my_smtp_host_name = ""
        my_smtp_username = ""
        my_smtp_password = ""
        

        # get values.
        my_smtp_host_name = self.m_smtp_server_host
        my_smtp_host_port = self.m_smtp_server_port
        my_smtp_username = self.m_smtp_server_username
        my_smtp_password = self.m_smtp_server_password
        use_SSL = self.m_smtp_server_use_SSL

        # got a host name?
        if ( ( my_smtp_host_name ) and ( my_smtp_host_name != None ) and ( my_smtp_host_name != "" ) ):
        
            # SSL?
            if ( use_SSL == True ):
            
                # got a port?
                if ( ( my_smtp_host_port ) and ( my_smtp_host_port > 0 ) ):
                
                    # We have a port.  Create server.
                    my_smtp_server = smtplib.SMTP_SSL( my_smtp_host_name, my_smtp_host_port )
                    
                else:
                
                    # no port.
                    my_smtp_server = smtplib.SMTP_SSL( my_smtp_host_name )
                    
                #-- END check to see if we have a port --#
            
            else:
            
                # got a port?
                if ( ( my_smtp_host_port ) and ( my_smtp_host_port > 0 ) ):
                
                    # We have a port.  Create server.
                    my_smtp_server = smtplib.SMTP( my_smtp_host_name, my_smtp_host_port )
                    
                else:
                
                    # no port.
                    my_smtp_server = smtplib.SMTP( my_smtp_host_name )
                    
                #-- END check to see if we have a port --#

            #-- END check to see if SSL --#
            
            # got username?
            if ( ( my_smtp_username ) and ( my_smtp_username != None ) and ( my_smtp_username != "" ) ):
            
                # yes.  Login.
                my_smtp_server.login( my_smtp_username, my_smtp_password )
                
            #-- END check to see if we have username. --#
            
            # store the server.
            self.m_smtp_server = my_smtp_server
            
            # return the server.
            instance_OUT = self.get_smtp_server()
        
        else:
        
            # no host name - no server.
            instance_OUT = None
        
        #-- END check to see if hostname --#
        
        return instance_OUT
        
    #-- END method initialize_smtp_server() --#


    def send_email( self, message_IN = None, subject_IN = None, from_address_IN = None, to_address_IN = None ):
    
        '''
        Accepts a from address.  Stores it.  If message, also adds from address
           to m_message.
        Preconditions: Must have already set your smtp_server_host.
        Postconditions: None
        '''
        
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # instance variables
        me = "send_email"
        my_smtp_server = None
        my_message = None
        
        # message passed in?
        if ( message_IN ):
        
            # Set it.
            self.set_message( message_IN )
        
        #-- END check to see if message passed in. --#
        
        # subject passed in?
        if ( subject_IN ):
        
            # Set it.
            self.set_subject( subject_IN )
        
        #-- END check to see if subject passed in. --#
        
        # from address passed in?
        if ( from_address_IN ):
        
            # Set it.
            self.set_from_address( from_address_IN )
        
        #-- END check to see if from address passed in. --#
        
        # to address passed in?
        if ( to_address_IN ):
        
            # Set it.
            self.set_to_address( to_address_IN )
        
        #-- END check to see if to address passed in. --#
        
        # Got server?
        my_smtp_server = self.get_smtp_server()
        if ( ( my_smtp_server ) and ( my_smtp_server != None ) ):
        
            # got a server.  Got message?
            my_message = self.m_message
            if ( my_message ):
            
                # Got a message.  Send it (if no to or from, we'll see what
                #    happens).
                my_smtp_server.sendmail( self.m_from_address, self.m_to_address, my_message.as_string() )
                
            else:
            
                status_OUT = "In " + me + ": ERROR - no message, so nothing to send.  Aborting."
            
            #-- END check to see if message. --#
        
        else:
        
            status_OUT = "In " + me + ": ERROR - no server, so can't send.  Aborting."
        
        #-- END check to see if we have a server. --#
        
        return status_OUT
        
    #-- END method send_email() --#
    
    
    def set_from_address( self, value_IN ):
    
        '''
        Accepts a from address.  Stores it.  If message, also adds from address
           to m_message.
        Preconditions: None
        Postconditions: Updates the message as well as the instance variable.
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_from_address"

        # store the subject.
        self.m_from_address = value_IN
        
        # If message, then also store the subject in the message.
        if ( self.m_message ):
        
            self.m_message[ EmailHelper.EMAIL_FROM ] = self.m_from_address
            
        #-- END check to see if message --#

        return status_OUT
    
    #-- END method set_from_address() --#


    def set_message( self, value_IN, MIME_type_IN = MIME_TYPE_TEXT ):
    
        '''
        Accepts a message and an optional MIME type (defaults to text).           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_message"
        mime_message_instance = None
        message = None
        
        # HTML?
        if ( MIME_type_IN == self.MIME_TYPE_HTML ):
        
            # Multi-part to start, then add HTML as an attachment...
            mime_message_instance = MIMEMultipart( 'alternative' )
            
            # create HTML message.
            message = MIMEText( value_IN, 'html' )
            
            # attach it.
            mime_message_instance.attach( message )
            
            # set preamble in case mail client doesn't like HTML
            mime_message_instance.preamble = "Your mail reader does not support HTML email."
            
        elif ( MIME_type_IN == self.MIME_TYPE_TEXT ):

            # plain text.
            mime_message_instance = MIMEText( value_IN )

        else:

            # unknown - Multi-part, add text as an attachment...
            mime_message_instance = MIMEMultipart( 'alternative' )
            
            # unknown - treat as plain text.
            message = MIMEText( value_IN )
        
            # attach it.
            mime_message_instance.attach( message )
            
        #-- END check of MIME type --#
        
        # success?
        if ( mime_message_instance ):
        
            self.m_message = mime_message_instance
            
            # got subject, from or to?

            # subject
            if ( self.m_subject ):
            
                self.m_message[ EmailHelper.EMAIL_SUBJECT ] = self.m_subject
            
            #-- END check to see if Subject --#
            
            # from
            if ( self.m_from_address ):
            
                self.m_message[ EmailHelper.EMAIL_FROM ] = self.m_from_address
            
            #-- END check to see if From address --#
            
            # to
            if ( self.m_to_address ):
            
                self.m_message[ EmailHelper.EMAIL_TO ] = self.m_to_address
            
            #-- END check to see if To address --#
        
        else:
        
            status_OUT = "In " + me + ": ERROR - we have a message ( \"" + str( value_IN ) + "\" ), but trying to put it in a MIMEText instance failed."
        
        #-- END check to see if we got message back. --#
        
        return status_OUT
    
    #-- END method set_message() --#


    def set_smtp_server_host( self, value_IN = "" ):
    
        '''
        Accepts SMTP server host name.           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_smtp_server_host"

        # see if there is a value passed in.
        if ( ( value_IN ) and ( value_IN != "" ) ):
        
            # eventually, will make different instances based on type passed in.
            #    For now, all text all the time.
            self.m_smtp_server_host = value_IN
            
            # And, make new smtp server instance for this host name.
            #self.m_smtp_server = smtplib.SMTP( value_IN )
            # use get_smtp_server, instead, so we can also set username, password.
            
        else:
        
            # no host name.  If there is an smtp server instance, clear it out.
            self.m_smtp_server_host = ""
            self.m_smtp_server = None
        
        #-- END check to see if hostname passed in.
        
        return status_OUT
    
    #-- END method set_smtp_server_host() --#


    def set_smtp_server_password( self, value_IN = "" ):
    
        '''
        Accepts SMTP server password.           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_smtp_server_password"

        # see if there is a value passed in.
        if ( ( value_IN ) and ( value_IN != "" ) ):
        
            # store value.
            self.m_smtp_server_password = value_IN
            
        else:
        
            # no value.  Empty field.
            self.m_smtp_server_password = ""
        
        #-- END check to see if value passed in.
        
        return status_OUT
    
    #-- END method set_smtp_server_password() --#


    def set_smtp_server_port( self, value_IN = -1 ):
    
        '''
        Accepts SMTP server port.           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_smtp_server_port"

        # see if there is a value passed in.
        if ( ( value_IN ) and ( value_IN > 0 ) ):

            # store value.        
            self.m_smtp_server_port = value_IN
            
        else:
        
            # no value.  Clear field.
            self.m_smtp_server_port = ""
        
        #-- END check to see if value passed in. --#
        
        return status_OUT
    
    #-- END method set_smtp_server_port() --#


    def set_smtp_server_use_SSL( self, value_IN = False ):
    
        '''
        Accepts SMTP server username.           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_smtp_server_use_SSL"

        # see if there is a value passed in.
        if ( value_IN ):
        
            # set value.
            self.m_smtp_server_use_SSL = value_IN
            
        else:
        
            # no value.  Clear field.
            self.m_smtp_server_use_SSL = False
        
        #-- END check to see if value passed in. --#
        
        return status_OUT
    
    #-- END method set_smtp_server_use_SSL() --#


    def set_smtp_server_username( self, value_IN = "" ):
    
        '''
        Accepts SMTP server username.           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_smtp_server_username"

        # see if there is a value passed in.
        if ( ( value_IN ) and ( value_IN != "" ) ):
        
            # set value.
            self.m_smtp_server_username = value_IN
            
        else:
        
            # no value.  Clear field.
            self.m_smtp_server_username = ""
        
        #-- END check to see if value passed in. --#
        
        return status_OUT
    
    #-- END method set_smtp_server_username() --#


    def set_subject( self, value_IN ):
    
        '''
        Accepts a subject.  Stores subject.  If message, also adds subject to
           m_message.
        Preconditions: None
        Postconditions: Updates the message as well as the instance variable.
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_subject"

        # store the subject.
        self.m_subject = value_IN
        
        # If message, then also store the subject in the message.
        if ( self.m_message ):
        
            self.m_message[ EmailHelper.EMAIL_SUBJECT ] = self.m_subject
            
        #-- END check to see if message --#

        return status_OUT
    
    #-- END method set_subject() --#


    def set_to_address( self, value_IN ):
    
        '''
        Accepts a to address.  Stores it.  If message, also adds to address to
           m_message.
        Preconditions: None
        Postconditions: Updates the message as well as the instance variable.
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_to_address"

        # store the subject.
        self.m_to_address = value_IN
        
        # If message, then also store the subject in the message.
        if ( self.m_message ):
        
            self.m_message[ EmailHelper.EMAIL_TO ] = self.m_to_address
            
        #-- END check to see if message --#

        return status_OUT
    
    #-- END method set_to_address() --#


#-- END class EmailHelper --#
