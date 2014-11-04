from django import forms
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class UserSearchForm(SearchForm):

    def search(self):
        sqs = super(UserSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()
        return sqs