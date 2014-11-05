from django.http import *
from django.shortcuts import render_to_response,redirect,render,get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from modeldb.models import Model, ModelRelation
from django.utils import simplejson
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from haystack.views import SearchView


# Create your views here.
def home(request):
    return render(request, 'site/home.html',context_instance=RequestContext(request))#{'user': request.user})

def setup(request):
    return render(request, 'site/setup.html',context_instance=RequestContext(request))

def login_user(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
    # the following line directs to home page if failed authentication
    return render(request, 'site/home.html', {'auth_failed': True})

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
@csrf_exempt
def dashboard(request):
    models = Model.objects.filter(user=request.user).order_by('-date_added')
    links = ModelRelation.objects.filter(Q(target__user=request.user) | Q(source__user=request.user))
    d = [{"source":r.source.name,"target":r.target.name,"type":"connection"} for r in links]
    link_data = simplejson.dumps(d)
    return render(request, 'site/dashboard.html',{'models': models, "link_data": link_data},context_instance=RequestContext(request))


class AuthenticatedSearchView(SearchView):
    def get_results(self):
        results = super(AuthenticatedSearchView, self).get_results()
        # next line is for development
        # self.request.user = authenticate(username='john', password='johnpassword')
        if self.request.user.is_authenticated():
            results = results.filter(Q(user=self.request.user) | Q(user=None) | Q(privacy='public'));
        else:
            results = results.filter(Q(user=None) | Q(privacy='public') | Q(privacy='unlisted'));
        results = results.order_by('-date_added')
        return results