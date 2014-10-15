from django.contrib import admin
from modeldb.models import Model, ModelSpec

# Register your models here.

class ModelSpecInline(admin.TabularInline):
    model = ModelSpec
    extra = 2

class ModelAdmin(admin.ModelAdmin):
#    # reorder field display order
#    fields = ['date_added', 'name']
    # split the form up into fieldsets and make one collapsable
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    inlines = [ModelSpecInline]
    list_display = ('name', 'date_added', 'was_added_recently')
    list_filter = ['date_added']
    search_fields = ['name']

admin.site.register(Model, ModelAdmin)

