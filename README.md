# python\_utilities

_latest_: [![DOI](https://zenodo.org/badge/6323399.svg)](https://zenodo.org/badge/latestdoi/6323399)

v.1.1.1: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6917759.svg)](https://doi.org/10.5281/zenodo.6917759)

v.1.1.0: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5904708.svg)](https://doi.org/10.5281/zenodo.5904708)

v.1.0.2: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4686148.svg)](https://doi.org/10.5281/zenodo.4686148)

v.1.0.1: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3523239.svg)](https://doi.org/10.5281/zenodo.3523239)

<!-- TOC -->

Python utility classes (should work in either Python 2 or 3).  Includes the following files:

- __/analysis/__

    - __/analysis/statistics/confusion_matrix_helper.py__ - helper class `ConfusionMatrixHelper`for working with confusion matrices, usually because you have run a classification model and are trying to assess its quality.
    - __/analysis/statistics/stats_helper.py__ - helper class `StatsHelper` for help with statistics not implemented in a statistical package.  Includes Krippendorff's Alpha, percent agreement, and Potter's Pi, for assessing interrater reliability/agreement.
    - __/analysis/statistics/tests.py__ - unit tests.

- __/bagit/__

    - __/bagit/bagit_python.ipynb__ and __/bagit/bagit_python.py__ - bagit python client example code, same code in both files, one is a jupyter notebook, one is a plain Python file.

- __/beautiful\_soup/__

    - __/beautiful\_soup/beautiful\_soup\_helper.py__ - `BeautifulSoupHelper` class that implements helper methods for common things you do with BeautifulSoup, like getting child text and encoding HTML entities.  Built against BeautifulSoup 3, updated to import BeautifulSoup 4, work just fine far as I can tell...

- __/booleans/__

    - __/booleans/boolean\_helper.py__ - `BooleanHelper` class with method to convert non-boolean values to boolean type based on valid known true values (1, 't', 'true', 'y', 'yes').

- __/data__

    - __/data/data\_functions.py__ - a set of reusable functions for various data tasks that includes pandas, RDBMS, CSV, and SAS processing.

- __/database__

    - __/database/database\_helper\_factory.py__ - `Database_Helper_Factory` class provides a class method you can use to pull in either a postgresql or mysql database helper, so you can write code that functions the same way for either, allowing easier switching between the two.
    - __/database/database\_helper.py__ - `Database_Helper` abstract class encapsulates basic logic for dealing with creating connections and cursors using a Python DB API library.  Not fancy.  Opens, creates cursors and keeps track of all cursors it creates, and closes all related cursors and connection when you call close().  Nothing more.
    - __/database/psycopg2\_helper.py__ - `psycopg2_Helper` class encapsulates basic logic for dealing with creating connections and cursors using the psycopg2 library.  Not fancy.  Opens and closes, nothing more.
    - __/database/MySQLdb\_helper.py__ - `MySQLdb_Helper` class encapsulates basic logic for dealing with creating connections and cursors using the MySQLdb library.  Not fancy.  Opens and closes, nothing more.
    - __/database/PyMySQL\_helper.py__ - `PyMySQL_Helper` class encapsulates basic logic for dealing with creating connections and cursors using the PyMySQL library.  Not fancy.  Opens and closes, nothing more.

- __/dictionaries/__

    - __/dictionaries/dict\_helper.py__ - `DictHelper` class contains a function to retrieve a dict values as strings, integers, and lists that also accept a default, so you can convert to types and define default yourself when you look things up in a dict.

- __/django\_utils/__

    - __/django\_utils/django\_ajax\_selects\_lookup\_helper.py__ - includes `LookupParent` class, to allow for easy implementation of robust lookup classes for `django_ajax_selects`.
    - __/django\_utils/django\form\_helper.py__ - has a class `DjangoFormHelper` that includes helper class methods for working with forms: `is_form_empty()`; `is_value_empty()`; `data_to_html_as_hidden_inputs()`, and then classes `FormParent` and `ModelFormParent` that correctly apply these methods to forms and model forms, respectively.
    - __/django\_utils/django\_memory\_helper.py__ - has a class `DjangoMemoryHelper` with a single class method, `free_memory()`, that does everything I know how to do to free up memory in django while a long-running process is running.
    - __/django\_utils/django\_model\_helper.py__ - has a class `DjangoModelHelper` with a single class method, `copy_m2m_values()`, that copies ManyToMany values from one model to another for a field whose name is passed in.
    - __/django\_utils/django\_string\_helper.py__ - extends `StringHelper` class from `strings/string_helper.py`, updating the `convert_to_unicode()` method to use Django's built-in method.
    - __/django\_utils/django\_test\_case\_helper.py__ - has a class `DjangoTestCaseHelper` that extends `django.test.TestCase` and is itself meant to be extended by test case classes that wnat to use the help it provides.  For now, has a single method, `validate_string_against_file_contents()`,  for comparing a string with the contents of a file using difflib.
    - __/django\_utils/django\_view\_helper.py__ - has a class `DjangoViewHelper` with a single class method, `get_request_data()`, that retrieves data from a request passed in, whether the request is GET or POST.
    - __/django\_utils/query\_filter.py__ - `QueryFilterHelper` class, just extends `QuerySetHelper` for backward compatibility.
    - __/django\_utils/queryset\_helper.py__ - `QuerySetHelper` class that contains memory-efficient ways of iterating over large QuerySets, and also a few convenience methods for adding date and primary key filters to a QuerySet.
    - __/django\_utils/requirements.txt__ - list of packages required by the code in this folder.

- __/email/__

    - __/email/email\_helper.py__ - `EmailHelper` class that contains logic for setting up SMTP server using smtplib, then sending text or HTML email messages.
    - __/email/email\_test.py__ - basic email code on which EmailHelper is based, as an example.

- __/etl/__ - Basic ETL framework that includes:

    - objects to capture a simple ETL specification:

        - __/etl/etl\_attribute.py__ - Class `ETLAttribute` holds details on a particular property/field within a source file that is being loaded.
        - __/etl/etl\_entity.py__ - Class `ETLEntity` holds details on a set of attributes being loaded, practically speaking the set of columns/properties/fields in each record from a file that is being loaded.
        - __/etl/etl\_error.py__ - Class `ETLError` is an Error child class used to signal unrecoverable problems in ETL.

    - ETL processor family

        - __/etl/etl\_processor.py__ - Class `ETLProcessor` contains parts of ETL loader that are shared regardless of source or destination.
        - ---> __/etl/etl\_object\_loader.py__ - Class `ETLObjectLoader` contains parts of ETL loader that pertain to loading into instance of Python objects (and if you are loading into something more common, there are better tools). Extends `ETLProcessor`.
        - --------> __/etl/etl\_django\_model\_loader.py__ - Class `ETLDjangoModelLoader` contains parts of ETL loader that pertain to loading data into the specific type of object that is an instance of a django model (primarily looking to see if record matching ID column values already exists, so we update, rather than duplicate). Extends `ETLObjectLoader`.
        - ------------> __/etl/etl\_from\_excel\_with\_headers.py__ - Class `ETLFromExcelWithHeaders` contains the code to load data from an Excel document into any django model class instance based on an ETL specification contained in an `ETLEntity` specifiation instance. Extends `ETLDjangoModelLoader`.
        - ------------> __/etl/etl\_from\_dictionary\_iterable.py__ - Class `ETLFromDictionaryIterable` contains the code to load data from a list of data dictionary objects (from JSON, CSVDictReader, or other source) into any django model class instance based on an ETL specification contained in an `ETLEntity` specifiation instance. Extends `ETLDjangoModelLoader`.

    - __/etl/loadable\_django\_model.py__ - Class `LoadableDjangoModel` is a django abstract class that extends Django's `models.Model` class and contains all the methods each of the "`ETLFrom...`" classes in this package expect so they can load to a Django model class.  This class is intended to show the fields and methods that have to be present in a django model for the ETL loaders here to run without needing any modification.  It can either be imported into simple Django applications and then extended, or copied and altered to fit a more complex object model.

- __/exceptions/__

    - __/exceptions/exception\_helper.py__ - `ExceptionHelper` class that contains logic for printing exception messages, and also for emailing a summary if email is set up in the isntance.

- __/integers/__

    - __/integers/integer_helper.py__ - helper class `IntegerHelper` with a single class method, `is_valid_integer()`, that accepts a value and returns True if it contains a valid integer, False if not.
    - __/integers/tests.py__ - unit tests.

- __/json/__

    - __/json/json\_helper.py__ - `JSONHelper` class that contains logic for pretty printing JSON and escaping all string values within a JSON object.

- __/lists/__

    - __/lists/list\_helper.py__ - `ListHelper` class that contains class method `get_value_as_list()` that accepts a value, tries to convert it to a list.

- __/logging/__

    - __/logging/logging\_helper.py__ - `LoggingHelper` class contains instance variables to hold python `logging` logger instance and application name used when getting logger, and methods to get and set them.  The get_logger() method makes a new one using the application name if none is already present in the instance.  Can be used on its own, or as a parent class to add this stuff to an existing class.
    - __/logging/summary\_helper.py__ - `SummaryHelper` class that contains logic for capturing and outputting timing and auditing information.

- __/network__

    - __/network/http\_helper.py__ - `Http_Helper` class that contains logic for checking if a URL has been redirected, and if so, storing redirect information including status code and redirect URLs.
    - __/network/network\_helper.py__ - `Network_Helper` class contains instance methods for parsing URL strings and plucking out different known, standard pieces (domain, trimmed domain, just path - no query string, and everything after the domain).
    - __/network/openanything.py__ - Contains `SmartRedirectHandler` class that keeps track of redirect hops for urllib2, logic to support Http_Helper, from the Dive Into Python site (http://www.diveintopython.net/download/diveintopython-examples-5.4.zip)

- __/objects/__

    - __/objects/object\_helper.py__ - `ObjectHelper` class contains logic for detecting attributes in a given class (like the vars() method, only a little fancier).

- __/parameters/__

    - __/parameters/param\_container.py__ - `ParamContainer` class contains logic for defining, loading, accessing, and outputting parameters stored in a dictionary.

- __/R/__

    - __/R/rserve_helper.py__ - `RserveHelper` class contains logic for working with the Rserve Python-R integration package.

- __/rate\_limited/__

    - __/rate\_limited/basic\_rate\_limited.py__ - `BasicRateLimited` is a non-parallel parent class that contains variables and code for rate-limiting.  Details on extending TK below, in Usage Section.

- __/status/__

    - __/status/status\_container.py__ - `StatusContainer` class that can be used as a single return-type that contains detailed status information including status code, status message, nested name value pairs (which can include exceptions as values), and a nested status container from a child call.

- __/sequences/__

    - __/sequences/sequence\_helper.py__ - `SequenceHelper` class for methods to help with working with Sequences (Lists, etc.).  Only method there now is KnuthMorrisPratt(), used to find index in list of places where another list is reproduced in its entirety (looking for subsequences within sequences).

- __/strings/__

    - __/strings/html\_helper.py__ - `HTMLHelper` class to help with parsing and dealing with HTML strings.  Right now, has one static method, `remove_html()`, that removes HTML from a string, allowing for a list of HTML elements you want left in, and within those elements, a list of attributes you want left in.  If something is not in one of those lists, it will be removed.
    - __/strings/string\_helper.py__ - `StringHelper` class with methods to help with unicode encoding, stripping HTML from strings.
    - __/strings/tests.py__ - unit tests.

## Installation

### Option 1: pip for stable version

Use pip:

    (sudo) pip install python-utilities-jsm

### Option 2: latest from github

Clone this repository ( [https://github.com/jonathanmorgan/python_utilities.git](https://github.com/jonathanmorgan/python_utilities.git) ) and place it somewhere in your PYTHON\_PATH, including the base "python\_utilities" directory.  The easiest way to use these libraries with a Django site is to clone this repository into the site's project folder (where `manage.py` lives) alongside other applications, so these utilities are a part of the same python path as other django apps.  These utilities are used by other of my django applications, as well.  They can also be used outside of django.

Dependencies are listed below.  You can install them individually, or you can just use the `requirements*.txt` files, which lists them all out, to install them all at once using pip.  The command to install base packages, without database-specific support:

    (sudo) pip install -r python_utilities/requirements.txt


### For either option, database packages

For database packages, you'll need to load the requirements file for each database you want to interact with (right now `requirements_pgsql.txt` for postgresql and `requirements_mysql.txt` for MySQL).  Whichever you install, you'll also need to make sure you installed the client and client-dev libraries for each database you use.

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

### /database/PyMySQL\_helper.py

Before you can connect to MySQL with this code, you need to do the following:

- install the PyMySQL python package.  To install, use pip (`sudo pip install PyMySQL`) or conda if you are using anaconda (`conda install pymysql`).

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

    # import logging
    import logging

    # make instance
    my_exception_helper = ExceptionHelper()

    # by default, logs to logger with name "python_utilities.exceptions.exception_helper".
    # if you want it to log to a different logger name, initialize that logger,
    #    then pass it to the set_logger() method.  Example:
    #
    # my_logger = logging.getLogger( "logger_name_example" )
    # my_exception_helper.set_logger( my_logger )

    # By default, ExceptionHelper logs exception information to logging.ERROR.
    #    You can set the level at which your exception helper will log messages:
    # my_exception_helper.set_logging_level( logging.DEBUG )

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

Also, this class extends LoggingHelper, so it can take advantage of that set of functionality as well, outlined below.

### /logging/logging_helper.py

The `LoggingHelper` class can be used two ways:

1. you can create an instance of it and use that to retrieve a python logger.

        # import logging and LoggingHelper
        import logging
        from python_utilities.logging.logging_helper import LoggingHelper

        # make a Logger instance.
        my_logger_factory = LoggingHelper()

        # set the logger name
        my_logger_factory.set_logger_name( "test_logger" )

        # get a python logging.logger
        my_logger = my_logger_factory.get_logger()


2. You can use it as a parent class for an existing class to add a variable for a logger and a logging application name and methods to get and set each to a class.

        # import logging and Logger
        import logging
        from python_utilities.logging.logging_helper import LoggingHelper

        # make Logger the parent class
        class MyClass( LoggingHelper ):

            # in your __init__() method, call parent __init__(), then set
            #    self.logger_name to either __name__ or a name you prefer.
            def __init__( self ):

                # call parent's __init__()
                super( MyClass, self ).__init__()

                # set self.logger_name
                self.set_logger_name( "MyClass" )

            #-- END __init__() method --#

            # then, to get logger instance, call self.get_logger().

        #-- END class MyClass --#


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

### /network/http_helper.py

The `Http_Helper` class lets you configure an HTTP request in an instance of `Http_Helper` using its built in storage for request properties and headers, then submit the request using either the urllib2 ([https://docs.python.org/2/library/urllib2.html](https://docs.python.org/2/library/urllib2.html)), mechanize ([http://wwwsearch.sourceforge.net/mechanize/](http://wwwsearch.sourceforge.net/mechanize/)), or requests ([http://docs.python-requests.org/en/latest/](http://docs.python-requests.org/en/latest/)) packages.  For a given request and package, you can either get the page itself, or just submit a URL to find its final redirected URL.

Example: using requests package to submit a post request.

    # create Http_Helper
    my_http_helper = Http_Helper()

    # set http headers
    my_http_helper.set_http_header( "Content-Type", "text/plain" )

    # request type
    my_http_helper.request_type = Http_Helper.REQUEST_TYPE_POST

    # place body of request in a variable.
    request_data = "My dog has fleas, figaro, figaro, figaro!"

    # make the request using requests package:
    requests_response = my_http_helper.load_url_requests( "http://yahoo.com", request_type_IN = Http_Helper.REQUEST_TYPE_POST, data_IN = request_data )

    # get raw text response:
    requests_raw_text = requests_response.text

    # convert to a json object:
    requests_response_json = requests_response.json()

    # to make request using mechanize (a full-featured web browser):
    mechanize_response = my_http_helper.load_url_mechanize( "http://yahoo.com", request_type_IN = Http_Helper.REQUEST_TYPE_POST, data_IN = request_data )

    # to make request using urllib2:
    urllib2_response = my_http_helper.load_url_urllib2( "http://yahoo.com", request_type_IN = Http_Helper.REQUEST_TYPE_POST, data_IN = request_data )

Troubleshooting:

- If you are using the requests package and have data that you want to pass to the `load_url_requests()` method in variable `data_IN` that is a unicode string, if that unicode string has any non-ascii characters, you must encode the data before passing it in, else somewhere down in a library, something detects that the data is a unicode string and tries to encode it to "ASCII", which fails if there any non-ascii characters.  If you encode to UTF-8 before passing the data in, this converts to a byte string, and all works fine.

    - An example of the stack trace and exception message you'll see if you have this problem:

            File "<project_home>/python_utilities/network/http_helper.py", line 638, in load_url_requests
              response_OUT = requests.post( url_IN, headers = headers, data = data_IN )
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/api.py", line 99, in post
              return request('post', url, data=data, json=json, **kwargs)
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/api.py", line 49, in request
              response = session.request(method=method, url=url, **kwargs)
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/sessions.py", line 461, in request
              resp = self.send(prep, **send_kwargs)
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/sessions.py", line 573, in send
              r = adapter.send(request, **kwargs)
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/adapters.py", line 370, in send
              timeout=timeout
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.py", line 518, in urlopen
              body=body, headers=headers)
            File "<home_dir>/.virtualenvs/sourcenet/local/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.py", line 330, in _make_request
              conn.request(method, url, **httplib_request_kw)
            File "/usr/lib/python2.7/httplib.py", line 1001, in request
              self._send_request(method, url, body, headers)
            File "/usr/lib/python2.7/httplib.py", line 1035, in _send_request
              self.endheaders(body)
            File "/usr/lib/python2.7/httplib.py", line 997, in endheaders
              self._send_output(message_body)
            File "/usr/lib/python2.7/httplib.py", line 854, in _send_output
              self.send(message_body)
            File "/usr/lib/python2.7/httplib.py", line 826, in send
              self.sock.sendall(data)
            File "/usr/lib/python2.7/socket.py", line 224, in meth
              return getattr(self._sock,name)(*args)
            UnicodeEncodeError: 'ascii' codec can't encode character u'\u2014' in position 98: ordinal not in range(128)

    - An example of encoding using StringHelper:

            encoded_data = StringHelper.encode_string( unicode_string, StringHelper.ENCODING_UTF8 )

    - An example of encoding using codecs:

            encoded_data =

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
            super( SampleClass, self ).__init__()

            # declare variables

            # limit to no more than 4 per second
            self.rate_limit_in_seconds = 0.25

        #-- END method __init__() --#

- At the start of each transaction, call the `self.start_request()` method to let the code know you're starting a request.
- Once the request is done, call `continue_collecting = self.may_i_continue()` this method will block if you have to wait, will return true if it is OK to continue, will return False if some error occurred.
- In your control structure, always check the result of `may_i_continue()` before continuing.

## License:

Copyright 2015-present (2019) Jonathan Morgan

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
