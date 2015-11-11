# start to support Python 3:
from __future__ import unicode_literals

'''
Copyright 2012 to 2014 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python_utilities is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/python_utilities.  If not, see
<http://www.gnu.org/licenses/>.
'''

'''
Usage:

# using string test_string

# import StringHelper
from python_utilities.strings.string_helper import StringHelper

# check to see if unicode
is_unicode = StringHelper.is_unicode( test_string )

# if not unicode, convert to unicode.
if ( is_unicode == False ):

    # use convert_to_unicode method to convert.
    test_string = StringHelper.convert_to_unicode( test_string )

#-- END check to see if unicode --#

# check if there are non-ASCII characters
has_non_ascii = StringHelper.has_non_ascii_characters( test_string )

# if there are non-ASCII characters, get a map of index of each in string to the
#    character itself.
if ( has_non_ascii == True ):

    # there are non-ASCII characters.  Find specifics.
    non_ascii_char_map = StringHelper.map_non_ascii_characters( test_string )
    
    # replace "\xa0" with "<BLARG!>", all else with " ".
    repl_map = { u"\xa0" : "<BLARG!>" }
    test_fixed = StringHelper.replace_non_ascii_characters( test_string, default_replacement_IN = " ", replacement_map_IN = repl_map )
    #-- END check to see if non-ASCII characters --#

'''

# Imports

# base python modules
import codecs
import htmlentitydefs
from HTMLParser import HTMLParser
import re
import six # help with supporting both python 2 and 3.

# Beautiful Soup
#from bs4 import UnicodeDammit

# define MLStripper class (from: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python )
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

    @classmethod
    def strip_tags( cls, html_IN ):
        s = cls()
        s.feed( html_IN )
        return s.get_data()
        
#-- END class MLStripper --#


# define HTMLTextExtractor class (from: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python )
class HTMLTextExtractor( HTMLParser ):

    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

    # class method to actually strip text.
    @classmethod
    def html_to_text( cls, html_IN = "" ):

        # return reference
        value_OUT = ""

        s = cls()
        s.feed( html_IN )
        value_OUT = s.get_text()

        return value_OUT

    #-- END class method html_to_text --#
        
#-- END class HTMLTextExtractor --#


