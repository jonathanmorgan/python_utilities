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
import matplotlib
import matplotlib.pyplot
import numpy
import pandas
import pandas_ml
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
    CALC_TYPE_PANDAS_ML = "pandas_ml"
    
    # calculation type to function map
    #CALC_TYPE_TO_METHOD_MAP = {}
    #CALC_TYPE_TO_METHOD_MAP[ CALC_TYPE_MANUAL ] = ConfusionMatrixHelper.populate_manual
    #CALC_TYPE_TO_METHOD_MAP[ CALC_TYPE_SKLEARN ] = ConfusionMatrixHelper.populate_sklearn
    #CALC_TYPE_TO_METHOD_MAP[ CALC_TYPE_PANDAS ] = ConfusionMatrixHelper.populate_pandas
    #CALC_TYPE_TO_METHOD_MAP[ CALC_TYPE_PANDAS_ML ] = ConfusionMatrixHelper.populate_pandas_ml
    
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
    
    # ==> class method precision_recall_f1():
    
    # calculation methods
    CALCULATION_METHOD_DEFAULT = "default"
    CALCULATION_METHOD_BINARY = "binary"
    CACLULATION_METHOD_MACRO = "macro"
    CALCULATION_METHOD_MICRO = "micro"
    CALCULATION_METHOD_WEIGHTED = "weighted"
    
    # return items
    RETURN_CONFUSION_MATRIX = "confusion_matrix"
    RETURN_METHOD_TO_RESULT_MAP = "method_to_result_map"
    RETURN_LINE_LIST = "line_list"


    #============================================================================
    # ! ==> class methods
    #============================================================================


    @classmethod
    def accuracy_at_k( cls, y_true, y_scores, k ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        threshold = None
        
        # get threshold index
        threshold = cls.threshold_at_k( y_scores, k )
        
        # use threshold to generate predicted scores
        y_pred = numpy.asarray( [ 1 if i >= threshold else 0 for i in y_scores ] )
        
        # calculate accuracy
        value_OUT = sklearn.metrics.accuracy_score( y_true, y_pred )
        
        return value_OUT
    
    #-- END class method accuracy_at_k() --#


    @classmethod
    def plot_precision_recall_n( cls,
                                 y_true,
                                 y_prob, model_name, output_path_IN = None ):

        """
        Accepts a list of baseline labels (0 or 1), a list of predicted scores
            (assumed to be decimal, between 0 and 1), and then a model name and
            optional path to which graphs should be output as PDF:
        
        - y_true: list of ground truth labels
        - y_prob: list of predicted scores (assume 0 to 1, decimal) from model.
        - model_name: string of model name (e.g, LR_123)
        - output_path_IN: optional file system path where you want output stored.
        
        For each distinct value in y_prob, uses that value as a cut-off for
            binary classification (all below are 0, all equal-to or above are
            1).  Then, using that cutoff, calculates percent of items above,
            precision, and recall for data that results from using that value as
            a cutoff.  Outputs a graph where x-axis is the range of distinct
            values used as cutoffs, and then on the Y-axis, at each point, is
            graphed the % above 0, the precision, and the recall for using that
            value as the 0-to-1 threshold.  If output path is specified, will
            output the resulting graph to a PDF file a that path.
        """
        
        # imports
        from sklearn.metrics import precision_recall_curve
        
        # return reference
        details_OUT = {}
        
        # declare variables
        me = "plot_precision_recall_n"
        y_score = None
        precision_curve = None
        recall_curve = None
        pr_thresholds = None
        num_above_thresh = None
        pct_above_thresh = None
        pct_above_per_thresh = None
        current_score = None
        above_threshold_list = None
        above_threshold_count = -1
        fig = None
        ax1 = None
        ax2 = None
        
        # store the raw scores in y_score
        y_score = y_prob
        
        # calculate precision-recall curve
        # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html
        # Returns:
        # - precision_curve - Precison values such that element i is the precision of predictions where cutoff is score >= thresholds[ i ] and the last element is 1.
        # - recall_curve - Recall values such that element i is the recall of predictions where cutoff is score >= thresholds[ i ] and the last element is 0.
        # - pr_thresholds - Increasing thresholds on the decision function used to decide 1 or 0, used to calculate precision and recall (looks like it is the set of unique values in the predicted value set).
        precision_curve, recall_curve, pr_thresholds = precision_recall_curve( y_true, y_score )
        
        # get all but the last precision score (1).
        precision_curve = precision_curve[ : -1 ]
        # print( "precision_curve: {}".format( precision_curve ) )
        
        # get all but the last recall score (0).
        recall_curve = recall_curve[ : -1 ]
        # print( "recall_curve: {}".format( recall_curve ) )
        
        # store details
        details_OUT[ "precision" ] = precision_curve
        details_OUT[ "recall" ] = recall_curve
        details_OUT[ "threshold" ] = pr_thresholds
        
        # init loop over thresholds
        pct_above_per_thresh = []
        number_scored = len(y_score)
        
        # loop over thresholds
        for value in pr_thresholds:
            
            # at each threshold, calculate the percent of rows above the threshold.
            above_threshold_list = []
            above_threshold_count = -1
            for current_score in y_score:
                
                # is it at or above threshold?
                if ( current_score >= value ):
                    
                    # it is either at or above threshold - add to list.
                    above_threshold_list.append( current_score )
                    
                #-- END check to see if at or above threshold? --#
                    
            #-- END loop over scores. --#
    
            # how many above threshold?
            #num_above_thresh = len(y_score[y_score>=value])
            above_threshold_count = len( above_threshold_list )
            num_above_thresh = above_threshold_count
            
            # percent above threshold
            pct_above_thresh = num_above_thresh / float( number_scored )
            
            # add to list.
            pct_above_per_thresh.append( pct_above_thresh )
            
        #-- END loop over thresholds --#
    
        details_OUT[ "percent_above" ] = pct_above_per_thresh
        
        # convert to numpy array
        pct_above_per_thresh = numpy.array(pct_above_per_thresh)
    
        # init matplotlib
        matplotlib.pyplot.clf()
        fig, ax1 = matplotlib.pyplot.subplots()
        
        # plot % above threshold line
        ax1.plot( pr_thresholds, pct_above_per_thresh, 'y')
        ax1.set_xlabel('threshold values')
        matplotlib.pyplot.xticks( [ 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1 ] )
        ax1.set_ylabel('% above threshold', color='y')
        ax1.set_ylim(0,1.05)
        
        # plot precision line
        ax2 = ax1.twinx()
        ax2.plot( pr_thresholds, precision_curve, 'b')
        ax2.set_ylabel('precision', color='b')
        ax2.set_ylim(0,1.05)
    
        # plot recall line
        ax3 = ax2.twinx()
        ax3.plot( pr_thresholds, recall_curve, 'r')
        ax3.set_ylabel('recall', color='r')
        ax3.set_ylim(0,1.05)
        
        # finish off graph
        name = model_name
        matplotlib.pyplot.title(name)
        
        # is there an output path?
        if ( ( output_path_IN is not None ) and ( output_path_IN != "" ) ):
        
            # save the figure to file.
            matplotlib.pyplot.savefig( output_path_IN )
            print( "In {}: figure output to {}".format( me, output_path_IN ) )
        
        #-- END check to see if we output to disk. --#
        
        matplotlib.pyplot.show()
    
        # clear plot.
        matplotlib.pyplot.clf()
        
        return details_OUT
        
    #-- END function plot_precision_recall_n() --#


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
                        
                    elif ( calc_type_IN == cls.CALC_TYPE_PANDAS_ML ):
                    
                        # call the populate_pandas_ml() method.
                        instance_OUT = instance_OUT.populate_pandas_ml( ground_truth_values_IN, predicted_values_IN, derive_metrics_IN = derive_metrics_IN )
                        
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


    @classmethod
    def precision_at_k( cls, y_true, y_scores, k ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        threshold = None
        
        # get threshold index
        threshold = cls.threshold_at_k( y_scores, k )
        
        # use threshold to generate predicted scores
        y_pred = numpy.asarray( [ 1 if i >= threshold else 0 for i in y_scores ] )
        
        # calculate precision
        value_OUT = sklearn.metrics.precision_score( y_true, y_pred )
        
        return value_OUT
    
    #-- END class method precision_at_k() --#


    @classmethod
    def precision_recall_f1( cls,
                             baseline_list_IN,
                             predicted_list_IN,
                             calculation_methods_list_IN,
                             do_print_IN = True,
                             output_to_file_IN = True ):
    
        '''
        Accepts baseline list and predicted list of values, a list of
            calculation methods to include, and then some configuration values
            around how to output information created during processing.
            
        For each of the selected calculation methods, calculates precision,
            recall, and F1 for the values passed in, then returns a dictionary
            that contains the results.  In the dictionary:
            
            - key "confusion_matrix" maps to the derived raw confusion matrix, created using sklearn.metrics.confusion_matrix().
            - key "method_to_result_map" maps each of the methods passed in to the results for that method, direct from scikit-learn.
            - key "line_list" contains a list of output lines IF output_to_file_IN, is True, for output to a file.
        '''
    
        # return reference
        output_dict_OUT = {}
        
        # declare variables
        output_string = None
        my_line_list = None
        calculation_methods = None
        cm = None
        method_to_result_map = None
        calculation_method = None
        precision = None
        recall = None
        accuracy = None
        F1 = None
        support = None
        
        # declare variables - default algorithm
        default_evaluation = None
        default_precision_list = None
        default_recall_list = None
        default_F1_list = None
        default_support_list = None
        precision_list_length = None
        recall_list_length = None
        F1_list_length = None
    
        # init
        my_line_list = []
        
        # init - calculation methods to include and lists
        calculation_methods = calculation_methods_list_IN
        baseline_list = baseline_list_IN
        derived_binary_list = predicted_list_IN
    
        # confusion matrix
        cm = sklearn.metrics.confusion_matrix( baseline_list, derived_binary_list )
        
        # RETURN - store confusion matrix
        output_dict_OUT[ cls.RETURN_CONFUSION_MATRIX ] = cm
    
        # output
        output_string = "\nConfusion matrix:\n{}\n\nBinary Key:\n[[ TN, FP ]\n [ FN, TP ]]".format( cm )
        if ( do_print_IN == True ):
            print( output_string )
        #-- END if do_print_IN --#
    
        # if output to file...
        if ( output_to_file_IN == True ):
    
            # store line for output
            my_line_list.append( output_string )
    
        #-- END if output... --#
    
        # loop over calculation methods
        method_to_result_map = {}
        for calculation_method in calculation_methods:
            
            # RETURN - create map for method
            
    
            # output
            output_string = "\n==> {}".format( calculation_method )
            if ( do_print_IN == True ):
                print( output_string )
            #-- END if do_print_IN --#
    
            # if output to file...
            if ( output_to_file_IN == True ):
    
                # store line for output
                my_line_list.append( output_string )
    
            #-- END if output... --#
    
            # binary?  If so, do basic calculations as sanity check.
            if ( calculation_method == cls.CALCULATION_METHOD_BINARY ):
    
                # calculate precision, recall, accuracy...
    
                # ==> precision
                precision = sklearn.metrics.precision_score( baseline_list, derived_binary_list )
    
                # output
                output_string = "\n- {} metrics.precision_score = {}".format( calculation_method, precision )
                if ( do_print_IN == True ):
                    print( output_string )
                #-- END if do_print_IN --#
    
                # if output...
                if ( output_to_file_IN == True ):
    
                    # store line for output
                    my_line_list.append( output_string )
    
                #-- END if output... --#
    
                # ==> recall
                recall = sklearn.metrics.recall_score( baseline_list, derived_binary_list )
    
                # output
                output_string = "- {} metrics.recall_score = {}".format( calculation_method, recall )
                if ( do_print_IN == True ):
                    print( output_string )
                #-- END if do_print_IN --#
    
                # if output...
                if ( output_to_file_IN == True ):
    
                    # store line for output
                    my_line_list.append( output_string )
    
                #-- END if output... --#
    
                # ==> accuracy
                accuracy = sklearn.metrics.accuracy_score( baseline_list, derived_binary_list )
    
                # output
                output_string = "- {} metrics.accuracy_score = {}".format( calculation_method, accuracy )
                if ( do_print_IN == True ):
                    print( output_string )
                #-- END if do_print_IN --#
    
                # if output...
                if ( output_to_file_IN == True ):
    
                    # store line for output
                    my_line_list.append( output_string )
    
                #-- END if output... --#
    
            #-- END check to see if CALCULATION_METHOD_BINARY --#
    
            # calculate based on calculation method.
    
            # default?
            if ( calculation_method == cls.CALCULATION_METHOD_DEFAULT ):
    
                # default metrics and F-Score - default returns a list for each of
                #     the scores per label, so get list and output, don't pick one or
                #     another value.
                default_evaluation = sklearn.metrics.precision_recall_fscore_support( baseline_list, derived_binary_list )
                default_precision_list = default_evaluation[ 0 ]
                default_recall_list = default_evaluation[ 1 ]
                default_F1_list = default_evaluation[ 2 ]
                default_support_list = default_evaluation[ 3 ]
    
                # output lists
                output_string = "\ndefault lists:"
                output_string += "\n- precision list = {}".format( default_precision_list )
                output_string += "\n- recall list = {}".format( default_recall_list )
                output_string += "\n- F1 list = {}".format( default_F1_list )
                output_string += "\n- support list = {}".format( default_support_list )
    
                # add to results map
                method_to_result_map[ calculation_method ] = default_evaluation
    
                # look at length of lists (should all be the same).
                precision_list_length = len( default_precision_list )
                recall_list_length = len( default_recall_list )
                F1_list_length = len( default_F1_list )
    
                output_string += "\n\nlist lengths: {}".format( precision_list_length )
    
                if ( precision_list_length > 2 ):
    
                    # binary, but list is greater than 2, not binary - output message.
                    output_string += "\n- NOTE: default output lists have more than two entries - your data is not binary."
    
                #-- END check to see if list length greater than 2 --#
    
                if ( do_print_IN == True ):
                    print( output_string )
                #-- END if do_print_IN --#
    
                # if output...
                if ( output_to_file_IN == True ):
    
                    # store line for output
                    my_line_list.append( output_string )
    
                #-- END if output... --#
    
            # all others are just argument to "average" parameter, result in one number per
            #     derived score.  For now, implement them the same.
            else:
    
                # F-Score
                evaluation_tuple = sklearn.metrics.precision_recall_fscore_support( baseline_list, derived_binary_list, average = calculation_method )
                precision = evaluation_tuple[ 0 ]
                recall = evaluation_tuple[ 1 ]
                F1 = evaluation_tuple[ 2 ]
                support = evaluation_tuple[ 3 ]
    
                # add to results map
                method_to_result_map[ calculation_method ] = evaluation_tuple
    
                # output
                output_string = "\n{}: precision = {}, recall = {}, F1 = {}, support = {}".format( calculation_method, precision, recall, F1, support )
                if ( do_print_IN == True ):
                    print( output_string )
                #-- END if do_print_IN --#
    
                # if output to file...
                if ( output_to_file_IN == True ):
    
                    # store line for output
                    my_line_list.append( output_string )
    
                #-- END if output... --#
    
            #-- END default F-Score --#
    
        #-- END loop over calculation_methods --#
    
        # RETURN - method-to-result map
        output_dict_OUT[ cls.RETURN_METHOD_TO_RESULT_MAP ] = method_to_result_map
        
        # RETURN - store line_list
        output_dict_OUT[ cls.RETURN_LINE_LIST ] = my_line_list
    
        return output_dict_OUT
        
    #-- END class method precision_recall_f1() --#
    
    
    @classmethod
    def recall_at_k( cls, y_true, y_scores, k ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        threshold = None
        
        # get threshold index
        threshold = cls.threshold_at_k( y_scores, k )
        
        # use threshold to generate predicted scores
        y_pred = numpy.asarray( [ 1 if i >= threshold else 0 for i in y_scores ] )
        
        # calculate recall
        value_OUT = sklearn.metrics.recall_score( y_true, y_pred )
        
        return value_OUT
    
    #-- END function recall_at_k() --#


    @classmethod
    def threshold_at_k( cls, y_scores, k ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        value_list = None
        threshold_index = -1
        
        # sort values
        value_list = numpy.sort( y_scores )
        
        # reverse order of list
        value_list = value_list[ : : -1 ]
        
        # calculate index of value that is k% of the way through the sorted distribution of scores
        threshold_index = int( k * len( y_scores ) )
        
        # get value that is k% of the way through the sorted distribution of scores
        value_OUT = value_list[ threshold_index ]
        
        print( "Threshold: {}".format( value_OUT ) )
        
        return value_OUT
    
    #-- END class method threshold_at_k() --#


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
        
        # related object, if useful (for pandas_ml)
        self.m_related_instance = None

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
        status_message = None
        
        # declare variables - derived metrics
        metric_value = None
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


        #----------------------------------------------------------------------#
        # ! ==> precision - Positive predictive value (PPV), Precision
        #----------------------------------------------------------------------#

        #precision = ( true_positive_count / predicted_positive_count )
 
        if ( ( predicted_positive_count is not None ) and ( predicted_positive_count != 0 ) ):
 
            metric_value = ( true_positive_count / predicted_positive_count )
 
        else:
 
            metric_value = None
            status_message = "ERROR calculating precision"
            status_list_OUT.append( status_message )
 
        #-- END check for division by zero --#        
 
        precision = metric_value
        confusion_metrics.set_value( self.METRIC_PRECISION, precision )
        confusion_metrics.set_value( self.METRIC_PPV, precision )
        

        #----------------------------------------------------------------------#
        # ! ==> recall - True positive rate (TPR), Recall, Sensitivity, probability of detection
        #----------------------------------------------------------------------#

        #recall = ( true_positive_count / ground_truth_positive_count )

        if ( ( ground_truth_positive_count is not None ) and ( ground_truth_positive_count != 0 ) ):

            metric_value = ( true_positive_count / ground_truth_positive_count )

        else:

            metric_value = None
            status_message = "ERROR calculating recall"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        recall = metric_value
        confusion_metrics.set_value( self.METRIC_RECALL, recall )
        confusion_metrics.set_value( self.METRIC_TPR, recall )
        

        #----------------------------------------------------------------------#
        # ! ==> False negative rate (FNR), Miss rate
        #----------------------------------------------------------------------#

        #false_negative_rate = ( false_negative_count / ground_truth_positive_count )

        if ( ( ground_truth_positive_count is not None ) and ( ground_truth_positive_count != 0 ) ):

            metric_value = ( false_negative_count / ground_truth_positive_count )

        else:

            metric_value = None
            status_message = "ERROR calculating false_negative_rate"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        false_negative_rate = metric_value
        confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE_RATE, false_negative_rate )
        confusion_metrics.set_value( self.METRIC_FNR, false_negative_rate )


        #----------------------------------------------------------------------#
        # ! ==> False positive rate (FPR), Fall-out
        #----------------------------------------------------------------------#

        #false_positive_rate = ( false_positive_count / ground_truth_negative_count )

        if ( ( ground_truth_negative_count is not None ) and ( ground_truth_negative_count != 0 ) ):

            metric_value = ( false_positive_count / ground_truth_negative_count )

        else:

            metric_value = None
            status_message = "ERROR calculating false_positive_rate"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        false_positive_rate = metric_value
        confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE_RATE, false_positive_rate )
        confusion_metrics.set_value( self.METRIC_FPR, false_positive_rate )


        #----------------------------------------------------------------------#
        # ! ==> True negative rate (TNR), Specificity (SPC)
        #----------------------------------------------------------------------#

        #true_negative_rate = ( true_negative_count / ground_truth_negative_count )

        if ( ( ground_truth_negative_count is not None ) and ( ground_truth_negative_count != 0 ) ):

            metric_value = ( true_negative_count / ground_truth_negative_count )

        else:

            metric_value = None
            status_message = "ERROR calculating true_negative_rate"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        true_negative_rate = metric_value
        confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE_RATE, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_TNR, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_SPECIFICITY, true_negative_rate )
        confusion_metrics.set_value( self.METRIC_SPC, true_negative_rate )
        

        #----------------------------------------------------------------------#
        # ! ==> False omission rate (FOR)
        #----------------------------------------------------------------------#

        #false_omission_rate = ( false_negative_count / predicted_negative_count )

        if ( ( predicted_negative_count is not None ) and ( predicted_negative_count != 0 ) ):

            metric_value = ( false_negative_count / predicted_negative_count )

        else:

            metric_value = None
            status_message = "ERROR calculating false_omission_rate"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        false_omission_rate = metric_value
        confusion_metrics.set_value( self.METRIC_FALSE_OMISSION_RATE, false_omission_rate )
        confusion_metrics.set_value( self.METRIC_FOR, false_omission_rate )
        

        #----------------------------------------------------------------------#
        # ! ==> Positive likelihood ratio (LR+)
        #----------------------------------------------------------------------#

        tpr = recall
        fpr = false_positive_rate

        #positive_likelihood_ratio = ( tpr / fpr )

        if ( ( tpr is not None ) and ( ( fpr is not None ) and ( fpr != 0 ) ) ):

            metric_value = ( tpr / fpr )

        else:

            metric_value = None
            status_message = "ERROR calculating positive_likelihood_ratio"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        positive_likelihood_ratio = metric_value
        confusion_metrics.set_value( self.METRIC_POSITIVE_LIKELIHOOD_RATIO, positive_likelihood_ratio )
        confusion_metrics.set_value( self.METRIC_LR_PLUS, positive_likelihood_ratio )
        

        #----------------------------------------------------------------------#
        # ! ==> Negative likelihood ratio (LR-)
        #----------------------------------------------------------------------#

        fnr = false_negative_rate
        tnr = true_negative_rate

        #negative_likelihood_ratio = ( fnr / tnr )

        if ( ( fnr is not None ) and ( ( tnr is not None ) and ( tnr != 0 ) ) ):

            metric_value = ( fnr / tnr )

        else:

            metric_value = None
            status_message = "ERROR calculating negative_likelihood_ratio"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        negative_likelihood_ratio = metric_value
        confusion_metrics.set_value( self.METRIC_NEGATIVE_LIKELIHOOD_RATIO, negative_likelihood_ratio )
        confusion_metrics.set_value( self.METRIC_LR_MINUS, negative_likelihood_ratio )
        

        #----------------------------------------------------------------------#
        # ! ==> Accuracy (ACC)
        #----------------------------------------------------------------------#

        total_population = true_positive_count + true_negative_count + false_positive_count + false_negative_count

        #accuracy = ( ( true_positive_count + true_negative_count ) / total_population )

        if ( ( total_population is not None ) and ( total_population != 0 ) ):

            metric_value = ( ( true_positive_count + true_negative_count ) / total_population )

        else:

            metric_value = None
            status_message = "ERROR calculating accuracy"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#

        accuracy = metric_value
        confusion_metrics.set_value( self.METRIC_ACCURACY, accuracy )
        confusion_metrics.set_value( self.METRIC_ACC, accuracy )
        confusion_metrics.set_value( self.METRIC_TOTAL_POPULATION, total_population )
        

        #----------------------------------------------------------------------#
        # ! ==> False discovery rate (FDR), probability of false alarm
        #----------------------------------------------------------------------#

        #false_discovery_rate = ( false_positive_count / predicted_positive_count )

        if ( ( predicted_positive_count is not None ) and ( predicted_positive_count != 0 ) ):

            metric_value = ( false_positive_count / predicted_positive_count )

        else:

            metric_value = None
            status_message = "ERROR calculating false_discovery_rate"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#

        false_discovery_rate = metric_value
        confusion_metrics.set_value( self.METRIC_FALSE_DISCOVERY_RATE, false_discovery_rate )
        confusion_metrics.set_value( self.METRIC_FDR, false_discovery_rate )
        

        #----------------------------------------------------------------------#
        # ! ==> Negative predictive value (NPV)
        #----------------------------------------------------------------------#

        #negative_predictive_value = ( true_negative_count / predicted_negative_count )

        if ( ( predicted_negative_count is not None ) and ( predicted_negative_count != 0 ) ):

            metric_value = ( true_negative_count / predicted_negative_count )

        else:

            metric_value = None
            status_message = "ERROR calculating negative_predictive_value"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        negative_predictive_value = metric_value
        confusion_metrics.set_value( self.METRIC_NEGATIVE_PREDICTIVE_VALUE, negative_predictive_value )
        confusion_metrics.set_value( self.METRIC_NPV, negative_predictive_value )


        #----------------------------------------------------------------------#
        # ! ==> Diagnostic odds ratio (DOR)
        #----------------------------------------------------------------------#

        lr_plus = positive_likelihood_ratio
        lr_minus = negative_likelihood_ratio

        #diagnostic_odds_ratio = ( lr_plus / lr_minus )

        if ( ( lr_plus is not None ) and ( ( lr_minus is not None ) and ( lr_minus != 0 ) ) ):

            metric_value = ( lr_plus / lr_minus )

        else:

            metric_value = None
            status_message = "ERROR calculating diagnostic_odds_ratio"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#

        diagnostic_odds_ratio = metric_value
        confusion_metrics.set_value( self.METRIC_DIAGNOSTIC_ODDS_RATIO, diagnostic_odds_ratio )
        confusion_metrics.set_value( self.METRIC_DOR, diagnostic_odds_ratio )


        #----------------------------------------------------------------------#
        # ! ==> F1 score
        #----------------------------------------------------------------------#

        #f1_score = ( 2 / ( ( 1 / recall ) + ( 1 / precision ) ) )

        if ( ( ( recall is not None ) and ( recall != 0 ) )
             and ( ( precision is not None ) and ( precision != 0 ) ) ):

            metric_value = ( 2 / ( ( 1 / recall ) + ( 1 / precision ) ) )

        else:

            metric_value = None
            status_message = "ERROR calculating f1_score"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        f1_score = metric_value
        confusion_metrics.set_value( self.METRIC_F_ONE_SCORE, f1_score )
        

        #----------------------------------------------------------------------#
        # ! ==> Matthews correlation coefficient (MCC)
        #----------------------------------------------------------------------#

        numerator = ( ( true_positive_count * true_negative_count ) - ( false_positive_count * false_negative_count ) )
        temp_math = ( ( true_positive_count + false_positive_count ) * ( true_positive_count + false_negative_count ) * ( true_negative_count + false_positive_count ) * ( true_negative_count + false_negative_count ) )
        denominator = math.sqrt( temp_math )

        #matthews_correlation_coefficient = ( numerator / denominator )

        if ( ( denominator is not None ) and ( denominator != 0 ) ):

            metric_value = ( numerator / denominator )

        else:

            metric_value = None
            status_message = "ERROR calculating matthews_correlation_coefficient"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        matthews_correlation_coefficient = metric_value
        confusion_metrics.set_value( self.METRIC_MATTHEWS_CORRELATION_COEFFICIENT, matthews_correlation_coefficient )
        confusion_metrics.set_value( self.METRIC_MCC, matthews_correlation_coefficient )
                

        #----------------------------------------------------------------------#
        # ! ==> Informedness or Bookmaker Informedness (BM)
        #----------------------------------------------------------------------#

        #informedness = tpr + tnr - 1

        if ( ( tpr is not None ) and ( tnr is not None ) ):

            metric_value = tpr + tnr - 1

        else:

            metric_value = None
            status_message = "ERROR calculating informedness"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        informedness = metric_value
        confusion_metrics.set_value( self.METRIC_INFORMEDNESS, informedness )
        confusion_metrics.set_value( self.METRIC_BM, informedness )


        #----------------------------------------------------------------------#
        # ! ==> Markedness (MK) = PPV + NPV − 1 
        #----------------------------------------------------------------------#

        ppv = precision
        npv = negative_predictive_value

        #markedness = ppv + npv - 1

        if ( ( ppv is not None ) and ( npv is not None ) ):

            metric_value = ppv + npv - 1

        else:

            metric_value = None
            status_message = "ERROR calculating markedness"
            status_list_OUT.append( status_message )

        #-- END check for division by zero --#        

        markedness = metric_value
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


    def get_related_instance( self ):
    
        # return reference
        value_OUT = None
        
        # declare variables

        # get m_predicted_values
        value_OUT = self.m_related_instance
        
        return value_OUT
    
    #-- END method get_related_instance --#


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


    def populate_pandas_ml( self,
                            ground_truth_values_IN,
                            predicted_values_IN,
                            derive_metrics_IN = True ):
                              
        # return reference
        instance_OUT = self
    
        # declare variables
        me = "populate_pandas_ml"
        error_string = ""
        ground_truth_length = -1
        predicted_length = -1
        ground_truth_list = None
        predicted_list = None
        y_actu = None
        y_pred = None
        confusion_matrix = None
        ground_truth_positive_count = 0
        predicted_positive_count = 0
        true_positive_count = 0
        false_positive_count = 0
        ground_truth_negative_count = 0
        predicted_negative_count = 0
        true_negative_count = 0
        false_negative_count = 0
        stats_dict = None
        
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

                    # pandas_ml
                    # http://pandas-ml.readthedocs.io/en/stable/conf_mat.html
                    confusion_matrix = pandas_ml.ConfusionMatrix( ground_truth_list, predicted_list )
                    self.set_related_instance( confusion_matrix )

                    if ( self.DEBUG_FLAG == True ):
                        print( str( confusion_matrix ) )
                    #-- END DEBUG --#

                    # get counts in variables
                    true_positive_count = confusion_matrix.TP
                    false_positive_count = confusion_matrix.FP
                    true_negative_count = confusion_matrix.TN
                    false_negative_count = confusion_matrix.FN
                    
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
                        
                        # retrieve the stats dict generated by ConfusionMatrix
                        stats_dict = confusion_matrix.stats()
                        
                        # example: OrderedDict([('population', 2446), ('P', 2378), ('N', 68), ('PositiveTest', 2383), ('NegativeTest', 63), ('TP', 2315), ('TN', 0), ('FP', 68), ('FN', 63), ('TPR', 0.97350714886459211), ('TNR', 0.0), ('PPV', 0.97146454049517417), ('NPV', 0.0), ('FPR', 1.0), ('FDR', 0.02853545950482585), ('FNR', 0.026492851135407905), ('ACC', 0.94644317252657395), ('F1_score', 0.97248477210670026), ('MCC', -0.027495193775309384), ('informedness', -0.026492851135407891), ('markedness', -0.028535459504825833), ('prevalence', 0.97219950940310706), ('LRP', 0.97350714886459211), ('LRN', inf), ('DOR', 0.0), ('FOR', 1.0)])
                        
                        #confusion_metrics.set_value( self.METRIC_POPULATION_POSITIVE, ground_truth_positive_count )  

                        # population
                        confusion_metrics.set_value( self.METRIC_TOTAL_POPULATION, stats_dict[ "population" ] )                        

                        # P
                        confusion_metrics.set_value( self.METRIC_POPULATION_POSITIVE, stats_dict[ "P" ] )

                        # N
                        confusion_metrics.set_value( self.METRIC_POPULATION_NEGATIVE, stats_dict[ "N" ] )

                        # PositiveTest
                        confusion_metrics.set_value( self.METRIC_PREDICTED_POSITIVE, stats_dict[ "PositiveTest" ] )

                        # NegativeTest
                        confusion_metrics.set_value( self.METRIC_PREDICTED_NEGATIVE, stats_dict[ "NegativeTest" ] )

                        # TP
                        confusion_metrics.set_value( self.METRIC_TRUE_POSITIVE, stats_dict[ "TP" ] )

                        # TN
                        confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE, stats_dict[ "TN" ] )

                        # FP
                        confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE, stats_dict[ "FP" ] )

                        # FN
                        confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE, stats_dict[ "FN" ] )
                        
                        # TPR
                        confusion_metrics.set_value( self.METRIC_RECALL, stats_dict[ "TPR" ] )
                        confusion_metrics.set_value( self.METRIC_TPR, stats_dict[ "TPR" ] )
                        
                        # TNR
                        confusion_metrics.set_value( self.METRIC_SPECIFICITY, stats_dict[ "TNR" ] )
                        confusion_metrics.set_value( self.METRIC_SPC, stats_dict[ "TNR" ] )
                        confusion_metrics.set_value( self.METRIC_TRUE_NEGATIVE_RATE, stats_dict[ "TNR" ] )
                        confusion_metrics.set_value( self.METRIC_TNR, stats_dict[ "TNR" ] )
                        
                        # PPV
                        confusion_metrics.set_value( self.METRIC_PRECISION, stats_dict[ "PPV" ] )
                        confusion_metrics.set_value( self.METRIC_PPV, stats_dict[ "PPV" ] )
                        
                        # NPV
                        confusion_metrics.set_value( self.METRIC_NEGATIVE_PREDICTIVE_VALUE, stats_dict[ "NPV" ] )
                        confusion_metrics.set_value( self.METRIC_NPV, stats_dict[ "NPV" ] )
                        
                        # FPR
                        confusion_metrics.set_value( self.METRIC_FALSE_POSITIVE_RATE, stats_dict[ "FPR" ] )
                        confusion_metrics.set_value( self.METRIC_FPR, stats_dict[ "FPR" ] )
                        
                        # FDR
                        confusion_metrics.set_value( self.METRIC_FALSE_DISCOVERY_RATE, stats_dict[ "FDR" ] )
                        confusion_metrics.set_value( self.METRIC_FDR, stats_dict[ "FDR" ] )
                        
                        # FNR
                        confusion_metrics.set_value( self.METRIC_FALSE_NEGATIVE_RATE, stats_dict[ "FNR" ] )                        
                        confusion_metrics.set_value( self.METRIC_FNR, stats_dict[ "FNR" ] )                        
                        
                        # ACC
                        confusion_metrics.set_value( self.METRIC_ACC, stats_dict[ "ACC" ] ) 
                        confusion_metrics.set_value( self.METRIC_ACCURACY, stats_dict[ "ACC" ] ) 

                        # F1_score
                        confusion_metrics.set_value( self.METRIC_F_ONE_SCORE, stats_dict[ "F1_score" ] )
                        
                        # MCC
                        confusion_metrics.set_value( self.METRIC_MATTHEWS_CORRELATION_COEFFICIENT, stats_dict[ "MCC" ] )
                        confusion_metrics.set_value( self.METRIC_MCC, stats_dict[ "MCC" ] )
                        
                        # Informedness
                        confusion_metrics.set_value( self.METRIC_INFORMEDNESS, stats_dict[ "informedness" ] )                        
                        confusion_metrics.set_value( self.METRIC_BM, stats_dict[ "informedness" ] )
                        
                        # markedness
                        confusion_metrics.set_value( self.METRIC_MARKEDNESS, stats_dict[ "markedness" ] )                        
                        confusion_metrics.set_value( self.METRIC_MK, stats_dict[ "markedness" ] )
                        
                        # prevalence
                        # LRP
                        confusion_metrics.set_value( self.METRIC_POSITIVE_LIKELIHOOD_RATIO, stats_dict[ "LRP" ] )
                        confusion_metrics.set_value( self.METRIC_LR_PLUS, stats_dict[ "LRP" ] )

                        # LRN
                        confusion_metrics.set_value( self.METRIC_NEGATIVE_LIKELIHOOD_RATIO, stats_dict[ "LRN" ] )
                        confusion_metrics.set_value( self.METRIC_LR_MINUS, stats_dict[ "LRN" ] )
                        
                        # DOR
                        confusion_metrics.set_value( self.METRIC_DIAGNOSTIC_ODDS_RATIO, stats_dict[ "DOR" ] ) 
                        confusion_metrics.set_value( self.METRIC_DOR, stats_dict[ "DOR" ] )                         
                        
                        # FOR
                        confusion_metrics.set_value( self.METRIC_FALSE_OMISSION_RATE, stats_dict[ "FOR" ] ) 
                        confusion_metrics.set_value( self.METRIC_FOR, stats_dict[ "FOR" ] ) 
                    
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
        
    #-- END method populate_pandas_ml() --#


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
        
    #-- END method set_predicted_values() --#


    def set_related_instance( self, instance_IN ):
        
        '''
        Accepts related_instance.  Stores it and returns it.
        '''
        
        # return reference
        value_OUT = None
        
        # use store dictionary.
        self.m_related_instance = instance_IN
        
        # return it.
        value_OUT = self.get_related_instance()
        
        return value_OUT
        
    #-- END method set_related_instance() --#


#-- END class ConfusionMatrixHelper --#
