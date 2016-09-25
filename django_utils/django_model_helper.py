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

# imports - python_utilities
from python_utilities.status.status_container import StatusContainer

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

    #===========================================================================
    # ! ==> class methods
    #===========================================================================


    @classmethod
    def copy_m2m_values( cls, attr_name_IN, copy_from_IN, copy_to_IN, *args, **kwargs ):
        
        '''
        Accepts the name of the ManyToMany (m2m) field you want to copy from
            one instance of a given model class to another, the instance you
            want to copy from, and the instance you want to copy to.  Loops over
            items in the from instance for the field and adds each to the field
            in the to instance.  If error returns status of error and message
            that describes the problem.
            
        Postconditions: the copy-to instance is updated, but not saved.  If 
            error returned, the copy-to instance is not updated.
        '''
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "copy_m2m_values"
        status_message = ""
        copy_m2m_from = None
        copy_m2m_to = None
        m2m_qs = None
        m2m_instance = None
        
        # init status container
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got an attribute name?
        if ( ( attr_name_IN is not None ) and ( attr_name_IN != "" ) ):
        
            # got copy_from_IN instance?
            if ( copy_from_IN is not None ):
            
                # got copy_to_IN instance?
                if ( copy_to_IN is not None ):
                
                    # ! ----> ManyToMany - topics
                    copy_m2m_from = getattr( copy_from_IN, attr_name_IN )
                    copy_m2m_to = getattr( copy_to_IN, attr_name_IN )
                    
                    # loop over existing items
                    m2m_qs = copy_m2m_from.all()
                    for m2m_instance in m2m_qs:
                    
                        # add to new.
                        copy_m2m_to.add( m2m_instance )
                    
                    #-- END loop over m2m instances --#
                    
                else:
                
                    # error - must have attribute name.
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            
                    # add a status message
                    status_message = "No instance passed in to copy TO."
                    status_OUT.add_message( status_message )
                
                #-- END check to see if copy_to_IN --#
    
            else:
            
                # error - must have attribute name.
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
        
                # add a status message
                status_message = "No instance passed in to copy FROM."
                status_OUT.add_message( status_message )
            
            #-- END check to see if copy_from_IN --#
            
        else:
        
            # error - must have attribute name.
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
    
            # add a status message
            status_message = "No attribute name passed in ( " + str( attr_name_IN ) + " )"
            status_OUT.add_message( status_message )
            
        #-- END check for attribute name --#
        
    #-- END class method copy_m2m_values() --#
    

#-- END class DjangoModelHelper --#