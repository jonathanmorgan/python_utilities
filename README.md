# python\_utilities

<!-- TOC -->

Python Utility classes.  Includes the following files:

- __/beautiful\_soup/__
    - __/beautiful\_soup/beautiful\_soup\_helper.py__ - `BeautifulSoupHelper` class that implements helper methods for common things you do with BeautifulSoup, like getting child text and encoding HTML entities.  Built against BeautifulSoup 3, updated to import BeautifulSoup 4, work just fine far as I can tell...
- __/booleans/__
    - __/booleans/boolean\_helper.py__ - `BooleanHelper` class with method to convert non-boolean values to boolean type based on valid known true values (1, 't', 'true', 'y', 'yes').
- __/database__
    - __/database/database\_helper\_factory.py__ - `Database_Helper_Factory` class provides a class method you can use to pull in either a postgresql or mysql database helper, so you can write code that functions the same way for either, allowing easier switching between the two.
    - __/database/database\_helper.py__ - `Database_Helper` abstract class encapsulates basic logic for dealing with creating connections and cursors using a Python DB API library.  Not fancy.  Opens, creates cursors and keeps track of all cursors it creates, and closes all related cursors and connection when you call close().  Nothing more.
    - __/database/psycopg2\_helper.py__ - `psycopg2_Helper` class encapsulates basic logic for dealing with creating connections and cursors using the psycopg2 library.  Not fancy.  Opens and closes, nothing more.
    - __/database/MySQLdb\_helper.py__ - `MySQLdb_Helper` class encapsulates basic logic for dealing with creating connections and cursors using the MySQLdb library.  Not fancy.  Opens and closes, nothing more.
- __/dictionaries/__
    - __/dictionaries/dict\_helper.py__ - `DictHelper` class contains a function to retrieve a dict values as strings, integers, and lists that also accept a default, so you can convert to types and define default yourself when you look things up in a dict.
- __/django\_utils/__
    - __/django\_utils/django\_memory\_helper.py__ - for now, has a class `DjangoMemoryHelper` with a single class method, `free_memory()`, that does everything I know how to do to free up memory in django while a long-running process is running.
    - __/django\_utils/django\_string\_helper.py__ - extends `StringHelper` class from `strings/string_helper.py`, updating the `convert_to_unicode()` method to use Django's built-in method.
    - __/django\_utils/query\_filter.py__ - `QueryFilterHelper` class, just extends `QuerySetHelper` for backward compatibility.
    - __/django\_utils/queryset\_helper.py__ - `QuerySetHelper` class that contains memory-efficient ways of iterating over large QuerySets, and also a few convenience methods for adding date and primary key filters to a QuerySet.
- __/email/__
    - __/email/email\_helper.py__ - `EmailHelper` class that contains logic for setting up SMTP server using smtplib, then sending text or HTML email messages.
- __/exceptions/__
    - __/exceptions/exception\_helper.py__ - `ExceptionHelper` class that contains logic for printing exception messages, and also for emailing a summary if email is set up in the isntance.
- __/logging/__
    - __/logging/summary\_helper.py__ - `SummaryHelper` class that contains logic for capturing and outputting timing and auditing information.
