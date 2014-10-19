import datetime
from haystack import indexes
from modeldb.models import Model, ModelSpec, ModelRelation
import datetime

class ModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    notes = indexes.CharField(model_attr='notes')
    date_added = indexes.DateTimeField(model_attr='date_added')

    def get_model(self):
        return Model

# following method taken from Haystack tutorial at:
# http://django-haystack.readthedocs.org/en/latest/tutorial.html#installation
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())