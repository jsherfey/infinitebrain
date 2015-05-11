from django.conf.urls import patterns, url
from modeldb import views
# for voting:
#from modeldb.models import Model
#from voting.views import vote_on_object
#from django.views.generic.list import ListView

urlpatterns = patterns('',
    # Generic view to list Link objects
    # ex: /list/
#    url(r'^list/?$', ListView, dict(queryset=Model.objects.all(),
#        template_object_name='model', template_name='modeldb/model_list.html',
#        paginate_by=15, allow_empty=True)),
    # Generic view to vote on Model objects
    # ex: /list/1/...
#    (r'^list/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
#        vote_on_object, dict(model=Model, template_object_name='model',
#            template_name='modeldb/model_confirm_vote.html',
#            allow_xmlhttprequest=True)),                       
    # ex: /models/
    url(r'^$', views.index, name='index'),
    # ex: /models/5/
    url(r'^(?P<model_id>\d+)/$', views.detail, name='detail'),
    # ex: /models/graph
    url(r'^graph/(?P<model_id>\d+)/$', views.graph, name='graph'),
    url(r'^evolution/$', views.evolution, name='evolution'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^add/$', views.add_model, name='add_model'),
)
