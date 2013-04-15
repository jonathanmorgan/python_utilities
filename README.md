# python_utilities

Python Utility classes.  Includes the following:
- /beautiful_soup/beautiful_soup_helper.py - BeautifulSoupHelper class that implements helper methods for common things you do with BeautifulSoup, like getting child text and encoding HTML entities.  Built against BeautifulSoup 3, but should work with BeautifulSoup 4 if you change the imports.
- /dictionaries/dict_helper.py - for now, just contains a function to retrieve a dict value that also accepts a default, so you can define default yourself when you look things up in a dict.
- /django_utils/queryset_helper.py - QuerySetHelper class that contains memory-efficient ways of iterating over large QuerySets, and also a few convenience methods for adding date and primary key filters to a QuerySet. 
- /email/email_helper.py - EmailHelper class that contains logic for setting up SMTP server using smtplib, then sending text or HTML email messages.
- /strings/string_helper.py - StringHelper class with methods to help with unicode encoding, stripping HTML from strings.

## Installation

The easiest way to use these libraries is to clone this repository into a django sites folder alongside other applications, so they are a part of the same python path as other django apps.  These utilities are used by other of my django applications, as well.  They can also be used outside of django.
