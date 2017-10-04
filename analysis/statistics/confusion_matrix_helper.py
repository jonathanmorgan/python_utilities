# start to support python 3:
from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2017 Jonathan Morgan

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

# import ConfusionMatrixHelper
from python_utilities.analysis.statistics.confusion_matrix_helper import ConfusionMatrixHelper

# build confusion matrix and derive statistics.


# retrieve some derived statistics.
number_of_coders = 3
number_of_choices = 2
value_list_1 = [ retty_json_string = JSONHelper.pretty_print_json( json_object )

'''

#==============================================================================#
# Imports
#==============================================================================#

# base python modules

# basic packages
import math
import numpy
import pandas
import six # help with supporting both python 2 and 3.
import sklearn
import sklearn.metrics

# python_utilities
from python_utilities.dictionaries.dict_helper import DictHelper
from python_utilities.logging.logging_helper import LoggingHelper

#==============================================================================#
# classes
#==============================================================================#

# define ConfusionMatrixHelper class.
class ConfusionMatrixHelper( object ):


    #============================================================================
    # ! ==> constants-ish
    #============================================================================


    # DEBUG
    DEBUG_FLAG = False
    
    # calculation types
    CALC_TYPE_MANUAL = "manual"
    CALC_TYPE_SKLEARN = "sklearn"
    CALC_TYPE_PANDAS = "pandas"
    
    # metric names, for map of metric names to metric values.    
    METRIC_ACCURACY = "accuracy"  # --> ACC
    METRIC_ACC = "ACC"  # --> accuracy
    METRIC_BM = "BM"  # --> informedness 
    METRIC_DIAGNOSTIC_ODDS_RATIO = "diagnostic_odds_ratio"  # --> DOR
    METRIC_DOR = "DOR"  # --> diagnostic_odds_ratio
    METRIC_F_ONE_SCORE = "f1_score"
    METRIC_FALSE_DISCOVERY_RATE = "false_discovery_rate"  # --> FDR
    METRIC_FALSE_NEGATIVE = "false_negative"
    METRIC_FALSE_NEGATIVE_RATE = "false_negative_rate"  # --> FNR
    METRIC_FALSE_OMISSION_RATE = "false_omission_rate"  # --> FOR
    METRIC_FALSE_POSITIVE = "false_positive"
    METRIC_FALSE_POSITIVE_RATE = "false_positive_rate"  # --> FPR
    METRIC_FDR = "FDR"  # --> false_discovery_rate
    METRIC_FNR = "FNR"  # --> false_negative_rate
    METRIC_FOR = "FOR"  # --> false_omission_rate
    METRIC_FPR = "FPR"  # --> false_positive_rate
    METRIC_INFORMEDNESS = "informedness"  # --> BM
    METRIC_LR_MINUS = "LR-"  # --> negative_likelihood_ratio
    METRIC_LR_PLUS = "LR+"  # --> positive_likelihood_ratio
    METRIC_MARKEDNESS = "markedness"  # --> MK
    METRIC_MATTHEWS_CORRELATION_COEFFICIENT = "matthews_correlation_coefficient"  # --> MCC
    METRIC_MCC = "MCC"  # --> matthews_correlation_coefficient
    METRIC_MK = "MK"  # --> markedness 
    METRIC_NEGATIVE_LIKELIHOOD_RATIO = "negative_likelihood_ratio"  # --> LR-
    METRIC_NEGATIVE_PREDICTIVE_VALUE = "negative_predictive_value"  # --> NPV
    METRIC_NPV = "NPV"  # --> negative_predictive_value
    METRIC_POPULATION_NEGATIVE = "population_negative"
    METRIC_POPULATION_POSITIVE = "population_positive"
    METRIC_POSITIVE_LIKELIHOOD_RATIO = "positive_likelihood_ratio"  # --> LR+
    METRIC_PPV = "PPV"  # --> precision
    METRIC_PRECISION = "precision"  # --> PPV
    METRIC_PREDICTED_NEGATIVE = "predicted_negative"
    METRIC_PREDICTED_POSITIVE = "predicted_positive"
    METRIC_RECALL = "recall"  # --> TPR
    METRIC_SPC = "SPC"  # --> true_negative_rate, TNR, specificity
    METRIC_SPECIFICITY = "specificity" # --> true_negative_rate, TNR, SPC
    METRIC_TOTAL_POPULATION = "total_population"
    METRIC_TNR = "TNR"  # --> true_negative_rate, specificity, SPC
    METRIC_TPR = "TPR"  # --> recall
    METRIC_TRUE_NEGATIVE = "true_negative"
    METRIC_TRUE_NEGATIVE_RATE = "true_negative_rate" # --> TNR, specificity, SPC
    METRIC_TRUE_POSITIVE = "true_positive"


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def populate_confusion_matrix( cls,
                                   ground_truth_values_IN,
                                   predicted_values_IN,
                                   calc_type_IN = CALC_TYPE_MANUAL,
                                   derive_metrics_IN = True ):
                                   
        '''
        Accepts ground truth and predicted values and an optional calculation
            type parameter and flag to tell if we want to derive all metrics.
            As long as there are ground truth and predicted values, and the two
            lists are the same length, calls a method to do initial confusion
            matrix population, then by default derive all stats we know how to
            derive based on it.  Returns instance of ConfusionMatrixHelper that
            contains all values.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables.
        me = "populate_confusion_matrix"
        error_string = ""
        ground_truth_length = -1
        predicted_length = -1
        
        # got two lists?  ground truth?
        if ( ground_truth_values_IN != None ):
        
            # predicted?
            if ( predicted_values_IN != None ):
            
                # got two lists.  Same length?
                ground_truth_length = len( ground_truth_values_IN )
                predicted_length = len( predicted_values_IN )
                if ( ground_truth_length == predicted_length ):
                
                    # good!  same length!
                    instance_OUT = ConfusionMatrixHelper()
                    instance_OUT.set_ground_truth_values( ground_truth_values_IN )
                    instance_OUT.set_predicted_values( predicted_values_IN )
                    
                    # check calc type - if get lots more, convert to dictionary
                    #     of types to function pointers.
                    if ( calc_type_IN == cls.CALC_TYPE_MANUAL ):
                    
                        # call the populate_manual() method.
                        instance_OUT = instance_OUT.populate_manual( ground_truth_values_IN, predicted_values_IN, derive_metrics_IN = derive_metrics_IN )
                        
                    elif ( calc_type_IN == cls.CALC_TYPE_SKLEARN ):
                    
                        # call the populate_sklearn() method.
                        instance_OUT = instance_OUT.populate_sklearn( ground_truth_values_IN, predicted_values_IN, derive_metrics_IN = derive_metrics_IN )
                        
                    elif ( calc_type_IN == cls.CALC_TYPE_PANDAS ):
                    
                        # call the populate_pandas() method.
                        instance_OUT = instance_OUT.populate_pandas( ground_truth_values_IN, predicted_values_IN, derive_metrics_IN = derive_metrics_IN )
                        
                    else:
                    
                        # no known CALC TYPE, so default - call the
                        #     populate_manual() method.
                        instance_OUT = instance_OUT.populate_manual( ground_truth_values_IN, predicted_values_IN, derive_metrics_IN = derive_metrics_IN )
                        
                    #-- END check for calc type --#
                    
                else:
                
                    error_string = "In " + me + "(): ERROR - lengths of ground_truth ( " + str( ground_truth_length ) + " ) and predicted ( " + str( predicted_length ) + " ) don't match.  Falling out."

                    if ( cls.DEBUG_FLAG == True ):
                        print( error_string )
                    #-- END DEBUG --#

                    instance_OUT = None

                #-- END check to see if lengths are the same. --#
            
            else:
            
                error_string = "In " + me + "(): ERROR - No predicted values ( " + str( predicted_values_IN ) + " ). Falling out."

                if ( cls.DEBUG_FLAG == True ):
                    print( error_string )
                #-- END DEBUG --#

                instance_OUT = None

            #-- END check to see if predicted values. --#
            
        else:
        
            error_string = "In " + me + "(): ERROR - No ground truth values ( " + str( ground_truth_values_IN ) + " ). Falling out."

            if ( cls.DEBUG_FLAG == True ):
                print( error_string )
            #-- END DEBUG --#

            instance_OUT = None

        #-- END check to see if ground truth. --#
        
        return instance_OUT
        
    #-- END class method populate_confusion_matrix() --#


    #============================================================================
    # ! ==> Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # initialize variables
        self.m_metrics_dict = {}
        
        # base dictionary
        self.m_metrics_dict_helper = DictHelper()
        self.m_metrics_dict_helper.set_dictionary( self.m_metrics_dict )
        
        # lists
        self.m_ground_truth_values = []
        self.m_predicted_values = []

    #-- END method __init__() --#


    def __str__( self, fancy_print_IN = True, *args, **kwargs ):

        # return reference
        string_OUT = ""
        
        # declare variables
        my_dict = None
        
        # note the class
        string_OUT = "ConfusionMatrixHelper --> \n"
        
        # get nested metrics helper.
        my_metrics = self.get_metrics_helper()
        string_OUT += str( my_metrics )
                
        return string_OUT
        
    #-- END method __str__() --#
    

    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def derive_metrics( self ):
        
        # return reference
        status_list_OUT = []
        
        # declare variables - base metrics
        confusion_metrics = None
        ground_truth_positive_count = None
        predicted_positive_count = None
        ground_truth_negative_count = None
        predicted_negative_count = None
        true_positive_count = None
        false_positive_count = None
        true_negative_count = None
        false_negative_count = None
        
        # declare variables - derived metrics
        precision = None  # PPV
        recall = None  # TPR
        false_negative_rate = None  # FNR
        false_positive_rate = None  # FPR
        true_negative_rate = None  # TNR, Specificity, SPC
        false_omission_rate = None  # FOR
        positive_likelihood_ratio = None  # LR+
        tpr = None
        fpr = None
        negative_likelihood_ratio = None
        fnr = None
        tnr = None
        accuracy = None
        total_population = None
        false_discovery_rate = None       
        negative_predictive_value = None 
        diagnostic_odds_ratio = None
        lr_plus = None
        lr_minus = None
        f1_score = None
        matthews_correlation_coefficient = None
        numerator = None
        temp_math = None
        denominator = None
        informedness = None
        markedness = None
        ppv = None
        npv = None
                
        # init confusion metrics and base values
        confusion_metrics = self.get_metrics_helper()
        ground_truth_positive_count = confusion_metrics.get_value_as_int( self.METRIC_POPULATION_POSITIVE, None )
        predicted_positive_count = confusion_metrics.get_value_as_int( self.METRIC_PREDICTED_POSITIVE, None )
        ground_truth_negative_count = confusion_metrics.get_value_as_int( self.METRIC_POPULATION_NEGATIVE, None )
        predicted_negative_count = confusion_metrics.get_value_as_int( self.METRIC_PREDICTED_NEGATIVE, None )
        true_positive_count = confusion_metrics.get_value_as_int( self.METRIC_TRUE_POSITIVE, None )
        false_positive_count = confusion_metrics.get_value_as_int( self.METRIC_FALSE_POSITIVE, None )
        true_negative_count = confusion_metrics.get_value_as_int( self.METRIC_TRUE_NEGATIVE, None )
        false_negative_count = confusion_metrics.get_value_as_int( self.METRIC_FALSE_NEGATIVE, None )

        # ! ==> precision - Positive predictive value (PPV), Precision
        precision = ( true_positive_count / predicted_positive_count )
        confusion_metrics.set_value( self.METRIC_PRECISION, precision )
        confusion_metrics.set_value( self.METRIC_PPV, precision )
        
        # ! ==> recall - True positive rate (TPR), Recall, Sensitivity, probability of detection
        recall = ( true_positive_count / ground_truth_positive_count )
        confusion_metrics.set_value( self.METRIC_RECALL, recall )
        confusion_metrics.set_value( self.METRIC_TPR, recall )
        
        # ! ==> False negative rate (FNR), Miss rate
        false_negative_rate = ( false_negative_count / ground_truth_positive_count )
        confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE_RATE, false_negative_rate )
        confusion_metrics.set_value( self.METRIC_FNR, false_negative_rate )

        # ! ==> False positive rate (FPR), Fall-out
        false_positive_rate = ( false_positive_count / ground_truth_negative_count )
        confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE_RATE, false_positive_rate )
        confusion_metrics.set_value( self.METRIC_FPR, false_positive_rate )

        # ! ==> True negative rate (TNR), Specificity (SPC)
        true_negative_rate = ( true_negative_count / ground_truth_negative_count )
        confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE_RATE, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_TNR, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_SPECIFICITY, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_SPC, true_negative_rate )
        
        # ! ==> False omission rate (FOR)
        false_omission_rate = ( false_negative_count / predicted_negative_count )
        confusion_metrics.set_value( self.METRIC_FALSE_OMISSION_RATE, false_omission_rate )
        confusion_metrics.set_value( self.METRIC_FOR, false_omission_rate )
        
        # ! ==> Positive likelihood ratio (LR+)
        tpr = recall
        fpr = false_positive_rate
        positive_likelihood_ratio = ( tpr / fpr )
        confusion_metrics.set_value( self.METRIC_POSITIVE_LIKELIHOOD_RATIO, positive_likelihood_ratio )
        confusion_metrics.set_value( self.METRIC_LR_PLUS, positive_likelihood_ratio )
        
        # ! ==> Negative likelihood ratio (LR-)
        fnr = false_negative_rate
        tnr = true_negative_rate
        if ( ( tnr is not None ) and ( tnr != 0 ) ):
            negative_likelihood_ratio = ( fnr / tnr )
        else:
            negative_likelihood_ratio = None
        #-- END check for division by zero --#
        confusion_metrics.set_value( self.METRIC_NEGATIVE_LIKELIHOOD_RATIO, negative_likelihood_ratio )
        confusion_metrics.set_value( self.METRIC_LR_MINUS, negative_likelihood_ratio )
        
        # ! ==> Accuracy (ACC)
        total_population = true_positive_count + true_negative_count + false_positive_count + false_negative_count
        accuracy = ( ( true_positive_count + true_negative_count ) / total_population )
        confusion_metrics.set_value( self.METRIC_ACCURACY, accuracy )
        confusion_metrics.set_value( self.METRIC_ACC, accuracy )
        confusion_metrics.set_value( self.METRIC_TOTAL_POPULATION, total_population )
        
        # ! ==> False discovery rate (FDR), probability of false alarm
        false_discovery_rate = ( false_positive_count / predicted_positive_count )
        confusion_metrics.set_value( self.METRIC_FALSE_DISCOVERY_RATE, false_discovery_rate )
        confusion_metrics.set_value( self.METRIC_FDR, false_discovery_rate )
        
        # ! ==> Negative predictive value (NPV)
        negative_predictive_value = ( true_negative_count / predicted_negative_count )
        confusion_metrics.set_value( self.METRIC_NEGATIVE_PREDICTIVE_VALUE, negative_predictive_value )
        confusion_metrics.set_value( self.METRIC_NPV, negative_predictive_value )

        # ! ==> Diagnostic odds ratio (DOR)
        lr_plus = positive_likelihood_ratio
        lr_minus = negative_likelihood_ratio
        if ( ( lr_minus is not None ) and ( lr_minus != 0 ) ):
            diagnostic_odds_ratio = ( lr_plus / lr_minus )
        else:
            diagnostic_odds_ratio = None
        #-- END check for division by zero --#
        confusion_metrics.set_value( self.METRIC_DIAGNOSTIC_ODDS_RATIO, diagnostic_odds_ratio )
        confusion_metrics.set_value( self.METRIC_DOR, diagnostic_odds_ratio )

        # ! ==> F1 score
        f1_score = ( 2 / ( ( 1 / recall ) + ( 1 / precision ) ) )
        confusion_metrics.set_value( self.METRIC_F_ONE_SCORE, f1_score )
        
        # ! ==> Matthews correlation coefficient (MCC)
        numerator = ( ( true_positive_count * true_negative_count ) - ( false_positive_count * false_negative_count ) )
        temp_math = ( ( true_positive_count + false_positive_count ) * ( true_positive_count + false_negative_count ) * ( true_negative_count + false_positive_count ) * ( true_negative_count + false_negative_count ) )
        denominator = math.sqrt( temp_math )
        matthews_correlation_coefficient = numerator / denominator
        confusion_metrics.set_value( self.METRIC_MATTHEWS_CORRELATION_COEFFICIENT, matthews_correlation_coefficient )
        confusion_metrics.set_value( self.METRIC_MCC, matthews_correlation_coefficient )
                
        # ! ==> Informedness or Bookmaker Informedness (BM)
        informedness = tpr + tnr - 1
        confusion_metrics.set_value( self.METRIC_INFORMEDNESS, informedness )
        confusion_metrics.set_value( self.METRIC_BM, informedness )

        # ! ==> Markedness (MK) = PPV + NPV − 1 
        ppv = precision
        npv = negative_predictive_value
        markedness = ppv + npv - 1
        confusion_metrics.set_value( self.METRIC_MARKEDNESS, markedness )
        confusion_metrics.set_value( self.METRIC_MK, markedness )
        
        return status_list_OUT
    
    #-- END method derive_metrics() --#


    def get_ground_truth_values( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        list_instance = None
        
        # get m_predicted_values
        value_OUT = self.m_ground_truth_values
        
        # got anything?
        if ( value_OUT is None ):
        
            # make dictionary instance.
            list_instance = []
            
            # store the instance.
            value_OUT = self.set_ground_truth_values( list_instance )
            
        #-- END check to see if dictionary initialized. --#
        
        return value_OUT
    
    #-- END method get_ground_truth_values --#


    def get_predicted_values( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        list_instance = None
        
        # get m_predicted_values
        value_OUT = self.m_predicted_values
        
        # got anything?
        if ( value_OUT is None ):
        
            # make dictionary instance.
            list_instance = []
            
            # store the instance.
            value_OUT = self.set_predicted_values( list_instance )
            
        #-- END check to see if dictionary initialized. --#
        
        return value_OUT
    
    #-- END method get_predicted_values --#


    def get_metrics_dict( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        dict_instance = None
        
        # get m_dictionary
        value_OUT = self.m_metrics_dict
        
        # got anything?
        if ( value_OUT is None ):
        
            # make dictionary instance.
            dict_instance = {}
            
            # store the instance.
            self.set_metrics_dict( dict_instance )
            
            # get the instance.
            value_OUT = self.get_metrics_dict()
        
        #-- END check to see if dictionary initialized. --#
        
        return value_OUT
    
    #-- END method get_metrics_dict --#


    def get_metrics_helper( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables
        metrics_helper_instance = None
        
        # get m_dictionary
        value_OUT = self.m_metrics_dict_helper
        
        # got anything?
        if ( value_OUT is None ):
        
            # make DictHelper instance.
            metric_helper_instance = DictHelper()
            
            # store the instance.
            self.set_metrics_helper( metrics_helper_instance )
            
            # get the instance.
            value_OUT = self.get_metrics_helper()
        
        #-- END check to see if dictionary initialized. --#
        
        return value_OUT
    
    #-- END method get_metrics_helper --#


    def populate_manual( self,
                         ground_truth_values_IN,
                         predicted_values_IN,
                         derive_metrics_IN = True ):
                                   
        '''
        Accepts ground truth and predicted values and flag to tell if we want to
            derive all metrics.  As long as there are ground truth and predicted
            values, and the two lists are the same length, calls a method to do
            initial confusion matrix population, then by default derive all
            stats we know how to derive based on it.  Returns instance of
            ConfusionMatrixHelper that contains all values.
        '''
        
        # return reference
        instance_OUT = self
        
        # declare variables
        me = "populate_manual"
        error_string = ""
        ground_truth_length = -1
        predicted_length = -1
        ground_truth_list = None
        predicted_list = None
        predicted_value = -1
        ground_truth_value = -1
        ground_truth_positive_count = 0
        predicted_positive_count = 0
        true_positive_count = 0
        false_positive_count = 0
        ground_truth_negative_count = 0
        predicted_negative_count = 0
        true_negative_count = 0
        false_negative_count = 0
        list_index = -1
        confusion_metrics = None
        
        # got two lists?  ground truth?
        if ( ground_truth_values_IN != None ):
        
            # predicted?
            if ( predicted_values_IN != None ):
            
                # got two lists.  Same length?
                ground_truth_length = len( ground_truth_values_IN )
                predicted_length = len( predicted_values_IN )
                if ( ground_truth_length == predicted_length ):
                
                    # load variables
                    ground_truth_list = ground_truth_values_IN
                    predicted_list = predicted_values_IN
            
                    # loop over lists to derive counts
                    for predicted_value in predicted_list:
                    
                        # increment index and get associated item from ground_truth_list
                        list_index += 1
                        ground_truth_value = ground_truth_list[ list_index ]
                        
                        # add to counts
                        
                        # ==> ground truth
                        if ( ground_truth_value == 0 ):
                            
                            # ground truth negative
                            ground_truth_negative_count += 1
                            
                        # not zero - so 1 (or supports other integer values)
                        else:
                    
                            # ground truth positive
                            ground_truth_positive_count += 1
                                    
                        #-- END check to see if positive or negative --# 
                        
                        
                        if ( predicted_value == 0 ):
                            
                            # predicted negative
                            predicted_negative_count += 1
                            
                            # equal to ground_truth?
                            if ( predicted_value == ground_truth_value ):
                                
                                # true negative
                                true_negative_count += 1
                                
                            else:
                                
                                # false negative
                                false_negative_count += 1
                                
                            #-- END check to see if true or false --#
                            
                        # not zero - so 1 (or supports other integer values)
                        else:
                    
                            # predicted positive
                            predicted_positive_count += 1
                            
                            # equal to ground_truth?
                            if ( predicted_value == ground_truth_value ):
                                
                                # true positive
                                true_positive_count += 1
                                
                            else:
                                
                                # false positive
                                false_positive_count += 1
                                
                            #-- END check to see if true or false --#
                            
                        #-- END check to see if positive or negative --# 
                    
                    #-- END loop over list items. --#
                        
                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Predicted positives: " + str( predicted_positive_count ) + " ( " + str( ( true_positive_count + false_positive_count ) ) + " )" )
                        print( "==> Ground truth positives: " + str( ground_truth_positive_count )  + " ( " + str( ( true_positive_count + false_negative_count ) ) + " )" )
                        print( "==> True positives: " + str( true_positive_count ) )
                        print( "==> False positives: " + str( false_positive_count ) )
                        print( "==> Predicted negatives: " + str( predicted_negative_count ) + " ( " + str( ( true_negative_count + false_negative_count ) ) + " )" )
                        print( "==> Ground truth negatives: " + str( ground_truth_negative_count ) + " ( " + str( ( true_negative_count + false_positive_count ) ) + " )" )
                        print( "==> True negatives: " + str( true_negative_count ) )
                        print( "==> False negatives: " + str( false_negative_count ) )
                        print( "==> Precision (true positive/predicted positive): " + str( ( true_positive_count / predicted_positive_count ) ) )
                        print( "==> Recall (true positive/ground truth positive): " + str( ( true_positive_count / ground_truth_positive_count ) ) )
                    #-- END DEBUG --#
                    
                    # add items to dictionary.
                    # add base measures to confusion_outputs
                    confusion_metrics = self.get_metrics_helper()
                    confusion_metrics.set_value( self.METRIC_POPULATION_POSITIVE, ground_truth_positive_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_POSITIVE, predicted_positive_count )
                    confusion_metrics.set_value( self.METRIC_POPULATION_NEGATIVE, ground_truth_negative_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_NEGATIVE, predicted_negative_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_POSITIVE, true_positive_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE, false_positive_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE, true_negative_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE, false_negative_count )

                    # derive the rest of the things we know about?
                    if ( derive_metrics_IN == True ):
                    
                        # yes - derive metrics.
                        self.derive_metrics()
                    
                    #-- END check to see if we derive additional metrics --#

                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Confusion outputs:" )
                        print( str( confusion_metrics ) )
                    #-- END DEBUG --#

                else:
                
                    error_string = "In " + me + "(): ERROR - lengths of ground_truth ( " + str( ground_truth_length ) + " ) and predicted ( " + str( predicted_length ) + " ) don't match.  Falling out."

                    if ( self.DEBUG_FLAG == True ):
                        print( error_string )
                    #-- END DEBUG --#

                    instance_OUT = None

                #-- END check to see if lengths are the same. --#
            
            else:
            
                error_string = "In " + me + "(): ERROR - No predicted values ( " + str( predicted_values_IN ) + " ). Falling out."

                if ( self.DEBUG_FLAG == True ):
                    print( error_string )
                #-- END DEBUG --#

                instance_OUT = None

            #-- END check to see if predicted values. --#
            
        else:
        
            error_string = "In " + me + "(): ERROR - No ground truth values ( " + str( ground_truth_values_IN ) + " ). Falling out."

            if ( self.DEBUG_FLAG == True ):
                print( error_string )
            #-- END DEBUG --#

            instance_OUT = None

        #-- END check to see if ground truth. --#

        return instance_OUT
        
    #-- END method populate_manual() --#


    def populate_pandas( self,
                         ground_truth_values_IN,
                         predicted_values_IN,
                         derive_metrics_IN = True ):
                              
        # return reference
        instance_OUT = self
    
        # declare variables
        me = "populate_pandas"
        error_string = ""
        ground_truth_length = -1
        predicted_length = -1
        ground_truth_list = None
        predicted_list = None
        y_actu = None
        y_pred = None
        df_confusion = None
        ground_truth_positive_count = 0
        predicted_positive_count = 0
        true_positive_count = 0
        false_positive_count = 0
        ground_truth_negative_count = 0
        predicted_negative_count = 0
        true_negative_count = 0
        false_negative_count = 0
        
        # got two lists?  ground truth?
        if ( ground_truth_values_IN != None ):
        
            # predicted?
            if ( predicted_values_IN != None ):
            
                # got two lists.  Same length?
                ground_truth_length = len( ground_truth_values_IN )
                predicted_length = len( predicted_values_IN )
                if ( ground_truth_length == predicted_length ):
                
                    # load variables
                    ground_truth_list = ground_truth_values_IN
                    predicted_list = predicted_values_IN

                    # pandas
                    # https://stackoverflow.com/questions/2148543/how-to-write-a-confusion-matrix-in-python
                    y_actu = pandas.Series( ground_truth_list, name='Actual')
                    y_pred = pandas.Series( predicted_list, name='Predicted')
                    df_confusion = pandas.crosstab(y_actu, y_pred)

                    if ( self.DEBUG_FLAG == True ):
                        print( str( conf_matrix ) )
                    #-- END DEBUG --#

                    # get counts in variables
                    true_positive_count = df_confusion[ 1 ][ 1 ]
                    false_positive_count = df_confusion[ 1 ][ 0 ]
                    true_negative_count = df_confusion[ 0 ][ 0 ]
                    false_negative_count = df_confusion[ 0 ][ 1 ]
                    
                    # and derive population and predicted counts
                    ground_truth_positive_count = true_positive_count + false_negative_count
                    predicted_positive_count = true_positive_count + false_positive_count
                    ground_truth_negative_count = true_negative_count + false_positive_count
                    predicted_negative_count = true_negative_count + false_negative_count

                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Predicted positives: " + str( predicted_positive_count ) + " ( " + str( ( true_positive_count + false_positive_count ) ) + " )" )
                        print( "==> Ground truth positives: " + str( ground_truth_positive_count )  + " ( " + str( ( true_positive_count + false_negative_count ) ) + " )" )
                        print( "==> True positives: " + str( true_positive_count ) )
                        print( "==> False positives: " + str( false_positive_count ) )
                        print( "==> Predicted negatives: " + str( predicted_negative_count ) + " ( " + str( ( true_negative_count + false_negative_count ) ) + " )" )
                        print( "==> Ground truth negatives: " + str( ground_truth_negative_count ) + " ( " + str( ( true_negative_count + false_positive_count ) ) + " )" )
                        print( "==> True negatives: " + str( true_negative_count ) )
                        print( "==> False negatives: " + str( false_negative_count ) )
                        print( "==> Precision (true positive/predicted positive): " + str( ( true_positive_count / predicted_positive_count ) ) )
                        print( "==> Recall (true positive/ground truth positive): " + str( ( true_positive_count / ground_truth_positive_count ) ) )
                    #-- END DEBUG --#
                    
                    # add items to dictionary.
                    # add base measures to confusion_outputs
                    confusion_metrics = self.get_metrics_helper()
                    confusion_metrics.set_value( self.METRIC_POPULATION_POSITIVE, ground_truth_positive_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_POSITIVE, predicted_positive_count )
                    confusion_metrics.set_value( self.METRIC_POPULATION_NEGATIVE, ground_truth_negative_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_NEGATIVE, predicted_negative_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_POSITIVE, true_positive_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE, false_positive_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE, true_negative_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE, false_negative_count )

                    # derive the rest of the things we know about?
                    if ( derive_metrics_IN == True ):
                    
                        # yes - derive metrics.
                        self.derive_metrics()
                    
                    #-- END check to see if we derive additional metrics --#

                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Confusion outputs:" )
                        print( str( confusion_metrics ) )
                    #-- END DEBUG --#

                else:
                
                    error_string = "In " + me + "(): ERROR - lengths of ground_truth ( " + str( ground_truth_length ) + " ) and predicted ( " + str( predicted_length ) + " ) don't match.  Falling out."

                    if ( self.DEBUG_FLAG == True ):
                        print( error_string )
                    #-- END DEBUG --#

                    instance_OUT = None

                #-- END check to see if lengths are the same. --#
            
            else:
            
                error_string = "In " + me + "(): ERROR - No predicted values ( " + str( predicted_values_IN ) + " ). Falling out."

                if ( self.DEBUG_FLAG == True ):
                    print( error_string )
                #-- END DEBUG --#

                instance_OUT = None

            #-- END check to see if predicted values. --#
            
        else:
        
            error_string = "In " + me + "(): ERROR - No ground truth values ( " + str( ground_truth_values_IN ) + " ). Falling out."

            if ( self.DEBUG_FLAG == True ):
                print( error_string )
            #-- END DEBUG --#

            instance_OUT = None

        #-- END check to see if ground truth. --#

        return instance_OUT
        
    #-- END method populate_pandas() --#


    def populate_sklearn( self,
                          ground_truth_values_IN,
                          predicted_values_IN,
                          derive_metrics_IN = True ):
                              
        # return reference
        instance_OUT = self
    
        # declare variables
        me = "populate_sklearn"
        error_string = ""
        ground_truth_length = -1
        predicted_length = -1
        ground_truth_list = None
        predicted_list = None
        conf_matrix = None
        ground_truth_positive_count = 0
        predicted_positive_count = 0
        true_positive_count = 0
        false_positive_count = 0
        ground_truth_negative_count = 0
        predicted_negative_count = 0
        true_negative_count = 0
        false_negative_count = 0
        
        # got two lists?  ground truth?
        if ( ground_truth_values_IN != None ):
        
            # predicted?
            if ( predicted_values_IN != None ):
            
                # got two lists.  Same length?
                ground_truth_length = len( ground_truth_values_IN )
                predicted_length = len( predicted_values_IN )
                if ( ground_truth_length == predicted_length ):
                
                    # load variables
                    ground_truth_list = ground_truth_values_IN
                    predicted_list = predicted_values_IN

                    # scikit-learn confusion matrix
                    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
                    conf_matrix = sklearn.metrics.confusion_matrix( ground_truth_list, predicted_list )
                    
                    if ( self.DEBUG_FLAG == True ):
                        print( str( conf_matrix ) )
                    #-- END DEBUG --#

                    # get counts in variables
                    true_positive_count = conf_matrix[ 1 ][ 1 ]
                    false_positive_count = conf_matrix[ 0 ][ 1 ]
                    true_negative_count = conf_matrix[ 0 ][ 0 ]
                    false_negative_count = conf_matrix[ 1 ][ 0 ]
                    
                    # and derive population and predicted counts
                    ground_truth_positive_count = true_positive_count + false_negative_count
                    predicted_positive_count = true_positive_count + false_positive_count
                    ground_truth_negative_count = true_negative_count + false_positive_count
                    predicted_negative_count = true_negative_count + false_negative_count

                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Predicted positives: " + str( predicted_positive_count ) + " ( " + str( ( true_positive_count + false_positive_count ) ) + " )" )
                        print( "==> Ground truth positives: " + str( ground_truth_positive_count )  + " ( " + str( ( true_positive_count + false_negative_count ) ) + " )" )
                        print( "==> True positives: " + str( true_positive_count ) )
                        print( "==> False positives: " + str( false_positive_count ) )
                        print( "==> Predicted negatives: " + str( predicted_negative_count ) + " ( " + str( ( true_negative_count + false_negative_count ) ) + " )" )
                        print( "==> Ground truth negatives: " + str( ground_truth_negative_count ) + " ( " + str( ( true_negative_count + false_positive_count ) ) + " )" )
                        print( "==> True negatives: " + str( true_negative_count ) )
                        print( "==> False negatives: " + str( false_negative_count ) )
                        print( "==> Precision (true positive/predicted positive): " + str( ( true_positive_count / predicted_positive_count ) ) )
                        print( "==> Recall (true positive/ground truth positive): " + str( ( true_positive_count / ground_truth_positive_count ) ) )
                    #-- END DEBUG --#
                    
                    # add items to dictionary.
                    # add base measures to confusion_outputs
                    confusion_metrics = self.get_metrics_helper()
                    confusion_metrics.set_value( self.METRIC_POPULATION_POSITIVE, ground_truth_positive_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_POSITIVE, predicted_positive_count )
                    confusion_metrics.set_value( self.METRIC_POPULATION_NEGATIVE, ground_truth_negative_count )
                    confusion_metrics.set_value( self.METRIC_PREDICTED_NEGATIVE, predicted_negative_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_POSITIVE, true_positive_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE, false_positive_count )
                    confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE, true_negative_count )
                    confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE, false_negative_count )

                    # derive the rest of the things we know about?
                    if ( derive_metrics_IN == True ):
                    
                        # yes - derive metrics.
                        self.derive_metrics()
                    
                    #-- END check to see if we derive additional metrics --#

                    if ( self.DEBUG_FLAG == True ):
                        print( "==> Confusion outputs:" )
                        print( str( confusion_metrics ) )
                    #-- END DEBUG --#

                else:
                
                    error_string = "In " + me + "(): ERROR - lengths of ground_truth ( " + str( ground_truth_length ) + " ) and predicted ( " + str( predicted_length ) + " ) don't match.  Falling out."

                    if ( self.DEBUG_FLAG == True ):
                        print( error_string )
                    #-- END DEBUG --#

                    instance_OUT = None

                #-- END check to see if lengths are the same. --#
            
            else:
            
                error_string = "In " + me + "(): ERROR - No predicted values ( " + str( predicted_values_IN ) + " ). Falling out."

                if ( self.DEBUG_FLAG == True ):
                    print( error_string )
                #-- END DEBUG --#

                instance_OUT = None

            #-- END check to see if predicted values. --#
            
        else:
        
            error_string = "In " + me + "(): ERROR - No ground truth values ( " + str( ground_truth_values_IN ) + " ). Falling out."

            if ( self.DEBUG_FLAG == True ):
                print( error_string )
            #-- END DEBUG --#

            instance_OUT = None

        #-- END check to see if ground truth. --#

        return instance_OUT
        
    #-- END method populate_sklearn() --#


    def set_ground_truth_values( self, instance_IN ):
        
        '''
        Accepts list.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_ground_truth_values = instance_IN
        
        # return it.
        value_OUT = self.get_ground_truth_values()
        
        return value_OUT
        
    #-- END method set_ground_truth_values() --#


    def set_predicted_values( self, instance_IN ):
        
        '''
        Accepts list.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_predicted_values = instance_IN
        
        # return it.
        value_OUT = self.get_predicted_values()
        
        return value_OUT
        
    #-- END method set_ground_truth_values() --#


    def set_metrics_dict( self, instance_IN ):
        
        '''
        Accepts dictionary.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_metrics_dict = instance_IN
        
        # return it.
        value_OUT = self.m_metrics_dict
        
        return value_OUT
        
    #-- END method set_metrics_dict() --#


    def set_metrics_helper( self, instance_IN ):
        
        '''
        Accepts dictionary.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_metrics_dict_helper = instance_IN
        
        # return it.
        value_OUT = self.m_metrics_dict_helper
        
        return value_OUT
        
    #-- END method set_metrics_helper() --#


#-- END class ConfusionMatrixHelper --#
