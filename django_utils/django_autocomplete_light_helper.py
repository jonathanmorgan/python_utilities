"""
Installation of "django-autocomplete-light":
- https://django-autocomplete-light.readthedocs.io/en/master/install.html
- Use pip to install "django-autocomplete-light" and dependencies.
- In settings.py:

    - add "dal" and "dal_select2" to the top of INSTALLED_APPS (make sure it is before "grapelli" if installed, and before "django.contrib.admin"):

            'dal',
            'dal_select2',
            # 'grappelli',
            'django.contrib.admin',

- Touch your project's wsgi.py file to reload applications.
- Run "python manage.py collectstatic".

To add a new autocomplete:
- https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html
- create a class-based autocomplete view for your model. Example is at the end of this file.
- create a URL route for your autocomplete view. Example:

        from context_text.views import PersonAutocomplete

        # context_text URL settings, intended to be included in master urls.py file.
        urlpatterns = [

            ...,

            # django-autocomplete-light
            url(
                r'^autocomplete_person/$',
                PersonAutocomplete.as_view(),
                name='autocomplete-person',
            ),
            
            ...,

        ]

- Ensure that the url can be reversed, ie:

        ./manage.py shell
        In [1]: from django.urls import reverse
        In [2]: #older django versions: from django.core.urlresolvers import reverse

        In [3]: reverse('autocomplete-person')
        Out[2]: u'/context/text/autocomplete-person/'

- You should be able to access the autocomplete view now once you are logged in:

        https://research.local/research/context/text/autocomplete_person/?q=f

- use the view in a form widget. In your form, for the field you want to autocomplete:

    - make it a "`forms.ModelChoiceField`".
    - in the call to "`forms.ModelChoiceField`", set:

        - "queryset" to the model's "<model>.objects.all()".
        - "widget" to "`autocomplete.ModelSelect2( url = '<name_from_urls.py>' )`"

    - example:

            # django-autocomplete-light imports
            from dal import autocomplete

            class ArticleCodingForm( forms.ModelForm ):

                '''
                Create a form to let a user look up the source.
                '''

                class Meta:
                    model = Article_Subject
                    fields = [ "person", ]

                    #exclude = [ 'article_data', 'original_person', 'match_confidence_level', 'match_status', 'capture_method', 'create_date', 'last_modified', 'source_type', 'subject_type', 'name', 'verbatim_name', 'lookup_name', 'title', 'more_title', 'organization', 'document', 'topics', 'source_contact_type', 'source_capacity', 'localness', 'notes', 'organization_string', 'more_organization' ]

                # AJAX lookup for person.
                #person  = make_ajax_field( Article_Subject, 'person', 'coding_person', help_text = "" )
                person = forms.ModelChoiceField(
                    queryset = Person.objects.all(),
                    widget = autocomplete.ModelSelect2( url = 'autocomplete-person' )
                )

            #-- END ModelForm class ArticleCodingForm --#

- in template

    - make sure to include your form's "`.media`", after including jquery.  Example for the above form being named "person_lookup_form" in a view passed to template:

            <!-- pull in same jquery as used by django admin -->
            <script type="text/javascript" src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>
            
            <!-- pull in dal scripts -->
            {{ person_lookup_form.media }}

    - then, just output the form's html somewhere in the template. Example:

            <p class="inputContainer" id="lookup-person-id" name="lookup-person-id">
                <h4>Person lookup</h4>
                <div class="lookupPersonExistingId" id="lookup-person-existing-id" name="lookup-person-existing-id"></div>
                <input type="button" id="lookup-person-name" name="lookup-person-name" value="Fetch Name ==>" /> | <input type="button" id="clear-person-lookup" name="clear-person-lookup" value="Clear Person Lookup" />
                <br />
                <br />
                {{ person_lookup_form }}
            </p>
            
- interacting with the DAL lookup via events:

    - TK.

"""


# python imports
import logging

# django imports
from django.db.models import Q

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper


#===============================================================================#
# ! Parent Lookup class
#===============================================================================#


