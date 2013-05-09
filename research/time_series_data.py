'''
Contains django abstract model class for creating and storing time-series data
   in a database.  For now, will have an abstract class and then a concrete
   implementation of it that can be used for generic time-series data. If you
   are serious about this, you should extend the abstract class and then add on
   the different pieces of data you want to capture per time slice in a child
   class.
'''

# imports
from __future__ import unicode_literals

# django
from django.db import models

class AbstractTimeSeriesDataModel( models.Model ):

    #============================================================================
    # Django model fields.
    #============================================================================
    
    start_date = models.DateTimeField( null = True, blank = True )
    end_date = models.DateTimeField( null = True, blank = True )
    time_period_type = models.CharField( max_length = 255, null = True, blank = True ) # - hourly, by minute, etc.
    filter_type = models.CharField( max_length = 255, null = True, blank = True ) # - place to keep track of different filter types, if you want.  Example: "text_contains"
    filter_value = models.CharField( max_length = 255, null = True, blank = True )
    time_period_label = models.CharField( max_length = 255, null = True, blank = True ) # could give each hour, etc. a separate identifier "start+1", "start+2", etc. - not naming _id to start, so you leave room for this to be a separate table.
    match_value = models.CharField( max_length = 255, null = True, blank = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True

    # add string output method.
    
#-- END abstract class AbstractTimeSeriesData --#


class BasicTimeSeriesData( AbstractTimeSeriesDataModel ):

    #============================================================================
    # Django model fields from parent.
    #============================================================================
    
    #start_date = models.DateTimeField( null = True, blank = True )
    #end_date = models.DateTimeField( null = True, blank = True )
    #time_period_type = models.CharField( max_length = 255, null = True, blank = True ) # - hourly, by minute, etc.
    #filter_type = models.CharField( max_length = 255, null = True, blank = True ) # - place to keep track of different filter types, if you want.  Example: "text_contains"
    #filter_value = models.CharField( max_length = 255, null = True, blank = True )
    #time_period_label = models.CharField( max_length = 255, null = True, blank = True ) # could give each hour, etc. a separate identifier "start+1", "start+2", etc. - not naming _id to start, so you leave room for this to be a separate table.
    #match_value = models.CharField( max_length = 255, null = True, blank = True )

    pass
    
#-- END abstract class BasicTimeSeriesData --# 