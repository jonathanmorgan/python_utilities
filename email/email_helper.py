'''
This class encapsulates code for sending emails in python.  It ain't that hard,
   but I only want to have to write it once.

Example of what this class does under the hood:
>>> msg = MIMEText( message_IN )
>>> msg['Subject'] = 'Test message'
>>> msg['From'] = 'morga125@msu.edu'
>>> msg['To'] = 'jonathan.morgan.007@gmail.com'                
>>> s = smtplib.SMTP('localhost')
>>> s.sendmail( 'morga125@msu.edu', 'jonathan.morgan.007@gmail.com', msg.as_string() )
>>> s.quit()

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

# MIME types - for now, just support text.
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
        my_smtp_server = self.m_smtp_server
        if ( my_smtp_server ):
        
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


    def set_message( self, value_IN, MIME_type_IN = "text/plain" ):
    
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
        
        # eventually, will make different instances based on type passed in.
        #    For now, all text all the time.
        mime_message_instance = MIMEText( value_IN )
        
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
        Accepts a message and an optional MIME type (defaults to text).           
        Preconditions: None
        Postconditions: None
        '''
    
        # return reference
        status_OUT = EmailHelper.STATUS_SUCCESS
        
        # declare variables
        me = "set_message"

        # see if there is a value passed in.
        if ( ( value_IN ) and ( value_IN != "" ) ):
        
            # eventually, will make different instances based on type passed in.
            #    For now, all text all the time.
            self.m_smtp_server_host = value_IN
            
            # And, make new smtp server instance for this host name.
            self.m_smtp_server = smtplib.SMTP( value_IN )
            
        else:
        
            # no host name.  If there is an smtp server instance, clear it out.
            self.m_smtp_server = None
        
        #-- END check to see if hostname passed in.
        
        return status_OUT
    
    #-- END method set_smtp_server_host() --#


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