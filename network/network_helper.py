from __future__ import unicode_literals

'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

python_utilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/python_utilities. If not, see http://www.gnu.org/licenses/.

Usage:

# import
from python_utilities.network.network_helper import Network_Helper

# make network helper instance
network_helper = Network_Helper()

# parse URL, just getting the canonical domain (no subdomains, not even "www.").
test_url = "http://www.nytimes.com/2013/07/16/us/politics/democrats-seeing-precedent-press-on-to-curb-filibuster.html?hp&_r=0"
domain = network_helper.parse_URL( test_url, Network_Helper.URL_PARSE_RETURN_TRIMMED_DOMAIN )

# output
print( domain ) # "nytimes.com"

# parse path, don't re-parse, just re-use last result
path = network_helper.parse_URL( test_url, Network_Helper.URL_PARSE_RETURN_PATH, use_last_parse_result = True )

# output
print( path ) # "/2013/07/16/us/politics/democrats-seeing-precedent-press-on-to-curb-filibuster.html"

# also, after a parse, the full urlparse parse result is stored in
#    network_helper.latest_parse_result
parse_result = network_helper.latest_parse_result

# output
print( parse_result ) # ParseResult(scheme='http', netloc='www.nytimes.com', path='/2013/07/16/us/politics/democrats-seeing-precedent-press-on-to-curb-filibuster.html', params='', query='hp&_r=0', fragment='')

Params are appended to the end of the page name, delimited by semi-colons.

Doc: http://stackoverflow.com/questions/10988614/what-are-the-url-parameters-element-at-position-3-in-urlparse-result

Example:
- http://some.page.pl/nothing.py;someparam=some;otherparam=other?query1=val1&query2=val2#frag
- print the result of parsing:
    ParseResult(scheme='http', netloc='some.page.pl', path='/nothing.py', params='someparam=some;otherparam=other', query='query1=val1&query2=val2', fragment='frag')
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# python libraries
import re

# six for python 2 and 3 support
import six

# import urlparse
from six.moves.urllib.parse import urlparse

#================================================================================
# class Http_Helper
#================================================================================

