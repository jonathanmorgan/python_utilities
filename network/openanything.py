from __future__ import unicode_literals

'''
OpenAnything: a kind and thoughtful library for HTTP web services

This program is part of 'Dive Into Python', a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Downloaded from: http://www.diveintopython.net/download/diveintopython-examples-5.4.zip

2013-07-11 - Jonathan Morgan - updated so that RedirectHandler appends each
   status to a list, instead of just storing most recent, in case of multiple
   redirects.

Usage:

# imports

#import urllib2
from six.moves import urllib

#import httplib
from six.moves import http_client
from six.moves.urllib.request import build_opener
from six.moves.urllib.request import Request

from python_utilities.http.openanything import SmartRedirectHandler

# set debug level so it outputs details as it connects.
http_client.HTTPConnection.debuglevel = 1

# create request for a URL (must include a protocol - http://, etc.).
request = Request( 'http://wbez.org' )

# make an opener, passing it an instance of our SmartRedirectHandler()
opener = build_opener( SmartRedirectHandler() )

# open the URL
open_result = opener.open(request)

# if redirected, there will be a status attribute
if ( hasattr( open_result, "status_list" ) == True ):

    # redirected - list of statuses from redirects will be in open_result.status_list.
    print( str( open_result.status_list ) )
    
#-- END check to see if redirect --#

# final URL will be in open_result.url
print( "- Final URL = " + open_result.url )
'''

__author__ = 'Mark Pilgrim (mark@diveintopython.org)'
__version__ = '$Revision: 1.6 $'[11:-2]
__date__ = '$Date: 2004/04/16 21:16:24 $'
__copyright__ = 'Copyright (c) 2004 Mark Pilgrim'
__license__ = 'Python'

# python standard library imports
import gzip

#=============
# six imports
#=============

#import urllib2, urlparse
from six.moves import urllib
from six.moves.urllib.request import build_opener
from six.moves.urllib.request import HTTPRedirectHandler
from six.moves.urllib.request import HTTPDefaultErrorHandler
from six.moves.urllib.request import Request

#from StringIO import StringIO
from six import StringIO

USER_AGENT = 'OpenAnything/%s +http://diveintopython.org/http_web_services/' % __version__

class SmartRedirectHandler( HTTPRedirectHandler ):


    def http_error_301(self, req, fp, code, msg, headers):

        # return reference
        result = None

        result = HTTPRedirectHandler.http_error_301( self, req, fp, code, msg, headers )

        # log redirect info.
        self.log_redirect_info( result, code )

        return result
        
    #-- END method http_error_301() --#


    def http_error_302(self, req, fp, code, msg, headers):

        # return reference
        result = None

        result = HTTPRedirectHandler.http_error_302( self, req, fp, code, msg, headers )
        
        # log redirect info.
        self.log_redirect_info( result, code )

        return result

    #-- END method http_error_302() --#


    def log_redirect_info( self, result_IN, code_IN, *args, **kwargs ):
        
        # First, check to see if there is already a status_list.
        if ( ( hasattr( result_IN, "status_list" ) == True ) and ( result_IN.status_list ) and ( result_IN.status_list != None ) and ( len( result_IN.status_list ) >= 0 ) ):

            # there is.  Append code and result's URL.
            result_IN.status_list.append( code_IN )
            result_IN.url_list.append( result_IN.url )

        else:

            # there is not.  Initialize then append values.

            # status list.
            result_IN.status_list = []
            result_IN.status_list.append( code_IN )

            # url list.
            result_IN.url_list = []
            result_IN.url_list.append( result_IN.url )

        #-- END check to see if status list --#

        
    #-- END method log_redirect_info() --#
    

#-- END class SmartRedirectHandler --#

class DefaultErrorHandler( HTTPDefaultErrorHandler ):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

def openAnything(source, etag=None, lastmodified=None, agent=USER_AGENT):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    If the etag argument is supplied, it will be used as the value of an
    If-None-Match request header.

    If the lastmodified argument is supplied, it must be a formatted
    date/time string in GMT (as returned in the Last-Modified header of
    a previous request).  The formatted date/time will be used
    as the value of an If-Modified-Since request header.

    If the agent argument is supplied, it will be used as the value of a
    User-Agent request header.
    """

    if hasattr(source, 'read'):
        return source

    if source == '-':
        return sys.stdin

    if urllib.urlparse(source)[0] == 'http':
        # open URL with urllib
        request = Request(source)
        request.add_header('User-Agent', agent)
        if lastmodified:
            request.add_header('If-Modified-Since', lastmodified)
        if etag:
            request.add_header('If-None-Match', etag)
        request.add_header('Accept-encoding', 'gzip')
        opener = build_opener( SmartRedirectHandler(), DefaultErrorHandler() )
        return opener.open(request)
    
    # try to open with native open function (if source is a filename)
    try:
        return open(source)
    except (IOError, OSError):
        pass

    # treat source as string
    return StringIO(str(source))

def fetch(source, etag=None, lastmodified=None, agent=USER_AGENT):
    '''Fetch data and metadata from a URL, file, stream, or string'''
    result = {}
    f = openAnything(source, etag, lastmodified, agent)
    result['data'] = f.read()
    if hasattr(f, 'headers'):
        # save ETag, if the server sent one
        result['etag'] = f.headers.get('ETag')
        # save Last-Modified header, if the server sent one
        result['lastmodified'] = f.headers.get('Last-Modified')
        if f.headers.get('content-encoding') == 'gzip':
            # data came back gzip-compressed, decompress it
            result['data'] = gzip.GzipFile(fileobj=StringIO(result['data'])).read()
    if hasattr(f, 'url'):
        result['url'] = f.url
        result['status'] = 200
    if hasattr(f, 'status'):
        result['status'] = f.status
    f.close()
    return result
    
