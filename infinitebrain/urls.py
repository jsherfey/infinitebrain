from django.conf.urls import patterns, include, url
from django.contrib import admin
#from wiki.urls import get_pattern as get_wiki_pattern
#from django_nyt.urls import get_pattern as get_nyt_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
import qhonuskan_votes.urls
admin.autodiscover()
import haystack
from haystack.views import SearchView
from haystack.forms import ModelSearchForm
from views import AuthenticatedSearchView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'infinitebrain.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'infinitebrain.views.home', name='home'),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'infinitebrain.views.login_user', name='login'),
    url(r'^logout/$', 'infinitebrain.views.logout_user'),#' 'django.contrib.auth.views.logout'),
    url(r'^dashboard/','infinitebrain.views.dashboard', name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^models/', include('modeldb.urls',namespace="modeldb")),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^votes/', include(qhonuskan_votes.urls)),
    url(r'^setup/', 'infinitebrain.views.setup'),
    url(r'^notifications/', get_nyt_pattern()),
#    url(r'^wiki/', get_wiki_pattern()),
    # url(r'^search/', include('haystack.urls')),
    url(r'^media/(?P<filename>.*)$', 'infinitebrain.views.download_model')
)
# the following will 
urlpatterns += patterns('haystack.views',
    url(r'^search/',AuthenticatedSearchView(
        ),
    name='haystack_search'),
    )