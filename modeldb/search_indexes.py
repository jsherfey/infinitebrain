import datetime
from haystack import indexes
from modeldb.models import Model, ModelSpec, ModelRelation
import datetime

class ModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    notes = indexes.CharField(model_attr='notes')
    date_added = indexes.DateTimeField(model_attr='date_added')
    user = indexes.CharField()
    privacy = indexes.CharField(model_attr='privacy')
    tags = indexes.CharField()

    def get_model(self):
        return Model

# following method taken from Haystack tutorial at:
# http://django-haystack.readthedocs.org/en/latest/tutorial.html#installation
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())

    def prepare_user(self, obj):
        return obj.user

    def prepare_tags(self, obj):
        return ' '.join(obj.tags.names())