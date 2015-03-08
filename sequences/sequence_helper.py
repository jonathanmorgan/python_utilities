# start to support python 3:
from __future__ import unicode_literals

'''
Copyright 2015 Jonathan Morgan

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

# import SequenceHelper
from python_utilities.sequences.sequence_helper import SequenceHelper

# look for this:
look_for_list = [ 4, 5, 6 ]

# in this:
look_in_list = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 ]

# try the KnuthMorrisPratt algorithm from Python Cookbook 2nd Ed.
for match_index in SequenceHelper.KnuthMorrisPratt( look_in_list, look_for_list ):

    # append match to list.
    print( "Found match starting at index: " + str( match_index ) )
    
#-- END loop over matches. --#

# Output:
# Found match starting at index: 3
# Found match starting at index: 13

'''

# Imports

# define StringHelper class.
class SequenceHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    #============================================================================
    # static methods
    #============================================================================


    @staticmethod
    def KnuthMorrisPratt( look_in_sequence_IN, look_for_sequence_IN ):

        ''' Yields all starting positions of copies of subsequence
            'look_for_sequence_IN' in sequence 'look_in_sequence_IN' -- each
            argument can be any iterable.  At the time of each yield,
            'look_in_sequence_IN' has been read exactly up to and including the
            match with 'look_for_sequence_IN' that is causing the yield. '''
            
        # based on KnuthMorrisPratt in Martelli, A., Ravenscroft, A., & Ascher, D. (2005). Python Cookbook (Second Edition edition). Beijing; Sebastopol, CA: O'Reilly Media., recipe 5.13 
            
        # declare variables
        pattern_list = []
        pattern_list_length = -1
        shifts = None
        shift = -1
        pos = None
        pat = None
        current_item = None
            
        # ensure we can index into look_for_sequence_IN, and also make a copy to
        #    protect against changes to 'look_for_sequence_IN' while we're
        #    suspended by 'yield'
        pattern_list = list( look_for_sequence_IN )
        pattern_list_length = len( pattern_list )

        # build the KMP "table of shift amounts" and name it 'shifts'
        shifts = [1] * (pattern_list_length + 1)
        shift = 1
        for pos, pat in enumerate(pattern_list):
            while shift <= pos and pat != pattern_list[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift

        # perform the actual search
        startPos = 0
        matchLen = 0
        for current_item in look_in_sequence_IN:
            while matchLen == pattern_list_length or matchLen >= 0 and pattern_list[matchLen] != current_item:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == pattern_list_length: yield startPos            
            
    #-- END function KnuthMorrisPratt() --#


    @staticmethod
    def list_unique_values( list_IN ):
        
        '''
        Accepts a list.  Builds a list of unique values within the list. Returns
           the list of unique values.
        Based on: https://xenocoder.wordpress.com/2008/07/07/finding-unique-values-in-a-list-with-python/
        '''

        # return reference
        uniques_list_OUT = []
        
        # declare variables
        current_item = None
        
        # loop over items in list.
        for current_item in list_IN:

            # is item in uniques list?
            if current_item not in uniques_list_OUT:

                # no.  Add it.
                uniques_list_OUT.append( current_item )
                
            #-- END check to see if item in unique list. --#

        #-- END loop over items. --#
        
        return uniques_list_OUT

    #-- END static method list_unique_values() --#


#-- END class SequenceHelper --#