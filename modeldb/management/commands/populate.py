from django.core.management.base import BaseCommand
from modeldb.models import Model, ModelSpec, ModelRelation
from django.contrib.auth.models import User

# Fields for Model are as follows:
'''
Model(models.Model)
    user = models.ForeignKey(User, blank=True, null=True, related_name='user_model')
    name=models.CharField(max_length=1000)
    level=models.CharField(max_length=10, default='network') # options: {mechanism, node, network}
    notes=models.CharField(max_length=10000, default='')
    privacy=models.CharField(max_length=10, default='unlisted') # options: {private, public, unlisted}
    rating = models.IntegerField(default=0) 
    d3file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='models',null=True)
    readmefile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='models',null=True)
    date_added =models.DateTimeField(default=datetime.now, null=True)
    tags = TaggableManager()
    votes = VotesField()
    objects = models.Manager() # Add objects before all other managers to avoid issues mention in http://stackoverflow.com/a/4455374/1462141
    objects_with_scores = ObjectsWithScoresManager() #For just a list of objects that are not ordered that can be customized.
    sort_by_score
'''

user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
user.save()
class Command(BaseCommand):
    args = ''
    help = ''

    def _create_model(self):
        for i in range(10):
            model = Model(
                name='Johns model',
                level='network',
                notes='john',
                privacy='public',
                user = User.objects.get(username='john'),
                )
            model.save()

    # def _create_user(self):
    #     model = User('john', 'lennon@thebeatles.com', 'johnpassword');
    #     model.save()
    #     model = User('jimmy', 'carter@thebeatles.com', 'johnpassword');
    #     model.save()

    def handle(self, *args, **kwargs):
        # self._create_user()
        self._create_model()