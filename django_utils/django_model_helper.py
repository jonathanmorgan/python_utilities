'''
Copyright 2016 to present (2016) - Jonathan Morgan

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

class DjangoModelHelper( object ):
    

    #===========================================================================
    # ! ==> class variables
    #===========================================================================

    # names of reverse lookup classes.
    CLASS_NAME_REVERSE_1_TO_1_OLD = "SingleRelatedObjectDescriptor"
    CLASS_NAME_REVERSE_1_TO_1_NEW = "ReverseOneToOneDescriptor"
    CLASS_NAME_REVERSE_M_TO_1_OLD = "ForeignRelatedObjectsDescriptor"
    CLASS_NAME_REVERSE_M_TO_1_NEW = "ReverseManyToOneDescriptor"
    CLASS_NAME_REVERSE_GENERIC_M_TO_1_OLD = "ReverseGenericRelatedObjectsDescriptor"
    CLASS_NAME_REVERSE_GENERIC_M_TO_1_NEW = "ReverseGenericManyToOneDescriptor"
    CLASS_NAME_M_TO_M_OLD = "ManyRelatedObjectsDescriptor"
    CLASS_NAME_M_TO_M_NEW = "ManyToManyDescriptor"
    
    REVERSE_LOOKUP_CLASS_NAMES = [ CLASS_NAME_REVERSE_1_TO_1_OLD,
                                   CLASS_NAME_REVERSE_1_TO_1_NEW,
                                   CLASS_NAME_REVERSE_M_TO_1_OLD,
                                   CLASS_NAME_REVERSE_M_TO_1_NEW,
                                   CLASS_NAME_REVERSE_GENERIC_M_TO_1_OLD,
                                   CLASS_NAME_REVERSE_GENERIC_M_TO_1_NEW,
                                   CLASS_NAME_M_TO_M_OLD,
                                   CLASS_NAME_M_TO_M_NEW ]


#-- END class DjangoModelHelper --#