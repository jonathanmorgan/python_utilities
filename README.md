# python\_utilities

Python Utility classes.  Includes the following:

- __/beautiful\_soup/beautiful\_soup\_helper.py__ - BeautifulSoupHelper class that implements helper methods for common things you do with BeautifulSoup, like getting child text and encoding HTML entities.  Built against BeautifulSoup 3, updated to import BeautifulSoup 4, work just fine far as I can tell...
- __/booleans/boolean\_helper.py__ - BooleanHelper class with method to convert non-boolean values to boolean type based on valid known true values (1, 't', 'true', 'y', 'yes').
- __/database/MySQLdb\_helper.py__ - MySQLdb\_Helper class encapsulates basic logic for dealing with creating connections and cursors using the MySQLdb library.  Not fancy.  Opens and closes, nothing more.
- __/dictionaries/dict\_helper.py__ - for now, just contains a function to retrieve a dict value that also accepts a default, so you can define default yourself when you look things up in a dict.
- __/django\_utils/queryset\_helper.py__ - QuerySetHelper class that contains memory-efficient ways of iterating over large QuerySets, and also a few convenience methods for adding date and primary key filters to a QuerySet.
- __/email/email\_helper.py__ - EmailHelper class that contains logic for setting up SMTP server using smtplib, then sending text or HTML email messages.
- __/exceptions/exception\_helper.py__ - ExceptionHelper class that contains logic for printing exception messages, and also for emailing a summary if email is set up in the isntance.
- __/network/http\_helper.py__ - Http_Helper class that contains logic for checking if a URL has been redirected, and if so, storing redirect information including status code and redirect URLs.
- __/network/mechanize\_tools.py__ - Contains logic to support Http_Helper, based on the Dive Into Python site (http://www.diveintopython.net/download/diveintopython-examples-5.4.zip), but using Mechanize's version of urllib2.
- __/network/openanything.py__ - Contains logic to support Http_Helper, from the Dive Into Python site (http://www.diveintopython.net/download/diveintopython-examples-5.4.zip)
- __/objects/object\_helper.py__ - ObjectHelper class contains logic for detecting attributes in a given class (like the vars() method, only a little fancier).
- __/rate\_limited/basic\_rate\_limited.py__ - BasicRateLimited is a non-parallel parent class that contains variables and code for rate-limiting.  Details on extending TK below, in Usage Section.
- __/strings/string\_helper.py__ - StringHelper class with methods to help with unicode encoding, stripping HTML from strings.

## Installation

Clone this repository and place it somewhere in your PYTHON\_PATH, including the base "python\_utilities" directory.  The easiest way to use these libraries with a Django site is to clone this repository into the site's folder alongside other applications, so these utilities are a part of the same python path as other django apps.  These utilities are used by other of my django applications, as well.  They can also be used outside of django.

### /beautiful\_soup/*

Requires the Beautiful Soup 4 package, installed via pip:

    (sudo) pip install BeautifulSoup4
    
If you are planning on using Beautiful Soup's "UnicodeDammit" class, you also should install chardet and/or cchardet:

    (sudo) pip install chardet
    (sudo) pip install cchardet

### /database/MySQLdb\_helper.py

Before you can connect to MySQL with this code, you need to do the following:

- install the MySQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libmysqlclient-dev) ( [source](http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/) ).

- install the MySQLdb python package.  To install, you can either install through your operating system's package manager (ubuntu, for example, has package "python-mysqldb") or using pip (`sudo pip install MySQL-python`).

### /network/*

Requires you install mechanize, a library that implements a browser client in python:

    (sudo) pip install mechanize
    
### /strings/*

Requires you to install the "six" package, which helps make python code that can run in either python 2 or 3:

    (sudo) pip install six

## Usage

### /rate\_limited/basic\_rate\_limited.py

For a class you want to be rate-limited:

- have that class extend BasicRateLimited
- in that class, set instance variable rate\_limit\_in\_seconds to the minimum number of seconds you want between requests (can be a decimal).
- At the start of each transaction, call the `self.start_request()` method to let the code know you're starting a request.
- Once the request is done, call `continue_collecting = self.may_i_continue()` this method will block if you have to wait, will return true if it is OK to continue, will return False if some error occurred.
- In your control structure, always check the result of `may_i_continue()` before continuing.

## ToDo:

- Implement a Postgresql\_Helper class, same interface as MySQL\_helper, so they are interchangable, then maybe a factory for getting instances.

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
