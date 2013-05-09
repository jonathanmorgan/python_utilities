# python_utilities

Python Utility classes.  Includes the following:

- __/beautiful\_soup/beautiful\_soup\_helper.py__ - BeautifulSoupHelper class that implements helper methods for common things you do with BeautifulSoup, like getting child text and encoding HTML entities.  Built against BeautifulSoup 3, but should work with BeautifulSoup 4 if you change the imports.
- __/booleans/boolean\_helper.py__ - BooleanHelper class with method to convert non-boolean values to boolean type based on valid known true values (1, 't', 'true', 'y', 'yes').
- __/dictionaries/dict\_helper.py__ - for now, just contains a function to retrieve a dict value that also accepts a default, so you can define default yourself when you look things up in a dict.
- __/django\_utils/queryset\_helper.py__ - QuerySetHelper class that contains memory-efficient ways of iterating over large QuerySets, and also a few convenience methods for adding date and primary key filters to a QuerySet.
- __/email/email\_helper.py__ - EmailHelper class that contains logic for setting up SMTP server using smtplib, then sending text or HTML email messages.
- __/rate\_limited/basic\_rate\_limited.py__ - BasicRateLimited is a non-parallel parent class that contains variables and code for rate-limiting.  Details on extending TK below, in Usage Section.
- __/research/time\_series\_data.py__ - BasicRateLimited is a non-parallel parent class that contains variables and code for rate-limiting.  Details on extending TK below, in Usage Section.
- __/strings/string\_helper.py__ - StringHelper class with methods to help with unicode encoding, stripping HTML from strings.

## Installation

The easiest way to use these libraries is to clone this repository into a django sites folder alongside other applications, so they are a part of the same python path as other django apps.  These utilities are used by other of my django applications, as well.  They can also be used outside of django.

## Usage

### /rate_limited/basic\_rate\_limited.py

For a class you want to be rate-limited:

- have that class extend BasicRateLimited
- in that class, set instance variable rate\_limit\_in\_seconds to the minimum number of seconds you want between requests (can be a decimal).
- At the start of each transaction, call the `self.start_request()` method to let the code know you're starting a request.
- Once the request is done, call `continue_collecting = self.may_i_continue()` this method will block if you have to wait, will return true if it is OK to continue, will return False if some error occurred.
- In your control structure, always check the result of `may_i_continue()` before continuing.
