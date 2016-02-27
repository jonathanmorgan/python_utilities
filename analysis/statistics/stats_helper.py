# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016 Jonathan Morgan

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

# import StatsHelper
from python_utilities.analysis.statistics.statistics_helper import StatsHelper

# calculate Potter and Levine-Donnerstein's modified nominal pi.
number_of_coders = 3
number_of_choices = 2
value_list_1 = [ retty_json_string = JSONHelper.pretty_print_json( json_object )

'''

# Imports

# base python modules

# basic packages
import six # help with supporting both python 2 and 3.

# define StatsHelper class.
class StatsHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    

    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def potter_pi( cls, value_list_1_IN, value_list_2_IN, option_count_IN, coder_count_IN ):

        '''
        Accepts number of nominal variable value from which coders are choosing
            and number of coders among whom we will be calculating modified pi.
            Calculates the probability of chance agreement for use in modified 
            pi based (or p-subscript-e --> p_sub_e --> Pe) on these values,
            returns the resulting value.  If either value is missing, returns
            None.
           
        Used in calculating Scott's Pi formula, modified per Potter and
            Levine-Donnerstein, 1999, to base chance agreement on numbers of
            choices and coders, not the distribution of values, since
            Krippendorff's Alpha breaks down when there is little variance in a
            set of coding values.

            - Potter, W. J., & Levine‐Donnerstein, D. (1999). Rethinking validity and reliability in content analysis. Journal of Applied Communication Research, 27(3), 258–284. http://doi.org/10.1080/00909889909365539
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        to_the = -1
        divisor = -1
        
        # got count of options?
        if ( ( option_count_IN is not None ) and ( option_count_IN != "" ) and ( option_count_IN > 0 ) ):
            
            # got count of coders?
            if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( coder_count_IN > 0 ) ):
            
                # yes - calculate probability of chance agreement:
                #    Pe = 1 / ( option_count_IN ^ ( coder_count_IN - 1 ) )
                to_the = coder_count_IN - 1
                divisor = pow( option_count_IN, to_the )
                value_OUT = 1 / divisor

            else:

                # no count of coders.  Return None.
                value_OUT = None                

            #-- END check to see if count of coders passed in. --#
        
        else:
        
            # no option count.  Return None.
            value_OUT = None
        
        #-- END check to see if count of options passed in. --#
        
        return value_OUT

    #-- END method potter_pi() --#


    @classmethod
    def potter_pi_calc_p_sub_e( cls, option_count_IN, coder_count_IN ):

        '''
        Accepts number of nominal variable value from which coders are choosing
            and number of coders among whom we will be calculating modified pi.
            Calculates the probability of chance agreement for use in modified 
            pi based (or p-subscript-e --> p_sub_e --> Pe) on these values,
            returns the resulting value.  If either value is missing, returns
            None.
           
        Used in calculating Scott's Pi formula, modified per Potter and
            Levine-Donnerstein, 1999, to base chance agreement on numbers of
            choices and coders, not the distribution of values, since
            Krippendorff's Alpha breaks down when there is little variance in a
            set of coding values.

            - Potter, W. J., & Levine‐Donnerstein, D. (1999). Rethinking validity and reliability in content analysis. Journal of Applied Communication Research, 27(3), 258–284. http://doi.org/10.1080/00909889909365539
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        to_the = -1
        divisor = -1
        
        # got count of options?
        if ( ( option_count_IN is not None ) and ( option_count_IN != "" ) and ( option_count_IN > 0 ) ):
            
            # got count of coders?
            if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( coder_count_IN > 0 ) ):
            
                # yes - calculate probability of chance agreement:
                #    Pe = 1 / ( option_count_IN ^ ( coder_count_IN - 1 ) )
                to_the = coder_count_IN - 1
                divisor = pow( option_count_IN, to_the )
                value_OUT = 1 / divisor

            else:

                # no count of coders.  Return None.
                value_OUT = None                

            #-- END check to see if count of coders passed in. --#
        
        else:
        
            # no option count.  Return None.
            value_OUT = None
        
        #-- END check to see if count of options passed in. --#
        
        return value_OUT

    #-- END method potter_pi_calc_p_sub_e() --#


#-- END class StatsHelper --#