class DalHelper( LoggingHelper ):

    #--------------------------------------------------------------------------#
    # ! Constants-ish
    #--------------------------------------------------------------------------#


    DEBUG = False
    LOGGER_NAME = "python_utilities.django_utils.django_autocomplete_light_helper.DalHelper"


    #--------------------------------------------------------------------------#
    # ! class methods
    #--------------------------------------------------------------------------#


    @classmethod
    def get_instance_query( cls, q, request, class_IN ):
    
        """
            return a query set if q passed in is an integer, and that number is
            the ID of one of the records in our class's database table.  You
            also have access to request.user if needed.
        """

        # return reference
        query_set_OUT = None

        # define variables
        my_class = None
        q_int = -1
        q_instance = ''

        # store class
        my_class = class_IN

        # is the q a number?
        try:

            # try casting the query string to int.
            q_int = int( q )

            # it is an int.  See if there is a match for this ID.
            q_instance = my_class.objects.get( pk = q_int )

            # got a match?
            if ( q_instance ):

                # it is a match - return query set with that article in it.
                query_set_OUT = my_class.objects.filter( Q( pk__in = [ q ] ) )

            else:

                # no match found.  Return None.
                query_set_OUT = None

            #-- END check to see if we got an instance. --#

        except:

            # not an integer.  set found to false.
            #found_instance = False
            query_set_OUT = None

        #-- END attempt to pull in instance by ID --#

        return query_set_OUT

    #-- END method get_instance_query() --#


    #--------------------------------------------------------------------------#
    # ! instance methods
    #--------------------------------------------------------------------------#


    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( DalHelper, self ).__init__()
        
        # initialize variables
        self.my_class = None
        
    #-- END method __init__() --#

    def format_result( self, instance_IN ):

        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """

        # return reference
        string_OUT = ''

        # try converting to string.  If exception, try calling method
        #    output_as_string() instead.
        try:

            # first, try using str()
            string_OUT = str( instance_IN )

        except:

            # if we get here, exception converting.  Try output_as_string()
            string_OUT = instance_IN.output_as_string( True )

        return string_OUT

    #-- END method format_result() --#


    def format_item( self, instance_IN ):

        """ the display of a currently selected object in the area below the search box. html is OK """

         # return reference
        string_OUT = ''
        
        # try converting to string.  If exception, try calling method
        #    output_as_string() instead.
        try:
            
            # first, try using str()
            string_OUT = str( instance_IN )
            
        except:
            
            # if we get here, exception converting.  Try output_as_string()
            string_OUT = instance_IN.output_as_string( True )

        return string_OUT

    #-- END method format_item() --#


    # new required method - surprise!
    def format_item_display( self, instance_IN ):
        
        '''
        accepts item, calls format_item(), returns result.
        '''
        
        # return reference
        string_OUT = ""
        
        # call format_item()
        string_OUT = self.format_item( instance_IN )
        
        return string_OUT
    
    #-- END method format_item_display() --#

#-- END class DalHelper --#


#===============================================================================#
# ! Example individual Lookup class-based view
#===============================================================================#

'''
#===============================================================================
# ! ==> imports (in alphabetical order by package, then by name)
#===============================================================================


# django class-based view imports
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# python_utilities
from python_utilities.django_utils.django_autocomplete_light_helper import DalHelper

# django-autocomplete-light
from dal import autocomplete


#===============================================================================
# ! ==> class-based view classes (in alphabetical order)
#===============================================================================


@method_decorator( login_required, name='dispatch' )
class PersonAutocomplete( autocomplete.Select2QuerySetView ):

    #--------------------------------------------------------------------------#
    # ! Constants-ish
    #--------------------------------------------------------------------------#


    # this autocomplete's related class.
    MY_LOOKUP_CLASS = Person


    #============================================================================
    # ! ==> Built-in Instance methods
    #============================================================================


    def __init__( self, *args, **kwargs ):
        
        # always call parent's __init__()
        super( PersonAutocomplete, self ).__init__()

    #-- END overridden built-in __init__() method --#
        

    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def get_queryset( self ):

        """
        return a query set.  you also have access to request.user if needed.
        """

        # return reference
        qs_OUT = None

        # declare variables
        me = "get_queryset"
        my_request = None
        my_q = None
        my_lookup_class = None
        my_logger_name = ""
        person_search_string = ""
        
        # init.
        my_request = self.request
        my_q = self.q
        my_lookup_class = self.MY_LOOKUP_CLASS
        my_logger_name = "context_text.views.PersonAutocomplete"

        # Don't forget to filter out results depending on the visitor !

        # is user authenticated? 
        if ( my_request.user.is_authenticated == True ):

            # store q in a real variable
            person_search_string = my_q
            
            # output string passed in
            DalHelper.output_debug( "q = " + str( my_q ), method_IN = me, logger_name_IN = my_logger_name )

            # is the q a number and is it the ID of an contributor?
            qs_OUT = DalHelper.get_instance_query( person_search_string, my_request, my_lookup_class )

            # got anything back?
            if ( qs_OUT is None ):

                # No exact match for q as ID.  Try Person.find_person_from_name()
                qs_OUT = my_lookup_class.find_person_from_name( person_search_string, do_strict_match_IN = False, do_partial_match_IN = True )
                
            #-- END retrieval of QuerySet when no ID match. --#

        else:

            # user not authenticated - return empty QuerySet.
            qs_OUT = my_lookup_class.objects.none()

        #-- END check to see if user authenticated. --#

        return qs_OUT

    #-- END method get_queryset() --#

#-- END class-based view PersonAutocomplete --#
'''

