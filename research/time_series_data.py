'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/python_utilities.

python_utilities is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/python_utilities.  If not, see
<http://www.gnu.org/licenses/>.
'''

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

@python_2_unicode_compatible
class AbstractTimeSeriesDataModel( models.Model ):

    #============================================================================
    # constants-ish
    #============================================================================

    # time period types
    TIME_PERIOD_HOURLY = "hourly"

    #============================================================================
    # Django model fields
    #============================================================================
    
    start_date = models.DateTimeField( null = True, blank = True )
    end_date = models.DateTimeField( null = True, blank = True )
    time_period_type = models.CharField( max_length = 255, null = True, blank = True ) # - hourly, by minute, etc.
    filter_type = models.CharField( max_length = 255, null = True, blank = True ) # - place to keep track of different filter types, if you want.  Example: "text_contains"
    filter_value = models.CharField( max_length = 255, null = True, blank = True )
    time_period_label = models.CharField( max_length = 255, null = True, blank = True ) # could give each hour, etc. a separate identifier "start+1", "start+2", etc. - not naming _id to start, so you leave room for this to be a separate table.
    match_value = models.CharField( max_length = 255, null = True, blank = True )

    #============================================================================
    # Instance variables
    #============================================================================
    
    
    #============================================================================
    # meta class
    #============================================================================

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True

    # add string output method.
    
#-- END abstract class AbstractTimeSeriesData --#


@python_2_unicode_compatible
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