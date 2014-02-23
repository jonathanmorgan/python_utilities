'''
Copyright 2014 Jonathan Morgan

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

# start to python 3 support:
from __future__ import unicode_literals

# python standard library imports
import gc

# django imports
import django.db

class DjangoMemoryHelper( object ):
    

    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def free_memory( cls, *args, **kwargs ):
        
        """
        Does everything I know how to do in django to free up memory.
        """
    
        # return reference
        status_OUT = "Success!"
        
        # memory management
        gc.collect()
        django.db.reset_queries()
    
        return status_OUT
    
    #-- END free_memory() function --#


#-- END class DjangoMemoryHelper --#