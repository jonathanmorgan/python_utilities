'''
Created on Apr 26, 2011

@author: jonathanmorgan
'''

__author__="jonathanmorgan"
__date__ ="$Apr 26, 2011 12:31:35 AM$"

if __name__ == "__main__":
    print "You can not execute QueryFilterHelper on its own.  Use it as part of another python program."

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# Python base modules
#import logging
import queryset_helper

class QueryFilterHelper( queryset_helper.QuerySetHelper ):

    '''
    Just extends QuerySetHelper, nothing more.
    '''
    pass

#-- END class QueryFilterHelper --#