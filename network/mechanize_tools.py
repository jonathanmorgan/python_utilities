'''
Based on OpenAnything: a kind and thoughtful library for HTTP web services

OpenAnything is part of 'Dive Into Python', a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Downloaded from: http://www.diveintopython.net/download/diveintopython-examples-5.4.zip

2013-07-20 - Jonathan Morgan - updated so that this uses mechanize's fork of
   urrlib2, and so that RedirectHandler appends each status to a list, instead
   of just storing most recent, in case of multiple redirects.

Usage:

# import mechanize
import mechanize

# import python utilities mechanize.
import python_utilities.network.mechanize_tools

# store URL to access
URL = 'http://www.winonapost.com/'

# create request
request = mechanize.Request( URL )

# set the redirect handler.
opener = mechanize.build_opener( python_utilities.network.mechanize_tools.SmartRedirectHandler() )

# open the URL
open_result = opener.open(request)

# if redirected, there will be a status attribute
if ( hasattr( open_result, "status_list" ) == True ):

    # redirected - list of statuses from redirects will be in open_result.status_list.
    print( str( open_result.status_list ) )
    
#-- END check to see if redirect --#

# final URL will be in open_result.geturl()
print( "- Final URL = " + open_result.geturl() )
'''

import mechanize

class SmartRedirectHandler( mechanize.HTTPRedirectHandler ):


    def http_error_301(self, req, fp, code, msg, headers):

        # return reference
        result = None

        result = mechanize.HTTPRedirectHandler.http_error_301( self, req, fp, code, msg, headers )

        # log redirect info.
        self.log_redirect_info( result, code )

        return result
        
    #-- END method http_error_301() --#


    def http_error_302(self, req, fp, code, msg, headers):

        # return reference
        result = None

        result = mechanize.HTTPRedirectHandler.http_error_302( self, req, fp, code, msg, headers )
        
        # log redirect info.
        self.log_redirect_info( result, code )

        return result

    #-- END method http_error_302() --#


    def log_redirect_info( self, result_IN, code_IN, *args, **kwargs ):
        
        # First, check to see if there is already a status_list.
        if ( ( hasattr( result_IN, "status_list" ) == True ) and ( result_IN.status_list ) and ( result_IN.status_list != None ) and ( len( result_IN.status_list ) >= 0 ) ):

            # there is.  Append code and result's URL.
            result_IN.status_list.append( code_IN )
            result_IN.url_list.append( result_IN.geturl() )

        else:

            # there is not.  Initialize then append values.

            # status list.
            result_IN.status_list = []
            result_IN.status_list.append( code_IN )

            # url list.
            result_IN.url_list = []
            result_IN.url_list.append( result_IN.geturl() )

        #-- END check to see if status list --#

        
    #-- END method log_redirect_info() --#
    

#-- END class SmartRedirectHandler --#