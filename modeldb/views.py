from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from modeldb.models import Model, ModelSpec, ModelRelation, Project, Citation
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext #, loader
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
#from django.views.decorators.csrf import ensure_csrf_cookie
#@ensure_csrf_cookie

# Create your views here.
def index(request):
    #models = Model.objects.order_by('-date_added')#[:5]
    models = Model.sort_by_score.all().filter(~Q(level='mechanism'), Q(privacy='public'))#.order_by('-date_added')
    context = {'models': models}
    return render(request, 'modeldb/index.html', context,context_instance=RequestContext(request))
    # Note: The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.
    #template = loader.get_template('modeldb/index.html')
    #context = RequestContext(request, {'latest_model_list': latest_model_list})
    #return HttpResponse(template.render(context))
    #return HttpResponse("Hello, world. You're at the model index.")

def detail(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    return render(request, 'modeldb/detail.html',{'model':model})
    #try:
    #    model=Model.objects.get(pk=model_id)
    #except Model.DoesNotExist:
    #    raise Http404
    #return render(request, 'modeldb/detail.html',{'model':model})
    #return HttpResponse("You're looking at model %s." % model_id)

def graph(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    return render(request, 'modeldb/graph.html',{'model':'model'})
    
def evolution(request):
    # create link dictionary
    d = [{"source":r.source.name,"target":r.target.name,"type":"connection"} for r in ModelRelation.objects.all()]  
    link_data = simplejson.dumps(d)
    return render(request, 'modeldb/evolution.html',{"link_data": link_data}, context_instance=RequestContext(request)) 

@csrf_exempt
def edit(request):
    #fid = open('/project/infinitebrain/sitelog.temp','w')
    #fid.write('editing model...')
    id = request.POST['id']
    #fid.write('#' + id + '\n')
    value = request.POST['value']
    field = request.POST['field']
    #fid.write('retrieving model...')
    model = get_object_or_404(Model, pk=id)
    #fid.write('done\n')
    #fid.close()
    if field=='notes':
        model.notes = value
    elif field=='name':
        model.name = value
    model.save()
    return HttpResponse(value)
    #return redirect('/dashboard/')

@csrf_exempt    
def delete(request):
    id=request.POST['id']
    model = get_object_or_404(Model, pk=id)
    model.delete()
    # delete associated files and other objects (ModelRelation, Files...)
    # TODO: make model function that deletes all associated objects and files then itself    
    #return HttpResponse(value)
    return HttpResponseRedirect('/dashboard/')
    #return redirect('/dashboard/')
    #models = Model.objects.filter(user=request.user).order_by('-date_added')
    #links = ModelRelation.objects.filter(Q(target__user=request.user) | Q(source__user=request.user))
    #d = [{"source":r.source.name,"target":r.target.name,"type":"connection"} for r in links]
    #link_data = simplejson.dumps(d)
    #return render(request, 'site/dashboard.html',{'models': models, "link_data": link_data},context_instance=RequestContext(request))