class Network_Helper( object ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "
    
    # DEBUG - changed to instance variable.
    #DEBUG_FLAG = False

    # URL parse return types
    URL_PARSE_RETURN_TRIMMED_DOMAIN = "trimmed_domain"
    URL_PARSE_RETURN_PATH = "path"
    URL_PARSE_RETURN_ALL_AFTER_DOMAIN = "all_after_domain"
    URL_PARSE_RETURN_RESULT_OBJECT = "result_object"

    
    #============================================================================
    # instance variables
    #============================================================================


    # debug_flag
    debug_flag = False
    
    # latest result
    latest_parse_result = None
    
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # debug
        self.debug_flag = False
        
        # latest parse result
        self.latest_parse_result = None

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================


    def parse_URL( self,
                   URL_IN = "",
                   return_type_IN = URL_PARSE_RETURN_RESULT_OBJECT,
                   use_last_parse_result_IN = False,
                   assume_http_IN = True,
                   *args,
                   **kwargs ):
        
        '''
        Accepts URL, return type, and optional flag to tell whether to use
           last parse result or force new parse (defaults to new parse every
           time).  Uses urlparse library to parse the URL, then plucks the
           requested piece from the results and returns it.
           
        Return type:
        - URL_PARSE_RETURN_TRIMMED_DOMAIN - "trimmed_domain" - returns the domain name, and removes "www." or "m." if they are on the front of the domain.
        - URL_PARSE_RETURN_PATH - "path" - returns just the path of the URL, no query string included.
        - URL_PARSE_RETURN_ALL_AFTER_DOMAIN - "all_after_domain" - returns the entire URL after the domain, including path, params, query string, and fragment (#<link name>, used, for example, for within-page navigation in web pages).
        - URL_PARSE_RETURN_RESULT_OBJECT - "result_object" - default - returns the object that results from parsing, not just one piece or another.
        '''

        # return reference
        value_OUT = ""
        
        # declare variables
        me = "parse_URL"
        url_to_parse = ""
        parse_result = None
        url_scheme = ""
        params = ""
        query_string = ""
        fragment_string = ""
        status_message = ""
        
        # got a URL?
        if ( ( URL_IN ) and ( URL_IN != None ) and ( URL_IN != "" ) ):
        
            # parse
            parse_result = self.parse_URL_string( URL_IN = URL_IN, use_last_parse_result_IN = use_last_parse_result_IN )

            # check if there was a scheme detected.
            url_scheme = parse_result.scheme
            if ( ( not url_scheme ) or ( url_scheme == None ) or ( url_scheme == "" ) ):
            
                # no URL scheme - do we assume HTTP?
                if ( assume_http_IN == True ):
                
                    # we do.  Are we asked to use last parse result?
                    if ( use_last_parse_result_IN == False ):
                    
                        # no - OK to change URL, reparse.  Append "http://" to
                        #    the front of the string, parse again.
                        url_to_parse = "http://" + URL_IN

                        # status
                        status_message = "In " + me + "(): Adding http:// to URL - " + url_to_parse
                
                        # parse again.
                        parse_result = self.parse_URL_string( URL_IN = url_to_parse, use_last_parse_result_IN = False )
                        
                    else:
                    
                        # we are not assuming HTTP.
                        status_message = "In " + me + "(): We are using last parse result, so not doing anything about missing scheme."
                
                    #-- END check to see if it is OK to change string and re-parse --#
                
                else:
                
                    # we are not assuming HTTP.
                    status_message = "In " + me + "(): We are not assuming HTTP, so not doing anything about missing scheme."
            
                #-- END check to see if we assume HTTP. --#
            
            else:
            
                # there is a URL scheme.
                status_message = "In " + me + "(): There is a URL Scheme - " + url_scheme
            
            #-- END check to see if URL scheme. --#
            
            # create output based on return type - see what we've been asked to
            #    return.
            if ( return_type_IN == self.URL_PARSE_RETURN_PATH ):
            
                # path - "path" in result.
                value_OUT = parse_result.path
                
                # is path just "/"?  If so, set to "".
                #if ( value_OUT == "/" ):
                
                    # yup. Set to "".
                    #value_OUT = ""
                
                #-- END check to see if path is just "/" --#

            elif ( return_type_IN == self.URL_PARSE_RETURN_ALL_AFTER_DOMAIN ):
            
                # path - "path" in result.
                value_OUT = parse_result.path
                            
                # params?
                params = parse_result.params
                if ( ( params ) and ( params != None ) and ( params != "" ) ):
                
                    # yes.  append a semicolon, then the params.
                    value_OUT += ";" + params
                
                #-- END check to see if params. --#
                
                # query_string
                query_string = parse_result.query
                if ( ( query_string ) and ( query_string != None ) and ( query_string != "" ) ):
                
                    # yes.  append a question mark, then the query_string.
                    value_OUT += "?" + query_string
                
                #-- END check to see if params. --#
                
                # fragment_string - how within-page links are passed.
                fragment_string = parse_result.fragment
                if ( ( fragment_string ) and ( fragment_string != None ) and ( fragment_string != "" ) ):
                
                    # yes.  append a pound, then the fragment_string.
                    value_OUT += "#" + fragment_string
                
                #-- END check to see if params. --#
                
            elif ( return_type_IN == self.URL_PARSE_RETURN_RESULT_OBJECT ):
            
                # just return the result.
                value_OUT = parse_result

            # default is trimmed domain, including for unknown value.
            else:
            
                # domain - "netloc" in result.
                value_OUT = parse_result.netloc
                
                # do a little more cleanup - place the URL in domain_name
                value_OUT = value_OUT.strip()
                
                # strip off leading "www."
                value_OUT = re.sub( r'^www\.', '', value_OUT )
                
                # strip off leading "m."
                value_OUT = re.sub( r'^m\.', '', value_OUT )

            #-- END check to see what we return. --#
            
        else:
        
            value_OUT = ""
        
        #-- END check to see if URL --#

        #if ( ( status_message ) and ( status_message != None ) and ( status_message != "" ) ):

        #    print( status_message )
        
        #-- END check to see if status message to output. --#

        return value_OUT
        
    #-- END method parse_URL() --#


    def parse_URL_string( self,
                          URL_IN = "",
                          use_last_parse_result_IN = False,
                          *args,
                          **kwargs ):
        
        '''
        Accepts URL and optional flag to tell whether to use last parse result
           or force new parse (defaults to new parse every time).  Uses urlparse
           library to parse the URL, stores result, then returns it.
        '''

        # return reference
        value_OUT = None
        
        # declare variables
        parse_result = None
        
        # got a URL?
        if ( ( URL_IN ) and ( URL_IN != None ) and ( URL_IN != "" ) ):
        
            # use urlparse to parse?
            if ( use_last_parse_result_IN == False ):
            
                # don't use last parse result - parse anew.
                parse_result = urlparse( URL_IN )
                
                # store the result
                self.latest_parse_result = parse_result
                
            #-- END check to see if we parse anew. --#
            
            # return latest parse result.
            value_OUT = self.latest_parse_result
            
        else:
        
            value_OUT = None
        
        #-- END check to see if URL --#

        return value_OUT
        
    #-- END method parse_URL_string() --#


#-- END class Http_Helper --#