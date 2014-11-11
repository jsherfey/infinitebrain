import os, json, shutil, sys
import os.path
os.environ['DJANGO_SETTINGS_MODULE']='infinitebrain.settings'

from modeldb.models import Model, ModelSpec, ModelRelation, Project, Citation
from django.contrib.auth.models import User
from django.utils import timezone

if len(sys.argv)>1: #and os.path.isfile(sys.argv[1]):
    tempfile=sys.argv[1]
else:
    print "no input given. nothing to do."
    sys.exit()

MEDIA_PATH = '/project/infinitebrain/media/'
inbox='/project/infinitebrain/inbox/'
jsonfile=inbox + tempfile
lockfile=jsonfile+'.locked'
#print "jsonfile: " + jsonfile
if not os.path.isfile(jsonfile):
    print "json specification not found. nothing to do."
    sys.exit()
elif os.path.isfile(lockfile):
    print "json specification locked. being processed elsewhere."
    sys.exit()
else:
    lock = open(lockfile, 'w+')
    lock.close()

try:
    json_data=open(jsonfile)
    data = json.load(json_data)
    json_data.close()
    
    print "extracting model info on server..."
    modelname = data['modelname']
    username = data['username']
    level = data['level']
    notes = data['notes']
    ispublished = data['ispublished']
    projectname = data['projectname']
    citationtitle = data['citationtitle']
    citationstring = data['citationstring']
    citationurl = data['citationurl']
    citationabout = data['citationabout']
    privacy = data['privacy']
    if not privacy:
        privacy = 'public'
    sources = data['source']
    if sources:
        sources=str(sources).replace('[','').replace(']','').split(',')
    
    # mat-file
    tempmatfile = jsonfile.replace('.json','') + '.mat'
    # d3 file
    tempd3file = inbox + data['d3file']
    # readme file
    if (level=='mechanism'):
        tempreadmefile = inbox + data['specfile']
    else:
        tempreadmefile = inbox + data['readmefile']
    tags = data['tags']
    tags = tags.replace(' ','').split(',')
    
    # get user
    u = User.objects.filter(username=username)[0]
    
    # Project
    if projectname:
        p = Project.objects.filter(name=projectname)
        if p:
            p=p[0]
        else:
            print "creating new database record for project..."
            p=Project(owner=u,name=projectname)
            p.save()
        print "creating new database record for model..."
        m = Model(user=u,project=p,name=modelname,level=level,notes=notes,privacy=privacy,ispublished=(ispublished=='1'),date_added=timezone.now()) # ,d3file=d3file,readmefile=readmefile
    else:
        print "creating new database record for model..."
        m = Model(user=u,name=modelname,level=level,notes=notes,privacy=privacy,ispublished=(ispublished=='1'),date_added=timezone.now()) # ,d3file=d3file,readmefile=readmefile
    m.save()
    m.tags.add(*tags)
    m.save()
    
    # Citation
    if ispublished=='1':
        print "creating new database record for citation..."
        c = Citation(model=m,title=citationtitle,citation=citationstring,url=citationurl,about=citationabout)
        c.save()
    
    # File handling
    USER_MEDIA = 'user/' + username + '/models/'
    if not os.path.isdir(MEDIA_PATH + USER_MEDIA):
         os.makedirs(MEDIA_PATH + USER_MEDIA)
    print "moving model to media archive..." #: " + MEDIA_PATH + USER_MEDIA
    if (level=='mechanism'):
        specfile = USER_MEDIA + 'model' + str(m.pk) + '_mech.txt'
        mechfile = inbox + data['specfile']
        if os.path.isfile(mechfile):
            shutil.copy2(mechfile,MEDIA_PATH+specfile)
            tempreadmefile = mechfile
    else:
        specfile = USER_MEDIA + 'model' + str(m.pk) + '_spec.json'
        shutil.copy2(jsonfile,MEDIA_PATH+specfile)
    os.remove(jsonfile)
    if os.path.isfile(tempd3file):
        m.d3file = USER_MEDIA + 'model' + str(m.pk) + '_d3.json'
        shutil.copy2(tempd3file,MEDIA_PATH+str(m.d3file))
        os.remove(tempd3file)
    if os.path.isfile(tempreadmefile):
        if (level=='mechanism'):
            m.readmefile = specfile # USER_MEDIA + 'model' + str(m.pk) + '_mech.txt'
        else:
            m.readmefile = USER_MEDIA + 'model' + str(m.pk) + '_readme.txt'
            shutil.copy2(tempreadmefile,MEDIA_PATH+str(m.readmefile))
            os.remove(tempreadmefile)
    m.save()
    if (level=='mechanism'):
        os.remove(mechfile)
    
    # Specification Files
    print "creating new database record for model specification..."
    # json/text file
    f=ModelSpec(model=m,file=specfile,date_added=timezone.now())
    f.save()
    # mat-file
    if os.path.isfile(tempmatfile):
        matfile = USER_MEDIA + 'model' + str(m.pk) + '_spec.mat'
        shutil.copy2(tempmatfile,MEDIA_PATH+matfile)
        os.remove(tempmatfile)
        f2=ModelSpec(model=m,file=matfile,type='dsim-MATLAB',date_added=timezone.now())
        f2.save()
    
    # Model Relations
    print "adding model relations based on parent_uids..."
    try:
        for source in sources:
            src=Model.objects.get(pk=source.strip())
            if src:
                rel=ModelRelation(source=src,target=m)
                rel.save()
                print rel
    except:
        print "no model relations added."
    
    print "success."
    os.remove(lockfile)
except:
    print "Unexpected error:", sys.exc_info()[0]
    os.remove(lockfile)