# define StringHelper class.
class StringHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    ENCODING_ASCII = 'ascii'
    ENCODING_UTF8 = 'utf-8'

    # regular expression for 4-byte unicode characters.
    #RE_UNICODE_4_BYTE = re.compile( '[\U00010000-\U0010ffff]', re.UNICODE )

    # need to re-jigger to accomodate UCS-2 builds of python (not sure if it
    #    works, though).
    # from: http://stackoverflow.com/questions/12636489/python-convert-4-byte-char-to-avoid-mysql-error-incorrect-string-value
    try:

        # only works on UCS-4 builds of python
        RE_UNICODE_4_BYTE = re.compile( '[\U00010000-\U0010ffff]', re.UNICODE )

    except re.error:

        # didn't work, so UCS-2 build
        RE_UNICODE_4_BYTE = re.compile( '[\uD800-\uDBFF][\uDC00-\uDFFF]', re.UNICODE )

    #-- END exception handling for UCS-2 vs. UCS-4 builds of python --#
    
    # clearing out white space
    DEFAULT_CHAR_SUB_LIST = [ [ "\n", "" ], [ "\t", "" ] ]
    DEFAULT_RE_SUB_LIST =  [ [ "\s\s+", " " ] ]
    
    # DEBUG
    DEBUG_FLAG = False


    #============================================================================
    # static methods
    #============================================================================


    @staticmethod
    def find_substring_iter( look_in_string_IN, look_for_string_IN ):

        ''' Yields all starting positions of copies of substring
            'look_for_string_IN' in string 'look_in_string_IN'.'''
            
        # based on KnuthMorrisPratt in Martelli, A., Ravenscroft, A., & Ascher, D. (2005). Python Cookbook (Second Edition edition). Beijing; Sebastopol, CA: O'Reilly Media., recipe 5.13 

        # declare variables
        current_index = -1

        while True:

            current_index = look_in_string_IN.find( look_for_string_IN, current_index + 1 )

            if current_index < 0:
            
                # no more matches.  Fall out.
                break
            
            #-- END check to see if any more matches.

            # pass out most recent match.
            yield current_index
            
        #-- END infinite loop! --#

    #-- END static method find_substring_iter() --#


    @staticmethod
    def remove_html( string_IN, preserve_entities_IN = False ):
        
        """
        strips out HTML from string.
        """
    
        # return reference
        string_OUT = ""
        
        if ( preserve_entities_IN == True ):
        
            string_OUT = HTMLTextExtractor.html_to_text( string_IN )
        
        else:

            string_OUT = MLStripper.strip_tags( string_IN )
            
        #-- END check to see if we preserve entities or not. --#

        return string_OUT
    
    #-- END remove_html() function --#


    @staticmethod
    def unicode_escape( string_IN ):
        
        """
        Tidys up unicode entities into HTML friendly entities
    
        Takes a unicode string as an argument
    
        Returns a unicode string
        """
    
        # return reference
        string_OUT = ""
        
        # declare variables
        char = ""
        name = ""
        entity = ""
    
        for char in string_IN:

            if ord( char ) in htmlentitydefs.codepoint2name:

                name = htmlentitydefs.codepoint2name.get( ord( char ) )
                entity = htmlentitydefs.name2codepoint.get( name )
                string_OUT += "&#" + str(entity) + ";"
    
            else:

                string_OUT += char
                
            #-- END check to see if character has an entity --#
            
        #-- END loop over all characters in string_IN --#
    
        return string_OUT
    
    #-- END unicode_escape() function --#


    #============================================================================
    # class methods
    #============================================================================

    
    @classmethod
    def clean_string( cls,
                       string_IN,
                       char_list_IN = DEFAULT_CHAR_SUB_LIST,
                       re_list_IN = DEFAULT_RE_SUB_LIST,
                       *args,
                       **kwargs ):
        
        '''
        Accepts a string.  First, loops over list of character substitutions,
           using replace on each pair to replace the first item in the list with
           the second. Next, loops over the list of regular expression
           substitutions, replacing matches for the regular expression that is
           first in each pair with the text that is second.  If called with 
           
        Parameters:
        - string_IN - string we want to clean.
        - char_list_IN - list of lists that contain two strings, the first the string you want replaced, and the second the string you want to replace with.  If nothing specified, defaults to replacing tabs and newlines.
        - re_list_IN - list of lists that contain two strings, the first the regular expression you are looking to match, the second the string you want to replace matches with.  If nothing specified, defaults to replacing two or more contiguous spaces with one space.
        '''
        
        # return reference
        string_OUT = ""

        # declare variables
        char_list_length = -1
        char_list_pair = None
        replace_this = ""
        replace_with = ""
        re_list_length = -1
        re_list_pair = None
        
        # first, store string_IN in string_OUT.
        string_OUT = string_IN.strip()

        # make sure it is not None or empty string    
        if ( ( string_OUT ) and ( string_OUT != None ) and ( string_OUT != "" ) ):
        
            # first, see if anything in char list.
            char_list_length = len( char_list_IN )
            if ( char_list_length > 0 ):
            
                # there are things in list.
                for char_list_pair in char_list_IN:
                
                    # get replace this and replace with strings.
                    replace_this = char_list_pair[ 0 ]
                    replace_with = char_list_pair[ 1 ]
                    
                    # replace.
                    string_OUT = string_OUT.replace( replace_this, replace_with )
                
                #-- END loop over char list --#
            
            #-- END check to see if character replacement list populated --#

            # see if we have regular expressions.
            re_list_length = len( re_list_IN )
            if ( re_list_length > 0 ):
            
                # there are things in list.
                for re_list_pair in re_list_IN:
                
                    # get replace this and replace with strings.
                    replace_this = re_list_pair[ 0 ]
                    replace_with = re_list_pair[ 1 ]
                    
                    # replace.
                    string_OUT = re.sub( replace_this, replace_with, string_OUT )
                
                #-- END loop over char list --#
            
            #-- END check to see if character replacement list populated --#
            
        #-- END check to see if something passed in - don't want "None". --#
        
        return string_OUT
        
    #-- END method clean_string --#


    @classmethod
    def convert_to_unicode( cls, string_IN, encoding_IN = "", *args, **kwargs ):
        
        """
        Converts string to unicode.
        
        Based in part on:
        http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        http://nedbatchelder.com/text/unipain.html
        
        If this isn't working for you, try the UnicodeDammit object provided by
           Beautiful Soup 4:
           - http://www.crummy.com/software/BeautifulSoup/bs4/doc/#unicode-dammit
           
           from bs4 import UnicodeDammit

           # convert the string
           bs_test = UnicodeDammit( test_string )

           # get string
           bs_string = bs_test.unicode_markup

        postconditions: throws UnicodeDecodeError exception if string can't be decoded into unicode.
        """
        
        return cls.decode_to_unicode( string_IN, encoding_IN, *args, **kwargs ) 
    
    #-- END method convert_to_unicode() --#


    @classmethod
    def decode_to_unicode( cls, string_IN, encoding_IN = "", *args, **kwargs ):
        # def convert_to_unicode( cls, string_IN, encoding_IN = "", use_bs4_IN = True, *args, **kwargs ):
        
        """
        Converts string to unicode.
        
        Based in part on:
        http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        http://nedbatchelder.com/text/unipain.html
        
        If this isn't working for you, try the UnicodeDammit object provided by
           Beautiful Soup 4:
           - http://www.crummy.com/software/BeautifulSoup/bs4/doc/#unicode-dammit
           
           from bs4 import UnicodeDammit

           # convert the string
           bs_test = UnicodeDammit( test_string )

           # get string
           bs_string = bs_test.unicode_markup

        postconditions: throws UnicodeDecodeError exception if string can't be decoded into unicode.
        """
        
        # might want to use codecs.decode() instead of unicode object initializer...
    
        # return reference
        unicode_OUT = ""
        
        # declare variables
        is_already_unicode = False
        
        # first, check to see if already unicode.
        is_already_unicode = cls.is_unicode( string_IN )
        if ( is_already_unicode == False ):
        
            # nope - decode from external encoding to unicode (probably is UTF-8).
            
            # do we have an encoding passed in?
            if ( ( encoding_IN ) and ( encoding_IN != None ) and ( encoding_IN != "" ) ):
            
                # encoding passed in.  Use it.
                #unicode_OUT = unicode( string_IN, encoding_IN )
                unicode_OUT = codecs.decode( string_IN, encoding_IN )
            
            else:
                
                # no encoding - use default.
                #unicode_OUT = unicode( string_IN )
                unicode_OUT = codecs.decode( string_IN )
                
            #-- END see if encoding is passed in. --#
            
        else:
        
            # already unicode - just return it.
            unicode_OUT = string_IN
            
        #-- END check to see if already unicode. --#
        
        return unicode_OUT
    
    #-- END decode_to_unicode() function --#


    @classmethod
    def encode_string( cls,
                       string_IN,
                       output_encoding_IN = ENCODING_ASCII,
                       input_encoding_IN = '',
                       encode_error_IN = "xmlcharrefreplace",
                       entitize_4_byte_unicode_IN = False,
                       *args,
                       **kwargs ):
        
        '''
        Accepts a string.  First, decodes it to unicode since you have to have
           unicode string to encode (if already a unicode object, doesn't change
           anything).  Then, tries to convert to encoding passed in.  If
           exception, re-encodes it into the requested output_encoding, escaping
           illegal characters to XML entities by default.
           
        Parameters:
        - string_IN - string we want encoded in the output encoding specified.
        - output_encoding_IN - encoding we want this string to be in.  Defaults to ascii.
        - input_encoding_IN - optional encoding in which our string is encoded.
        - encod_error_IN - what we want to do on encoding errors, when converting to safe string (default is "xmlcharrefreplace", which converts those characters to entities).
        - entitize_4_byte_unicode_IN - Boolean, if True, after encoding, converts all 4-byte unicode characters to entities (for mysql that can't handle 4-byte unicode).  If false, doesn't.
        '''
        
        # return reference
        string_OUT = ""
        
        # declare variables
        unicode_string = ""
        
        # first, store string_IN in string_OUT.
        string_OUT = string_IN
        
        # make sure it is not None or empty string    
        if ( ( string_OUT ) and ( string_OUT != None ) and ( string_OUT != "" ) ):
        
            # first, make sure we have a unicode string.
            unicode_string = cls.convert_to_unicode( string_OUT, input_encoding_IN )
            
            # have we been asked to convert 4-byte characters to entities?
            if ( entitize_4_byte_unicode_IN == True ):
                
                # yes.  convert 4-byte unicode characters to entities.
                unicode_string = cls.entitize_4_byte_unicode( unicode_string )
                
            #-- END check to see if we entitize 4-byte unicode characters. --#
            
            # first, see if converting to desired encoding breaks things.
            try:
            
                #string_OUT = unicode_string.encode( output_encoding_IN )
                string_OUT = codecs.encode( unicode_string, output_encoding_IN )
                
            except:
    
                # yes, it does.  Encode to desired encoding, escaping invalid
                #    characters.
                #string_OUT = unicode_string.encode( output_encoding_IN, encode_error_IN )
                string_OUT = codecs.encode( unicode_string, output_encoding_IN, encode_error_IN )
                
            #-- END check to see if we need to safen string. --#
            
        #-- END check to see if something passed in - don't want "None". --#
        
        return string_OUT
        
    #-- END method encode_string --#


    @classmethod
    def entitize_4_byte_unicode( cls, string_IN, encoding_IN = "", *args, **kwargs ):
        
        """
        Accepts string, optional encoding that string is in.  Converts string to
           unicode if it isn't already in unicode, then uses regular expression
           to see if string contains 4-byte Unicode.  If so, converts all the
           4-byte Unicode characters to XML entities.  If not, returns string.
           
        Based in part on:
        - http://stackoverflow.com/questions/3220031/how-to-filter-or-replace-unicode-characters-that-would-take-more-than-3-bytes
        - http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        - http://nedbatchelder.com/text/unipain.html

        Eventually, will want to make a method to do the opposite - convert
           these entities back to unicode.

        References:
        - by hand - http://effbot.org/zone/re-sub.htm#unescape-html
        - HTMLParser and BeautifulSoup - http://stackoverflow.com/questions/663058/html-entity-codes-to-text
        
        """
    
        # return reference
        string_OUT = False
        
        # declare variables
        me = "entitize_4_byte_unicode"
        unicode_string = ""
        match_count = -1
        re_match = None
        match_character = ""
        character_entity = ""

        # variables to hold position of match.
        span = None
        span_start = -1
        span_end = -1
        
        # first, decode.
        unicode_string = cls.convert_to_unicode( string_IN, encoding_IN )
        
        # initialize variables.
        match_count = 0
        string_OUT = unicode_string

        # see if there is at least one match.
        re_match = cls.RE_UNICODE_4_BYTE.search( string_OUT )

        # loop as long as there is another match.
        while ( ( re_match ) and ( re_match != None ) ):

            # get details on match and span.
            match_count += 1
            
            # get matching character
            match_character = re_match.group( 0 )
            
            # convert to XML entity (have to do "ascii", else it will not
            #    detect the character as an error).
            character_entity = re_match.group( 0 ).encode( 'ascii', 'xmlcharrefreplace' )
            
            # get span, and from it, start and end position of character.
            span = re_match.span()
            span_start = span[ 0 ]
            span_end = span[ 1 ]
            
            # if debug, output stuff.
            if ( cls.DEBUG_FLAG == True ):

                print( "In " + me + "(): " + str( match_count ) + " - " + character_entity + " - span: ( " + str( span_start ) + ", " + str( span_end ) + " )" )

            #-- END DEBUG --#
        
            # replace string with character.
            string_OUT = string_OUT[ : span_start ] + character_entity + string_OUT[ span_end : ]
            
            # check for another match.
            re_match = cls.RE_UNICODE_4_BYTE.search( string_OUT )

        #-- END 

        # if debug, output stuff.
        if ( cls.DEBUG_FLAG == True ):

            print( "In " + me + "(): replaced? - " + string_OUT )
            
        #-- END DEBUG --#
            
        return string_OUT
    
    #-- END entitize_4_byte_unicode() function --#


    @classmethod
    def find_substring_match_list( cls, look_in_string_IN, look_for_string_IN ):

        '''
        uses find_substring_iter to retrieve all matches of substring in a
           string, returns a list.
        If finds one or more, returns list.  If finds none, returns empty list.
           If error for any reason, returns None.
        '''

        # return reference
        list_OUT = []

        # declare variables
        current_index = -1

        # loop using find_substring_iter
        for current_index in cls.find_substring_iter( look_in_string_IN, look_for_string_IN ):
        
            # add match to list.
            list_OUT.append( current_index )
            
        #-- END loop! --#

        return list_OUT

    #-- END class method find_substring_match_list() --#


    @classmethod
    def has_non_ascii_characters( cls, string_IN, *args, **kwargs ):
        
        """
        Accepts a unicode string.  Tries to encode it in ASCII.  If it fails, 
           returns True (has non-ascii characters).  If success, returns false.

        Preconditions: Must pass in unicode string.
        """
    
        # return reference
        value_OUT = False
        
        # declare variables
        encode_result = ""
        
        # try to encode the string in ASCII.
        try:
        
            # encode with strict error handling.
            encode_result = string_IN.encode( encoding = "ascii", errors = "strict" )
            
            # if we get here, then does not contain non-ascii characters.
            value_OUT = False
        
        except UnicodeEncodeError as uee:
        
            # exception converting to ASCII.  Contains non-ascii characters.
            value_OUT = True
        
        #-- END try/except encoding string as ASCII. --#
        
        return value_OUT
    
    #-- END has_non_ascii_characters() function --#


    @classmethod
    def is_unicode( cls, string_IN, *args, **kwargs ):
        
        """
        Accepts a string - returns True if it is unicode, False if not.
        
        Based in part on:
        http://stackoverflow.com/questions/4987327/how-do-i-check-if-a-string-is-unicode-or-ascii
        https://docs.djangoproject.com/en/dev/topics/python3/
        
        postconditions: throws UnicodeDecodeError exception if string can't be decoded into unicode.
        """
    
        # return reference
        value_OUT = ""
        
        # use six.text_type to see if string is unicode.
        value_OUT = isinstance( string_IN, six.text_type )
        
        return value_OUT
    
    #-- END is_unicode() function --#


    @classmethod
    def map_non_ascii_characters( cls, string_IN, *args, **kwargs ):
        
        """
        Accepts a unicode string.  Tries to encode it in ASCII.  If it succeeds,
           returns an empty dictionary.  If it fails, loops over characters in
           the string, checking each to see if it converts to ASCII.  Any that
           don't are added to the output dictionary, with key = index of
           character and value the character itself.

        Preconditions: Must pass in unicode string.
        
        Postconditions: returns a dictionary.  If no non-ASCII characters found,
           returns empty dictionary.
        """
    
        # return reference
        map_OUT = {}
        
        # declare variables
        has_non_ascii = False
        character_index = -1
        current_character = ""
        encode_result = ""
        
        # Check for non-ASCII characters.
        has_non_ascii = cls.has_non_ascii_characters( string_IN )
        
        # anything to map?
        if ( has_non_ascii == True ):
        
            # yes.  Loop over characters in string, checking each for ASCII-ness.
            character_index = -1
            for current_character in string_IN:
            
                # increment character index.
                character_index += 1
                
                # try to encode to ASCII
                try:
                
                    # encode to ASCII
                    encode_result = current_character.encode( encoding = "ascii", errors = "strict" )
                    
                    # if we get here, ASCII character.  Do nothing.
                
                except UnicodeEncodeError as uee:
                
                    # non-ascii character.  Add to map.
                    map_OUT[ character_index ] = current_character
                
                #-- END try/except around encode to ASCII --#
            
            #-- END loop over characters in string --#
        
        #-- END check to see if any non-ASCII characters to map. --#

        return map_OUT
    
    #-- END map_non_ascii_characters() function --#


    @classmethod
    def replace_non_ascii_characters( cls, string_IN, default_replacement_IN = None, replacement_map_IN = {}, *args, **kwargs ):
        
        """
        Accepts a unicode string, a blanket replacement string, and a map of
           unicode characters to their replacement.  Tries to encode string in
           ASCII.  If it succeeds, returns string passed in.  If it fails, gets
           map of non-ASCII characters in string, then for each:
           - checks if there is a replacement map.  If so, sees if character is
              a key in the dict.  If so, replaces that character with the
              specified replacement.
           - if no replacement map, or if no match, replaces the character with
              the replacement string.
           Returns the string with all non-ASCII characters replaced.

        Preconditions: Must pass in unicode string, and must pass in a
           replacement string.
        
        Postconditions: returns a dictionary.  If no non-ASCII characters found,
           returns string as passed in.  If error, returns None.
        """
    
        # return reference
        value_OUT = {}
        
        # declare variables
        non_ascii_char_dict = {}
        non_ascii_count = -1
        char_index = -1
        char_value = ""
        replacement_map = {}
        replace_with = ""
        
        # check if there is a default replacement value.
        if ( ( default_replacement_IN ) and ( default_replacement_IN != None ) ):
        
            # yes - start with string passed in.
            value_OUT = string_IN
                
            # There is.  Check for non-ASCII characters.
            non_ascii_char_dict = cls.map_non_ascii_characters( string_IN )
            non_ascii_count = len( non_ascii_char_dict )
            
            # anything to convert?
            if ( non_ascii_count > 0 ):
            
                # yes - make sure map is at least an empty map, not None.
                if ( ( replacement_map_IN ) and ( replacement_map_IN != None ) ):
                
                    # dict passed in.  Use it.
                    replacement_map = replacement_map_IN
                
                else:
                
                    # no dict passed in.  Use empty one.
                    replacement_map = {}
                
                #-- END initialize replacement map. --#
        
                # Loop over characters in dict.
                for char_index, char_value in non_ascii_char_dict.items():
                
                    # set replacement value

                    # Is this character in the replacement map?
                    if char_value in replacement_map:
                    
                        # yes - use mapped value.
                        replace_with = replacement_map[ char_value ]
                    
                    else:
                    
                        # no - use default replacement value.
                        replace_with = default_replacement_IN

                    #-- END check to see if specific replacement value for this character. --#
                    
                    # replace.
                    value_OUT = value_OUT.replace( char_value, replace_with )
                
                #-- END loop over characters in string --#
            
            #-- END check to see if any non-ASCII characters to map. --#
            
        else:
        
            # no replacement value - error - return None.
            value_OUT = None

        #-- END check to see if replacement value. --#

        return value_OUT
    
    #-- END replace_non_ascii_characters() function --#


    @classmethod
    def replace_white_space( cls, string_IN = None, replace_with_IN = " ", *args, **kwargs ):
        
        """
        Accepts string, splits it on white-space, joins the fragments together
           with whatever is passed in "replace_with_IN", which defaults to
           a space ( " " ).  Returns result of substitution.  Default is to take
           all blocks of 1 or more characters of white space and convert them to
           single spaces.
           
        Parameters:
        - string_IN - string we want to replace white space within.
        - replace_with_IN - what we want to replace white space with.  Defaults to single space (all white space blocks of one or more characters are collapsed to a single space).
        """
    
        # return reference
        string_OUT = ""
        
        # declare variables
        fragment_list = None

        # split string passed in on white space.
        fragment_list = string_IN.split()
        
        # join the fragments back together with the replace_with_IN character
        #    passed in.        
        string_OUT = replace_with_IN.join( fragment_list )
                
        return string_OUT
    
    #-- END replace_white_space() function --#


    @classmethod
    def unicode_to_ascii( cls, string_IN = None, encode_error_IN = "xmlcharrefreplace", *args, **kwargs ):
        
        """
        Converts string to unicode, then to ascii, converting any Unicode 
           characters to XML entities.  UTF-8 is not unicode - it is an
           encoding, just like ASCII.  To really deal with ENCODING problems,
           you need to first DEECODE to unicode.  Who knew?
        
        Based in part on:
        http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        http://nedbatchelder.com/text/unipain.html
        """
    
        # return reference
        string_OUT = ""

        # use safe string to convert to ascii.        
        string_OUT = cls.encode_string( string_IN, cls.ENCODING_ASCII, encode_error_IN = encode_error_IN )
                
        return string_OUT
    
    #-- END unicode_to_ascii() function --#


#-- END class StringHelper --#