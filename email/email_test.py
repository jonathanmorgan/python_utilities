# Email imports
import smtplib

# MIME types for emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# configure SMTP, for use when there is an exception.
smtp_host = "smtp.gmail.com"
smtp_port = 465
smtp_username = ""
smtp_password = ""
smtp_use_ssl = True
email_from = ""
email_to = ""

# Create message.
email_message_body = "Test"

# email message
email_message = MIMEText( email_message_body )
email_message[ 'Subject' ] = 'EMAIL TEST'
email_message[ 'From' ] = email_from
email_message[ 'To' ] = email_to

# use SSL?
if ( smtp_use_ssl == True ):

    # use SSL
    my_smtp_server = smtplib.SMTP_SSL( smtp_host, smtp_port )
    
else:

    # don't use SSL
    my_smtp_server = smtplib.SMTP( smtp_host, smtp_port )        
    
#-- END check to see if use SSL --#

# got username (allow empty password)?
if ( ( smtp_username ) and ( smtp_username != None ) and ( smtp_username != "" ) ):

    # yes.  Login.
    my_smtp_server.login( smtp_username, smtp_password )
    
#-- END check to see if we have username. --#

# send email
my_smtp_server.sendmail( email_from, email_to, email_message.as_string() )
my_smtp_server.quit()
