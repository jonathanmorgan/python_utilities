# Imports
import htmlentitydefs
from HTMLParser import HTMLParser

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


#-- END class StringHelper --#