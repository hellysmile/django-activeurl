# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SimplePage'
        db.create_table('simplepage_simplepage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('simplepage', ['SimplePage'])


    def backwards(self, orm):
        # Deleting model 'SimplePage'
        db.delete_table('simplepage_simplepage')


    models = {
        'simplepage.simplepage': {
            'Meta': {'object_name': 'SimplePage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['simplepage']