# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Citation'
        db.create_table(u'modeldb_citation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['modeldb.Model'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('citation', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('about', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'modeldb', ['Citation'])

        # Adding model 'Project'
        db.create_table(u'modeldb_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'modeldb', ['Project'])

        # Adding field 'Model.project'
        db.add_column(u'modeldb_model', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_model', null=True, to=orm['modeldb.Project']),
                      keep_default=False)

        # Adding field 'Model.ispublished'
        db.add_column(u'modeldb_model', 'ispublished',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Citation'
        db.delete_table(u'modeldb_citation')

        # Deleting model 'Project'
        db.delete_table(u'modeldb_project')

        # Deleting field 'Model.project'
        db.delete_column(u'modeldb_model', 'project_id')

        # Deleting field 'Model.ispublished'
        db.delete_column(u'modeldb_model', 'ispublished')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'modeldb.citation': {
            'Meta': {'object_name': 'Citation'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'citation': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modeldb.Model']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'modeldb.model': {
            'Meta': {'object_name': 'Model'},
            'd3file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ispublished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'network'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'notes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10000'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'unlisted'", 'max_length': '10'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_model'", 'null': 'True', 'to': u"orm['modeldb.Project']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'readmefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_model'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'modeldb.modelrelation': {
            'Meta': {'object_name': 'ModelRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': u"orm['modeldb.Model']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target'", 'to': u"orm['modeldb.Model']"})
        },
        u'modeldb.modelspec': {
            'Meta': {'object_name': 'ModelSpec'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modeldb.Model']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'dsim-json'", 'max_length': '100'})
        },
        u'modeldb.modelvote': {
            'Meta': {'ordering': "('date',)", 'unique_together': "(('voter', 'object'),)", 'object_name': 'ModelVote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modeldb.Model']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'modeldb.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['modeldb']