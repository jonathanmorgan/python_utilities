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
value_list_1 = [ 1, 0, 1, 0, 1, 0, 0, 0, 1 ]
value_list_2 = [ 1, 0, 1, 1, 0, 0, 1, 0, 1 ]
StatsHelper.potter_pi( value_list_1, value_list_2, number_of_coders, number_of_choices )
'''

#==============================================================================#
# Imports
#==============================================================================#

# base python modules

# basic packages
import numpy
import pandas
import six # help with supporting both python 2 and 3.

# python_utilities
from python_utilities.logging.logging_helper import LoggingHelper

# for Krippendorff's Alpha Python implementation.
try:
    import numpy as N
except ImportError:
    N = None    


#==============================================================================#
# classes
#==============================================================================#

# define StatsHelper class.
class StatsHelper( object ):


    #============================================================================
    # constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    
    # measurement levels
    MEASUREMENT_LEVEL_NOMINAL = "nominal"
    MEASUREMENT_LEVEL_ORDINAL = "ordinal"
    MEASUREMENT_LEVEL_INTERVAL = "interval"
    MEASUREMENT_LEVEL_RATIO = "ratio"
    

    #============================================================================
    # class methods
    #============================================================================


    '''
    Python implementation of Krippendorff's alpha -- inter-rater reliability
    
    (c)2011 Thomas Grill (http://grrrr.org)
    license: http://creativecommons.org/licenses/by-sa/3.0/
    
    Python version >= 2.4 required
    '''
    
    @classmethod
    def nominal_metric( cls, a, b ):

        return a != b

    #-- END class method nominal_metric() --#
        
    # ! TODO - ordinal when needed - is complicated:
    # - https://en.wikipedia.org/wiki/Krippendorff's_alpha
    # - http://web.asc.upenn.edu/usr/krippendorff/mwebreliability5.pdf

    @classmethod
    def interval_metric( cls, a, b ):

        return ( a - b ) ** 2
    
    #-- END class method interval_metric() --#
    
    @classmethod
    def ratio_metric( cls, a, b ):

        return ( ( a - b ) / ( a + b ) ) ** 2
        
    #-- END class method ratio_metric() --#
    
    @classmethod
    def krippendorff_alpha( cls,
                            data,
                            metric = interval_metric,
                            force_vecmath = False,
                            convert_items = float,
                            missing_items = None ):

        '''
        Calculate Krippendorff's alpha (inter-rater reliability):
        
        data is in the format
        [
            {unit1:value, unit2:value, ...},  # coder 1
            {unit1:value, unit3:value, ...},   # coder 2
            ...                            # more coders
        ]
        or 
        it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items
        
        metric: function calculating the pairwise distance
        force_vecmath: force vector math for custom metrics (numpy required)
        convert_items: function for the type conversion of items (default: float)
        missing_items: indicator for missing items (default: None)
        '''
        
        # number of coders
        m = len(data)
        
        # set of constants identifying missing values
        maskitems = set( ( missing_items, ) )
        #if N is not None:
        #    maskitems.add( N.ma.masked_singleton )
        
        # convert input data to a dict of items
        units = {}
        for d in data:
            try:
                # try if d behaves as a dict
                diter = six.iteritems( d )
            except AttributeError:
                # sequence assumed for d
                diter = enumerate( d )
                
            for it,g in diter:
                if g not in maskitems:
                    try:
                        its = units[it]
                    except KeyError:
                        its = []
                        units[it] = its
                    its.append(convert_items(g))
    
    
        units = dict((it,d) for it,d in units.iteritems() if len(d) > 1)  # units with pairable values
        n = sum(len(pv) for pv in units.itervalues())  # number of pairable values
        
        N_metric = (N is not None) and ( ( metric in ( cls.interval_metric, cls.nominal_metric, cls.ratio_metric ) ) or force_vecmath )
        
        Do = 0.
        for grades in units.itervalues():
            if N_metric:
                gr = N.array(grades)
                Du = sum(N.sum(metric(gr,gri)) for gri in gr)
            else:
                Du = sum(metric(gi,gj) for gi in grades for gj in grades)
            Do += Du/float(len(grades)-1)
        Do /= float(n)
    
        De = 0.
        for g1 in units.itervalues():
            if N_metric:
                d1 = N.array(g1)
                for g2 in units.itervalues():
                    De += sum(N.sum(metric(d1,gj)) for gj in g2)
            else:
                for g2 in units.itervalues():
                    De += sum(metric(gi,gj) for gi in g1 for gj in g2)
        De /= float(n*(n-1))
    
        return 1.-Do/De
    
    #-- END - class method krippendorff_alpha() --#


    @classmethod
    def percentage_agreement( cls, value_list_1_IN, value_list_2_IN ):

        '''
        Accepts two lists of values that must be the same length.  Calculates
            the percentage of pairs of numbers between the two groups where the
            values are the same.  Returns the percentage of agreement as a
            decimal between 0 and 1 (so you'll need to multiply by 100 to get
            percentage).
            
        If error, returns None.
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "StatsHelper.percentage_agreement"
        list_1_count = -1
        list_2_count = -1
        work_df = None
        column_name_list_1 = ""
        column_name_list_2 = ""
        column_name_is_equal = ""
        equal_sum = -1
        
        # got lists?
        if ( ( value_list_1_IN is not None ) and ( value_list_2_IN is not None ) ):
        
            # get counts of values in each list.
            list_1_count = len( value_list_1_IN )
            list_2_count = len( value_list_2_IN )
            
            # counts equal?
            if ( list_1_count == list_2_count ):
            
                # counts greater than 0?
                if ( list_1_count > 0 ):
                
                    # init column name holders
                    column_name_list_1 = "value_list_1"
                    column_name_list_2 = "value_list_2"
                    column_name_is_equal = "is_equal"
    
                    # combine into one data frame.
                    work_df = pandas.DataFrame()
                    work_df[ column_name_list_1 ] = value_list_1_IN
                    work_df[ column_name_list_2 ] = value_list_2_IN
                    
                    # make a new column that is 1 if values are the same, 0 if not.
                    work_df[ column_name_is_equal ] = numpy.where( work_df[ column_name_list_1 ] == work_df[ column_name_list_2 ], 1, 0 )
                    
                    # get sum of "is_equal" column.
                    equal_sum = work_df[ column_name_is_equal ].sum()
                    
                    # value out is equal_sum / list_1_count
                    # - relies on "from __future__ import division" above
                    value_OUT = equal_sum / list_1_count
                    
                else:
                
                    # nothing in lists.
                    LoggingHelper.output_debug( "ERROR - lists are not the same length ( " + str( list_1_count ) + " != " + str( list_2_count ) + " ), so can't calculate percentage agreement.", method_IN = me )
                    value_OUT = None
                    
                #-- END check to make sure something is in list. --#

            else:
            
                # lists of different length...
                LoggingHelper.output_debug( "ERROR - lists are not the same length ( " + str( list_1_count ) + " != " + str( list_2_count ) + " ), so can't calculate percentage agreement.", method_IN = me )
                value_OUT = None

            #-- END check to make sure list values are the same length. --#
        
        else:
        
            # one or both lists is empty.  Error.
            LoggingHelper.output_debug( "ERROR - one or both lists is None - Need 2 lists of values to calculate percentage agreement.", method_IN = me )
            value_OUT = None
            
        #-- END check to make sure lists passed in --#
        
        return value_OUT

    #-- END method percentage_agreement() --#


    @classmethod
    def potter_pi( cls, value_list_1_IN, value_list_2_IN, coder_count_IN, option_count_IN ):

        '''
        Accepts two lists of values that should be the same length, a count of
            the number of coders, and a count of the options from which the
            coders were choosing.  Uses coder count and option count to
            calculate probability of chance agreement, then uses that
            probability along with percentage agreement between the two lists
            to calculate Scott's Pi:
            - Pi = ( Po - Pe ) / ( 1 - Pe )
            - WHERE:
                - Po = observed agreement
                - Pe = modified probability of change agreement = 1 / ( coding_option_count ^ ( coder_count - 1 ) )
        Used in calculating Scott's Pi formula, modified per Potter and
            Levine-Donnerstein, 1999, to base chance agreement on numbers of
            choices and coders, not the distribution of values, since
            Krippendorff's Alpha breaks down when there is little variance in a
            set of coding values.

            - Potter, W. J., & Levine-Donnerstein, D. (1999). Rethinking validity and reliability in content analysis. Journal of Applied Communication Research, 27(3), 258-284. http://doi.org/10.1080/00909889909365539
        '''
        
        # return reference
        value_OUT = None
        
        # declare variables
        me = "StatsHelper.potter_pi"
        list_1_count = -1
        list_2_count = -1
        chance_agreement = -1
        percentage_agree = -1

        # got lists?
        if ( ( value_list_1_IN is not None ) and ( value_list_2_IN is not None ) ):
        
            # get counts of values in each list.
            list_1_count = len( value_list_1_IN )
            list_2_count = len( value_list_2_IN )
            
            # counts equal?
            if ( list_1_count == list_2_count ):
            
                # counts greater than 0?
                if ( list_1_count > 0 ):
                
                    # lists are good - got count of options?
                    if ( ( option_count_IN is not None ) and ( option_count_IN != "" ) and ( option_count_IN > 0 ) ):
                        
                        # got count of coders?
                        if ( ( coder_count_IN is not None ) and ( coder_count_IN != "" ) and ( coder_count_IN > 0 ) ):
                        
                            # yes - calculate probability of chance agreement...
                            chance_agreement = cls.potter_pi_calc_p_sub_e( coder_count_IN = coder_count_IN, option_count_IN = option_count_IN )

                            # ...then percentage agreement between the two numpy
                            #    arrays...
                            percentage_agree = cls.percentage_agreement( value_list_1_IN, value_list_2_IN )
                            
                            # ...and, finally, Scott's Pi.
                            value_OUT = ( percentage_agree - chance_agreement ) / ( 1.0 - chance_agreement )
            
                        else:
            
                            # no count of coders.  Return None.
                            value_OUT = None                
            
                        #-- END check to see if count of coders passed in. --#
                    
                    else:
                    
                        # no option count.  Return None.
                        value_OUT = None
                    
                    #-- END check to see if count of options passed in. --#
        
                else:
                
                    # nothing in lists.
                    LoggingHelper.output_debug( "ERROR - lists are not the same length ( " + str( list_1_count ) + " != " + str( list_2_count ) + " ), so can't calculate percentage agreement.", method_IN = me )
                    value_OUT = None
                    
                #-- END check to make sure something is in list. --#

            else:
            
                # lists of different length...
                LoggingHelper.output_debug( "ERROR - lists are not the same length ( " + str( list_1_count ) + " != " + str( list_2_count ) + " ), so can't calculate percentage agreement.", method_IN = me )
                value_OUT = None

            #-- END check to make sure list values are the same length. --#
        
        else:
        
            # one or both lists is empty.  Error.
            LoggingHelper.output_debug( "ERROR - one or both lists is None - Need 2 lists of values to calculate percentage agreement.", method_IN = me )
            value_OUT = None
            
        #-- END check to make sure lists passed in --#

        return value_OUT

    #-- END method potter_pi() --#


    @classmethod
    def potter_pi_calc_p_sub_e( cls, coder_count_IN, option_count_IN, ):

        '''
        Accepts number of coders among whom we will be calculating modified pi
            and number of nominal variable values from which coders chose.
            Calculates the probability of chance agreement for use in modified 
            pi based (or p-subscript-e --> p_sub_e --> Pe) on these values,
            returns the resulting value.  If either value is missing, returns
            None.
           
        Used in calculating Scott's Pi formula, modified per Potter and
            Levine-Donnerstein, 1999, to base chance agreement on numbers of
            choices and coders, not the distribution of values, since
            Krippendorff's Alpha breaks down when there is little variance in a
            set of coding values.

            - Potter, W. J., & Levine-Donnerstein, D. (1999). Rethinking validity and reliability in content analysis. Journal of Applied Communication Research, 27(3), 258-284. http://doi.org/10.1080/00909889909365539
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
