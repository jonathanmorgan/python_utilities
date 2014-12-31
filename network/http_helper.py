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

# make a POST request using Http_Helper.
my_http_helper = Http_Helper()

# set up call to REST API.
calais_REST_API_URL = "http://api.opencalais.com/tag/rs/enrich"
calais_api_key = "<insert_calais_API_key_here>"
my_http_helper.set_http_header( "x-calais-licenseID", calais_api_key, None )
my_http_helper.set_http_header( "Content-Type", "TEXT/RAW", None )
my_http_helper.set_http_header( "outputformat", "Application/JSON", None )

# request type
my_http_helper.request_type = Http_Helper.REQUEST_TYPE_POST

# make the request.
requests_response = my_http_helper.load_url_requests( calais_REST_API_URL, data_IN = article_body_text )

'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# python libraries
import urllib2

# mechanize
import mechanize

# python_utilites.network
import mechanize_tools
import openanything

# import requests
import requests

# python_utilites DictHelper
from python_utilities.dictionaries.dict_helper import DictHelper

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
    HEADER_NAME_USER_AGENT = "User-Agent"
    HEADER_NAME_ACCEPT = "Accept"
    HEADER_NAME_ACCEPT_CHARSET = "Accept-Charset"
    HEADER_NAME_ACCEPT_ENCODING = "Accept-Encoding"
    HEADER_NAME_ACCEPT_LANGUAGE = "Accept-Language"
    HEADER_NAME_CONNECTION = "Connection"
    
    # request types
    REQUEST_TYPE_GET = "get"
    REQUEST_TYPE_POST = "post"
    REQUEST_TYPE_DEFAULT = REQUEST_TYPE_GET

    #============================================================================
    # instance variables
    #============================================================================


    # redirect statuses
    redirect_status_list = []
    redirect_url_list = []
    
    # HTTP header values
    header_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"
    header_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_accept_charset = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
    header_accept_encoding = 'none'
    header_accept_language = 'en-US,en;q=0.8'
    header_connection = 'keep-alive'
    
    # header dict
    header_dict = None
    
    # request_type
    request_type = None

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
    
        # HTTP header values
        self.header_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"
        self.header_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.header_accept_charset = 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
        self.header_accept_encoding = 'none'
        self.header_accept_language = 'en-US,en;q=0.8'
        self.header_connection = 'keep-alive'
        
        # initialize header dict
        self.initialize_header_dict()
        
        # request_type
        request_type = self.REQUEST_TYPE_DEFAULT
    
        # debug
        self.debug_flag = False

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def get_http_header( self, name_IN, default_IN = None, *args, **kwargs ):
        
        '''
        Accepts a header name.  If name is populated (not None and not ""),
           returns value for that header. If no name, returns nothing.
        
        Parameters:
        - name_IN - name of name-value HTTP header variable you want to retrieve.
        - default_IN - default value in case the variable is not present in the header dict.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_header_dict = None
        
        # get header dict
        my_header_dict = self.get_http_header_dict()
        
        # try to retrieve header value.
        value_OUT = DictHelper.get_dict_value( my_header_dict, name_IN, default_IN )

        return value_OUT
        
    #-- END method get_http_header() --#


    def get_http_header_dict( self, header_dict_IN = None, *args, **kwargs ):
        
        '''
        Accepts a set of header params in a dict.  Looks for a pre-existing dict
           in this instance.  If one present, retrieves it.  If not, creates one.
           If creating a new header dict, first initializes values from header
           variables in this instance.  Then, if dict passed in, places those
           values in the dict, overwriting any that are both in the nested set
           and in the set passed in with those passed in.  Stores the resulting
           dict, and returns it.
           
        If you want to alter the defaults, you have two options - you can either
           change the values in the "header_*" variables, or you can create a
           dict to hold your values and pass that to this method.  If you want to
           set values not stored in "header_*" variables, then you'll have to
           either pass in a header dict or just craft your header dict as you
           want it and store it in the header_dict instance variable in this
           instance.
        
        Parameters:
        - header_dict_IN - set of name-value HTTP header variables you want added to the header dict that is returned.
        '''
        
        # return reference
        dict_OUT = None
        
        # see if there is already a header dict nested.
        if ( ( self.header_dict ) and ( self.header_dict != None ) and ( len( self.header_dict ) > 0 ) ):
        
            # we have one.  Return it.
            dict_OUT = self.header_dict
        
        else:
        
            # nothing.  Initialize a new one.
            self.initialize_header_dict( header_dict_IN )
            
            # return what results.
            dict_OUT = self.header_dict

        #-- END check to see if header dict exists. --#
        
        return dict_OUT
        
    #-- END method get_http_header_dict() --#


    def get_redirect_url( self, url_IN, *args, **kwargs ):
    
        '''
        method defaults to calling mechanize methods, not urllib2.  If this
           becomes a problem, could do fancy things here to choose which is
           called.
        '''
        
        # return reference
        url_OUT = ""
        
        # call method implementation.
        url_OUT = self.get_redirect_url_mechanize( url_IN, args, kwargs )
        
        return url_OUT
        
    #-- END method get_redirect_url() --#
    


    def get_redirect_url_urllib2( self, url_IN, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page.  If page loads, checks to see if
           redirect. If yes, returns URL to which we were redirected and stores
           the list of redirect codes in self.redirect_status_list.  If no,
           returns None.  If there is an error loading the page, will throw an
           exception.  Return of None DOES NOT imply error in this case.
        '''
    
        # return reference
        url_OUT = None
    
        # declare variables.
        headers = None
        request = None
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # load the URL
            open_result = self.load_url_urllib2( url_IN, args, kwargs )
            
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
    
    #-- END methot get_redirect_url_urllib2 --#    


    def get_redirect_url_mechanize( self, url_IN, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page.  If page loads, checks to see if
           redirect. If yes, returns URL to which we were redirected and stores
           the list of redirect codes in self.redirect_status_list.  If no,
           returns None.  If there is an error loading the page, will throw an
           exception.  Return of None DOES NOT imply error in this case.
        '''
    
        # return reference
        url_OUT = None
    
        # declare variables.
        request = None
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # load URL
            open_result = self.load_url_mechanize( url_IN, args, kwargs )
            
            # if redirected, there will be a status_list attribute
            if ( hasattr( open_result, "status_list" ) == True ):
            
                # redirected - list of statuses from redirects will be in
                #    open_result.status_list - store it.
                self.redirect_status_list = open_result.status_list
                
                # redirected - list of urls of redirects will be in
                #    open_result.url_list - store it.
                self.redirect_url_list = open_result.url_list
                
                # return URL from result
                url_OUT = open_result.geturl()
                
            else:
            
                # no redirect.  Return None.
                url_OUT = None
            
            #-- END check to see if redirect --#
            
        else:
        
            # No URL passed in, return None.
            url_OUT = None
        
        #-- END check to see of URL string passed in. --#            
                
        return url_OUT
    
    #-- END methot get_redirect_url_mechanize --#    


    def get_redirect_url_requests( self, url_IN, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page.  If page loads, checks to see if
           redirect. If yes, returns URL to which we were redirected and stores
           the list of redirect codes in self.redirect_status_list.  If no,
           returns None.  If there is an error loading the page, will throw an
           exception.  Return of None DOES NOT imply error in this case.
        '''
    
        # return reference
        url_OUT = None
    
        # declare variables.
        headers = None
        request = None
        opener = None
        open_result = None
        history_response = None
        history_status_list = []
        history_url_list = []
        history_status = ""
        history_url = ""
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # load the URL
            open_result = self.load_url_requests( url_IN, args, kwargs )
            
            # if redirected, there will be a status_list attribute
            if ( len( open_result.history ) > 0 ):
            
                # redirected - list of requests responses from redirects will be
                #    in open_result.history - loop, making list of statuses and
                #    urls.
                history_status_list = []
                history_url_list = []
                for history_response in open_result.history:
                
                    # get status, url from response.
                    history_status = history_response.status_code
                    history_url = history_response.url
                    
                    # add to lists
                    history_status_list.append( history_status )
                    history_url_list.append( history_url )

                #-- END loop over history --#
                
                # store history lists.
                self.redirect_status_list = history_status_list
                self.redirect_url_list = history_url_list
                
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
    
    #-- END methot get_redirect_url_requests --#    


    def initialize_header_dict( self, header_dict_IN = None, *args, **kwargs ):
        
        '''
        Creates a new dict instance, stores default header values in it, then
           stores the resulting instance inside this instance.  Returns a
           reference to the dict.
        '''
        
        # return reference
        dict_OUT = {}
        
        # declare variables
        
        # nothing.  Make a new one.
        dict_OUT = {}
        dict_OUT[ self.HEADER_NAME_USER_AGENT ] = self.header_user_agent
        dict_OUT[ self.HEADER_NAME_ACCEPT ] = self.header_accept
        dict_OUT[ self.HEADER_NAME_ACCEPT_CHARSET ] = self.header_accept_charset
        dict_OUT[ self.HEADER_NAME_ACCEPT_ENCODING ] = self.header_accept_encoding
        dict_OUT[ self.HEADER_NAME_ACCEPT_LANGUAGE ] = self.header_accept_language
        dict_OUT[ self.HEADER_NAME_CONNECTION ] = self.header_connection
            
        # Got a dict of values passed in?
        if ( ( header_dict_IN ) and ( header_dict_IN != None ) and ( len( header_dict_IN ) > 0 ) ):

            # got one.  Put its data in the dict we are passing out.
            dict_OUT.update( header_dict_IN )
            
        #-- END check to see if header dict passed in. --#
        
        # store in instance
        self.set_http_header_dict( dict_OUT )
        
        return dict_OUT
    
    #-- END method initialize_header_dict() --#


    def load_url( self, url_IN, *args, **kwargs ):
    
        '''
        method defaults to calling mechanize methods, not urllib2.  If this
           becomes a problem, could do fancy things here to choose which is
           called.
        '''
        
        # return reference
        response_OUT = ""
        
        # call method implementation.
        response_OUT = self.load_url_mechanize( url_IN, args, kwargs )
        
        return response_OUT
        
    #-- END method load_url() --#
    


    def load_url_urllib2( self, url_IN, post_data_IN = None, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page using the urllib2 package.  If
           page loads, returns response.  If not, returns None.
        '''
    
        # return reference
        response_OUT = None
    
        # declare variables.
        headers = None
        request = None
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # get header dict
            headers = self.get_http_header_dict()

            # create request for a URL (must include a protocol - http://, etc.).
            request = urllib2.Request( url_IN, post_data_IN, headers )
        
            # make an opener, passing it an instance of our SmartRedirectHandler()
            opener = urllib2.build_opener( openanything.SmartRedirectHandler() )
            
            # open the URL
            response_OUT = opener.open(request)
            
        else:
        
            # No URL passed in, return None.
            response_OUT = None
        
        #-- END check to see of URL string passed in. --#            
                
        return response_OUT
    
    #-- END methot load_url_urllib2 --#    


    def load_url_mechanize( self, url_IN, post_data_IN = None, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page using the mechanize package.  If
           page loads, returns response.  If not, returns None.
        '''
    
        # return reference
        response_OUT = None
    
        # declare variables.
        request = None
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # get header dict
            headers = self.get_http_header_dict()

            # create request for a URL (must include a protocol - http://, etc.).
            request = mechanize.Request( url_IN, post_data_IN, headers )
        
            # make an opener, passing it an instance of our SmartRedirectHandler()
            opener = mechanize.build_opener( mechanize_tools.SmartRedirectHandler() )
            
            # open the URL
            response_OUT = opener.open( request )
            
        else:
        
            # No URL passed in, return None.
            response_OUT = None
        
        #-- END check to see of URL string passed in. --#            
                
        return response_OUT
    
    #-- END methot load_url_mechanize --#
    
    
    def load_url_requests( self, url_IN, request_type_IN = "", data_IN = None, *args, **kwargs ):
    
        '''
        Accepts a URL.  Tries to load that page using the "requests" HTTP
           package: http://docs.python-requests.org/en/latest/
        If page loads, returns response.  If not, returns None.
        '''
    
        # return reference
        response_OUT = None
    
        # declare variables.
        my_request_type = ""
        opener = None
        open_result = None
        
        # got a url?
        if ( ( url_IN ) and ( url_IN != None ) and ( url_IN != "" ) ):

            # get request_type
            my_request_type = request_type_IN
            if ( ( my_request_type == None ) or ( my_request_type == "" ) ):
            
                # no request type passed in.  Use what is in instance.
                my_request_type = self.request_type
            
            #-- END check to see if we have a request type. --#
            
            # get header dict
            headers = self.get_http_header_dict()
            
            # what type of request?
            if ( my_request_type == self.REQUEST_TYPE_GET ):
            
                # get.
                response_OUT = requests.get( url_IN, headers = headers, params = data_IN )
            
            elif ( my_request_type == self.REQUEST_TYPE_POST ):

                # post.
                response_OUT = requests.post( url_IN, headers = headers, data = data_IN )
            
            else:
            
                # Nothing to see here - set to None.
                response_OUT = None
            
            #-- END check to see what type of request.

        else:
        
            # No URL passed in, return None.
            response_OUT = None
        
        #-- END check to see of URL string passed in. --#            
                
        return response_OUT
    
    #-- END methot load_url_requests --#
    
    
    def set_http_header( self, name_IN, value_IN = None, *args, **kwargs ):

        '''
        Accepts name and value of header variable to set in the header variable
           dict in this instance.  If no name, does nothing.  If name, sets
           header for that name to the value passed in.  Returns the value, or
           None on error.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        my_header_dict = None
        
        # is there a name?
        if ( ( name_IN != None ) and ( name_IN != "" ) ):
        
            # yes, there is a name.  get header dict
            my_header_dict = self.get_http_header_dict()
            
            # set the header.
            my_header_dict[ name_IN ] = value_IN
            
            # re-store the header dict
            #self.set_http_header_dict( my_header_dict )
            
            # return value passed in.
            value_OUT = value_IN
        
        else:
        
            # no name - return None.
            value_OUT = None

        #-- END check to see if name. --#

        return value_OUT

    #-- END method set_http_header() --#


    def set_http_header_dict( self, dict_IN = None, *args, **kwargs ):

        '''
        Accepts a dict of header variables, stores the dict in this instance.
        '''
        
        # store the dict passed in.
        self.header_dict = dict_IN

    #-- END method set_http_header_dict() --#


#-- END class Http_Helper --#