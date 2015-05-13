from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from modeldb.models import Model, ModelSpec, ModelRelation, Project, Citation
from django.utils import simplejson
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext #, loader
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
import os
#from django.views.decorators.csrf import ensure_csrf_cookie
#@ensure_csrf_cookie

# Create your views here.
def index(request):
    #models = Model.objects.order_by('-date_added')#[:5]
    models = Model.sort_by_score.all().filter(~Q(level='mechanism'), Q(privacy='public'))#.order_by('-date_added')
    context = {'models': models}
    return render(request, 'modeldb/index.html', context, context_instance=RequestContext(request))
    # Note: The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.
    #template = loader.get_template('modeldb/index.html')
    #context = RequestContext(request, {'latest_model_list': latest_model_list})
    #return HttpResponse(template.render(context))
    #return HttpResponse("Hello, world. You're at the model index.")

def detail(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    print model.readmefile
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
    model = Model.objects.filter(id=id)
    #model = get_object_or_404(Model, pk=id)
    model.delete()
    # delete associated files and other objects (ModelRelation, Files...)
    # TODO: make model function that deletes all associated objects and files then itself    
    return HttpResponse(200)
    # return HttpResponseRedirect('/dashboard/')
    #return redirect('/dashboard/')
    #models = Model.objects.filter(user=request.user).order_by('-date_added')
    #links = ModelRelation.objects.filter(Q(target__user=request.user) | Q(source__user=request.user))
    #d = [{"source":r.source.name,"target":r.target.name,"type":"connection"} for r in links]
    #link_data = simplejson.dumps(d)
    #return render(request, 'site/dashboard.html',{'models': models, "link_data": link_data},context_instance=RequestContext(request))

@login_required
def add_model(request):
    MEDIA_PATH = settings.MEDIA_ROOT
    # MEDIA_PATH = '/Users/michaelromano/practice/'

    def save_model(request, owner, project):
        modelname = request.POST['name']
        level = request.POST.get('level','network')
        notes = request.POST['notes']
        ispublished = request.POST.get('ispublished', False)
        privacy = request.POST.get('privacy','unlisted')
        tags = request.POST.getlist('tag[]', '')
        newtags = request.POST.get('newtags').replace(',',' ').split()
        model = Model(name=modelname,
            user=owner,
            project=project,
            level=level,
            ispublished=ispublished,
            privacy=privacy,
            )
        model.save()
        model.tags.add(*tags)
        model.tags.add(*newtags)
        model.readmefile=upload_readme(request, model)
        model.save()
        return model

    def upload_and_save_spec(request, model, filetype):
        USER_MEDIA = 'user/' + request.user.username + '/models/'
        filename = request.FILES['specfile']
        extension = filename.content_type.split('/')[1]
        rel_path = USER_MEDIA + 'model' + str(model.pk) + '_spec.' + extension
        with open(MEDIA_PATH+rel_path, 'wb') as writefile:
            for chunk in filename.chunks():
                writefile.write(chunk)
        m = ModelSpec(model=model, file=rel_path,type=filetype)
        m.save()

    def upload_readme(request, model):
        USER_MEDIA = 'user/' + request.user.username + '/models/'
        filename = request.FILES['readme']
        rel_path = USER_MEDIA + 'model' + str(model.pk) + '_readme.txt'
        with open(MEDIA_PATH+rel_path, 'wb') as writefile:
            for chunk in filename.chunks():
                writefile.write(chunk)
        return rel_path


    if request.method == 'GET':
        # Get all of the projects for the current user
        projects = Project.objects.filter(owner=request.user)
        tags = Tag.objects.all()[:5]
        return render(request, 'modeldb/add_model.html', {'projects': projects, 'tags': tags, 'size_exceeded': False})
    else:
        '''
        First, check the file size
        '''
        if request.FILES['specfile'].size > int(settings.MAX_UPLOAD_SIZE) or request.FILES['readme'].size > int(settings.MAX_UPLOAD_SIZE):
            projects = Project.objects.filter(owner=request.user)
            tags = Tag.objects.all()[:5]
            return render(request, 'modeldb/add_model.html', {'size_exceeded': True, 'projects': projects, 'tags': tags})

        owner = request.user;
        USER_MEDIA = 'user/' + owner.username + '/models/'
        if not os.path.isdir(MEDIA_PATH + USER_MEDIA):
            os.makedirs(MEDIA_PATH + USER_MEDIA)

        if (request.POST['project'] == 'newproject' and request.POST['projectname'] != ''):
            projectname = request.POST['projectname']
        else:
            projectname = request.POST['project']
        
        project, created = Project.objects.get_or_create(owner=owner,name=projectname)
        if created:
            project.save()

        '''
        Then add the model and tags to the project
        '''
        model = save_model(request, owner, project)
        upload_and_save_spec(request, model, request.POST.get('filetype', 'dnsim'))
        
        '''
        Now, handle citations
        '''
        if model.ispublished:
            citationtitle = request.POST['citationtitle']
            citationstring = request.POST['citationstring']
            citationurl = request.POST['citationurl']
            citationabout = request.POST['citationabout']
            c = Citation(model=model,title=citationtitle,citation=citationstring,url=citationurl,about=citationabout)
            c.save()

        return HttpResponseRedirect('/dashboard/')
