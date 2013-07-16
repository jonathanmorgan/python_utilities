'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

python_utilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/python_utilities. If not, see http://www.gnu.org/licenses/.

Usage:

# import
from python_utilities.network.http_helper import Http_Helper

# make an instance.
my_http_helper = Http_Helper()

# try a URL to see if it redirects.
redirect_url = my_http_helper.get_redirect_url( "http://wbez.org" )

# If not None, then redirected.
if ( redirect_url != None ):

    # print out details:
    print( redirect_url ) # 'http://www.wbez.org/'
    print( str( my_http_helper.redirect_status_list ) ) # [301]
    print( str( my_http_helper.redirect_url_list ) ) # ['http://www.wbez.org/']

#-- END check to see if redirected --#
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

import urllib2
import openanything

#================================================================================
# class Http_Helper
#================================================================================

class Http_Helper( object ):


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


    # redirect statuses
    redirect_status_list = []
    redirect_url_list = []
    
    # debug_flag
    debug_flag = False
    
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # redirect statuses
        self.redirect_status_list = []
        self.redirect_url_list = []
    
        # debug
        self.debug_flag = False

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def get_redirect_url( self, url_IN, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page.  If page loads, checks to see if
           redirect. If yes, returns URL to which we were redirected and stores
           the list of redirect codes in self.redirect_status_list.  If no,
           returns None.
        '''
    
        # return reference
        url_OUT = None
    
        # declare variables.
        request = None
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # create request for a URL (must include a protocol - http://, etc.).
            request = urllib2.Request( 'http://wbez.org' )
        
            # make an opener, passing it an instance of our SmartRedirectHandler()
            opener = urllib2.build_opener( openanything.SmartRedirectHandler() )
            
            # open the URL
            open_result = opener.open(request)
            
            # if redirected, there will be a status_list attribute
            if ( hasattr( open_result, "status_list" ) == True ):
            
                # redirected - list of statuses from redirects will be in
                #    open_result.status_list - store it.
                self.redirect_status_list = open_result.status_list
                
                # redirected - list of urls of redirects will be in
                #    open_result.url_list - store it.
                self.redirect_url_list = open_result.url_list
                
                # return URL from result
                url_OUT = open_result.url
                
            else:
            
                # no redirect.  Return None.
                url_OUT = None
            
            #-- END check to see if redirect --#
            
        else:
        
            # No URL passed in, return None.
            url_OUT = None
        
        #-- END check to see of URL string passed in. --#            
                
        return url_OUT
    
    #-- END methot get_redirect_url --#    


#-- END class Http_Helper --#