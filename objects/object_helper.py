# imports
import inspect

class ObjectHelper( object ):

    @classmethod
    def get_user_attributes( cls, class_IN, exlude_boring_IN = True ):

        '''
        Based on: http://stackoverflow.com/questions/4241171/inspect-python-class-attributes
        '''

        # declare variables
        boring = None
        attrs = None

        # get list of attributes of default object.
        boring = dir( type( 'dummy', ( object, ), {} ) )

        # initialize dictionary of attributes.
        attrs = {}

        # get base cases for current class.
        bases = reversed( inspect.getmro( class_IN ) )   

        # loop over base classes.
        for base in bases:
        
            # check for __dict__
            if hasattr( base, '__dict__' ):

                # update from __dict__
                attrs.update( base.__dict__ )

            # else, check for __slots__
            elif hasattr( base, '__slots__' ):
            
                if hasattr( base, base.__slots__[ 0 ] ): 

                    # We're dealing with a non-string sequence or one char string
                    for item in base.__slots__:

                        attrs[ item ] = getattr( base, item )
                        
                    #-- END loop over __slots__ --#

                else: 

                    # We're dealing with a single identifier as a string
                    attrs[ base.__slots__ ] = getattr( base, base.__slots__ )
                    
                #-- END check I don't necessarily understand as of yet. --#
                    
            #-- END check to see if __slots__ attribute. --#
        
        #-- END loop over base classes --#

        # remove anything that is in the "boring" list.
        if ( exlude_boring_IN == True ):
        
            for key in boring:
    
                del attrs[ key ]  # we can be sure it will be present so no need to guard this
                
            #-- END loop over boring --#
            
        #-- END check to see if we exclude boring --#

        return attrs

    #-- END method get_user_attributes() --#


#-- END class ObjectHelper --#