- __/network__
    - __/network/http\_helper.py__ - `Http_Helper` class that contains logic for checking if a URL has been redirected, and if so, storing redirect information including status code and redirect URLs.
    - __/network/mechanize\_tools.py__ - Contains `SmartRedirectHandler` class that enables mechanize to keep track of all redirect hops taken from URL to resolved URL, with logic to support `Http_Helper`, based on the Dive Into Python site (http://www.diveintopython.net/download/diveintopython-examples-5.4.zip), but using Mechanize's version of urllib2.
    - __/network/network\_helper.py__ - `Network_Helper` class contains instance methods for parsing URL strings and plucking out different known, standard pieces (domain, trimmed domain, just path - no query string, and everything after the domain).
    - __/network/openanything.py__ - Contains `SmartRedirectHandler` class that keeps track of redirect hops for urllib2, logic to support Http_Helper, from the Dive Into Python site (http://www.diveintopython.net/download/diveintopython-examples-5.4.zip)
- __/objects/__
    - __/objects/object\_helper.py__ - `ObjectHelper` class contains logic for detecting attributes in a given class (like the vars() method, only a little fancier).
- __/parameters/__
    - __/parameters/param\_container.py__ - `ParamContainer` class contains logic for defining, loading, accessing, and outputting parameters stored in a dictionary.
- __/rate\_limited/__
    - __/rate\_limited/basic\_rate\_limited.py__ - `BasicRateLimited` is a non-parallel parent class that contains variables and code for rate-limiting.  Details on extending TK below, in Usage Section.
- __/strings/__
    - __/strings/html\_helper.py__ - `HTMLHelper` class to help with parsing and dealing with HTML strings.  Right now, has one static method, `remove_html()`, that removes HTML from a string, allowing for a list of HTML elements you want left in, and within those elements, a list of attributes you want left in.  If something is not in one of those lists, it will be removed.
    - __/strings/string\_helper.py__ - `StringHelper` class with methods to help with unicode encoding, stripping HTML from strings.

## Installation

Clone this repository and place it somewhere in your PYTHON\_PATH, including the base "python\_utilities" directory.  The easiest way to use these libraries with a Django site is to clone this repository into the site's folder alongside other applications, so these utilities are a part of the same python path as other django apps.  These utilities are used by other of my django applications, as well.  They can also be used outside of django.

Dependencies are listed below.  You can install them individually, or you can just use the `requirements.txt` file, which lists them all out, to install them all at once using pip.  The command:

    (sudo) pip install -r python_utilities/requirements.txt
    
For database packages, you'll likely want to go into the requirements.txt and remove packages for databases you don't have installed on your system, either `MySQL-python` or `psycopg2` (or both).

### /beautiful\_soup/*

Requires the Beautiful Soup 4 package, installed via pip:

    (sudo) pip install BeautifulSoup4
    
If you are planning on using Beautiful Soup's "UnicodeDammit" class, you also should install chardet and/or cchardet:

    (sudo) pip install chardet
    (sudo) pip install cchardet
    
### /strings/html_helper.py

requires bleach, a library for selectively parsing HTML and XML:

    (sudo) pip install bleach

and requires the Beautiful Soup 4 package, installed via pip:

    (sudo) pip install BeautifulSoup4
    
### /database/MySQLdb\_helper.py

Before you can connect to MySQL with this code, you need to do the following:

- install the MySQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libmysqlclient-dev) ( [source](http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/) ).

- install the MySQLdb python package.  To install, you can either install through your operating system's package manager (ubuntu, for example, has package "python-mysqldb") or using pip (`sudo pip install MySQL-python`).

### /database/psycopg2\_helper.py

Before you can connect to Postgresql with this code, you need to do the following (based on [http://initd.org/psycopg/install/](http://initd.org/psycopg/install/)):

- install the PostgreSQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libpq-dev) ( [source](http://initd.org/psycopg/install/) ).

- install the psycopg2 python package.  Install using pip (`sudo pip install psycopg2`).

### /network/*

Requires you install mechanize, a library that implements a browser client in python, and requests:

    (sudo) pip install mechanize
    (sudo) pip install requests
    
### /strings/*

Requires you to install the "six" package, which helps make python code that can run in either python 2 or 3:

    (sudo) pip install six

## Usage

### /exceptions/exception\_helper.py

For a class you want to use ExceptionHelper for outputting and potentially emailing exception messages:

    # import ExceptionHandler
    from python_utilities.exceptions.exception_helper import ExceptionHelper
    
    # make instance
    my_exception_helper = ExceptionHelper()
    
    # configure mail settings?
    '''
    smtp_host = 'localhost'
    smtp_port = 1234
    smtp_use_ssl = True
    smtp_username = "smtp_user"
    smtp_password = "smtp_pass"
    my_exception_helper.email_initialize( smtp_host, smtp_port, smtp_use_ssl, smtp_username, smtp_password ):
    '''
    
    # log an exception
    try:
    
        pass
    
    catch Exception as e:
    
        # log exception.
        exception_message = "Exception caught for article " + str( current_article.id )
        
        # no email
        my_exception_helper.process_exception( e, exception_message )
        
        # with email
        # my_exception_helper.process_exception( e, exception_message, True, "email_subject" )        

    #-- END try-catch --#

If you are going to be in a long-running or looping process, consider initializing at the beginning and storing instance in a variable, so you can reuse it.

### /logging/summary\_helper.py

How to use the summary helper:

    # import SummaryHelper
    from python_utilities.logging.summary_helper import SummaryHelper
    
    # initialize summary helper - this sets start time, as well.
    my_summary_helper = SummaryHelper()
    
    # auditing variables
    article_counter = -1
    exception_counter = -1
    
    # update the variables
    
    # once you are done:
    
    # set stop time
    my_summary_helper.set_stop_time()

    # add stuff to summary
    my_summary_helper.set_prop_value( "article_counter", article_counter )
    my_summary_helper.set_prop_desc( "article_counter", "Articles processed" )

    my_summary_helper.set_prop_value( "exception_counter", exception_counter )
    my_summary_helper.set_prop_desc( "exception_counter", "Exception count" )

    # output - set prefix if you want.
    summary_string += my_summary_helper.create_summary_string( item_prefix_IN = "==> " )
    print( summary_string )
    
Example output:

    ==> Articles processed: 46
    ==> Exception count: 20
    ==> Start time: 2014-12-31 14:32:28.221066
    ==> End time: 2014-12-31 14:32:41.982753
    ==> Duration: 0:00:13.761687

### /network/mechanize_tools.py

Usage of SmartRedirectHandler to keep track of redirect steps:

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

### /parameters/param\_container.py

Usage:

    # import ParamContainer
    from python_utilities.parameters.param_container import ParamContainer

    # make an instance
    my_param_container = ParamContainer()
    
    # define parameters (for outputting debug, nothing more at this point)
    my_param_container.define_parameter( "test_int", ParamContainer.PARAM_TYPE_INT )
    my_param_container.define_parameter( "test_string", ParamContainer.PARAM_TYPE_STRING )
    my_param_container.define_parameter( "test_list", ParamContainer.PARAM_TYPE_LIST )
    
    # load parameters in a dict
    my_param_container.set_parameters( params )
    
    # load parameters from a django HTTP request
    my_param_container.set_request( request )
    
    # get parameter value - pass name and optional default if not present.
    test_int = my_param_container.get_param( "test_int", -1 )
    test_string = my_param_container.get_param( "test_string", "" )
    test_list = my_param_container.get_param( "test_list", [] )
    
    # get param as int
    test_int = my_param_container.get_param_as_int( "test_int", -1 )

    # get param as str
    test_string = my_param_container.get_param_as_str( "test_string", -1 )

    # get param as list - pass in name, optional default, list delimiter string (defaults to ",")
    test_int = my_param_container.get_param_as_list( "test_int", -1, delimiter_IN = "," )

### /rate\_limited/basic\_rate\_limited.py

For a class you want to be rate-limited:

- have that class import and extend `BasicRateLimited`.

        # import
        from python_utilities.rate_limited.basic_rate_limited import BasicRateLimited
        
        # class definition
        def class SampleClass( BasicRateLimited ):

- in that class's `__init__()` method, call the parent `__init__()` method, then set instance variable `rate_limit_in_seconds` to the minimum number of seconds you want between requests (can be a decimal).

        def __init__( self ):
    
            # call parent's __init__()
            super( SourcenetBase, self ).__init__()
    
            # declare variables
            
            # limit to no more than 4 per second
            self.rate_limit_in_seconds = 0.25
            
        #-- END method __init__() --#

- At the start of each transaction, call the `self.start_request()` method to let the code know you're starting a request.
- Once the request is done, call `continue_collecting = self.may_i_continue()` this method will block if you have to wait, will return true if it is OK to continue, will return False if some error occurred.
- In your control structure, always check the result of `may_i_continue()` before continuing.

## License:

Copyright 2012, 2013 Jonathan Morgan

This file is part of [http://github.com/jonathanmorgan/python\_utilities](http://github.com/jonathanmorgan/python_utilities).

python\_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python\_utilities is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [http://github.com/jonathanmorgan/python\_utilities](http://github.com/jonathanmorgan/python_utilities).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
