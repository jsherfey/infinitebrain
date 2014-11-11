from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from taggit.managers import TaggableManager
from qhonuskan_votes.models import VotesField, ObjectsWithScoresManager, SortByScoresManager

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Model(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, related_name='project_model')
    user = models.ForeignKey(User, blank=True, null=True, related_name='user_model')
    name=models.CharField(max_length=1000)
    level=models.CharField(max_length=10, default='network') # options: {mechanism, node, network}
    notes=models.CharField(max_length=10000, default='')
    privacy=models.CharField(max_length=10, default='unlisted') # options: {private, public, unlisted}
    ispublished=models.BooleanField(default=False); # attribute added to speed up third-party API queries
    rating = models.IntegerField(default=0) 
    d3file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='models',null=True)
    readmefile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='models',null=True)
    date_added =models.DateTimeField(default=datetime.now, null=True)
    tags = TaggableManager()
    votes = VotesField()
    objects = models.Manager() # Add objects before all other managers to avoid issues mention in http://stackoverflow.com/a/4455374/1462141
    objects_with_scores = ObjectsWithScoresManager() #For just a list of objects that are not ordered that can be customized.
    sort_by_score = SortByScoresManager() #For a objects ordered by score.
    def __unicode__(self):
        return self.name
    def was_added_recently(self):
        return self.date_added >= timezone.now() - timedelta(days=1)
    was_added_recently.admin_order_field = 'date_added'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'
    # def ispublished(self):
    #     ... Citation...
        
class ModelSpec(models.Model):
    model =models.ForeignKey(Model)
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='models')
    type = models.CharField(max_length=100,default='dsim-json') # options: {dsim, neuron, genesis, neuroml, cellml, sbml, etc}
    rating = models.IntegerField(default=0)
    date_added =models.DateTimeField(default=datetime.now, null=True)
    def __unicode__(self):
        return str(self.file)
    def was_added_recently(self):
        return self.date_added >= timezone.now() - timedelta(days=1)

class ModelRelation(models.Model):
    source=models.ForeignKey(Model,related_name='source')
    target=models.ForeignKey(Model,related_name='target')
    def __unicode__(self):
        return str(self.source) + ' -> ' + str(self.target)
 
class Citation(models.Model):
    model = models.ForeignKey(Model, related_name='model_citation') # cited model
    title = models.CharField(max_length=500) # this will appear in the model list
    citation = models.CharField(max_length=1000) # (e.g., formal or informal reference)
    about = models.CharField(max_length=5000) # (e.g., abstract, comments, description)
    url = models.CharField(max_length=500) # (e.g., pubmed, personal site)
    def __unicode__(self):
        return self.title
