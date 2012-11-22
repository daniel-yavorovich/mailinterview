# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Poll.author_email'
        db.add_column('poll_poll', 'author_email',
                      self.gf('django.db.models.fields.EmailField')(default=None, max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Poll.author_email'
        db.delete_column('poll_poll', 'author_email')


    models = {
        'poll.client': {
            'Meta': {'object_name': 'Client'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'is_voted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'unique_id': ('poll.fields.UUIDField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'poll.poll': {
            'Meta': {'object_name': 'Poll'},
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['poll.Client']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'unique_id': ('poll.fields.UUIDField', [], {'max_length': '64', 'primary_key': 'True'}),
            'variants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['poll.Variant']", 'symmetrical': 'False'})
        },
        'poll.variant': {
            'Meta': {'object_name': 'Variant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'votes_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['poll']