# start to python 3 support:
from __future__ import unicode_literals

# Imports
import htmlentitydefs
from HTMLParser import HTMLParser
import re

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


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------


    ENCODING_ASCII = 'ascii'
    ENCODING_UTF8 = 'utf-8'

    # regular expression for 4-byte unicode characters.
    RE_UNICODE_4_BYTE = re.compile( '[\U00010000-\U0010ffff]', re.UNICODE )
    
    # DEBUG
    DEBUG_FLAG = False


    #============================================================================
    # static methods
    #============================================================================


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
    def convert_to_unicode( cls, string_IN, encoding_IN = "", *args, **kwargs ):
        
        """
        Converts string to unicode.
        
        Based in part on:
        http://stackoverflow.com/questions/15800185/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9
        http://nedbatchelder.com/text/unipain.html
        """
    
        # return reference
        string_OUT = ""
        
        # decode from external encoding to unicode (probably is UTF-8).

        # dp we have an encoding passed in?
        if ( ( encoding_IN ) and ( encoding_IN != None ) and ( encoding_IN != "" ) ):
        
            # encoding passed in.  Use it.
            string_OUT = unicode( string_IN, encoding_IN )
        
        else:
            
            # no encoding - use default.
            string_OUT = unicode( string_IN )
            
        #-- END see if encoding is passed in. --#
        
        return string_OUT
    
    #-- END convert_to_unicode() function --#


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
        Accepts a string.  First, tries to convert to encoding passed in.  If
           exception, decodes it to unicode, then re-encodes it into the
           requested output_encoding, escaping illegal characters to XML
           entities by default.
           
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
            
                string_OUT = unicode_string.encode( output_encoding_IN )
                
            except:
    
                # yes, it does.  Encode to desired encoding, escaping invalid
                #    characters.
                string_OUT = unicode_string.encode( output_encoding_IN, encode_error_IN )
                
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
    def unicode_to_ascii( cls, string_IN = None, encoding_IN = "", encode_error_IN = "xmlcharrefreplace", *args, **kwargs ):
        
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
        string_OUT = cls.encode_string( string_IN, 'ascii', encode_error_IN = encode_error_IN )
                
        return string_OUT
    
    #-- END unicode_to_ascii() function --#


#-- END class StringHelper --#