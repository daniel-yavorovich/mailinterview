# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('poll_client', (
            ('unique_id', self.gf('poll.fields.UUIDField')(max_length=64, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('is_voted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('poll', ['Client'])

        # Adding model 'Variant'
        db.create_table('poll_variant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('votes_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('poll', ['Variant'])

        # Adding model 'Poll'
        db.create_table('poll_poll', (
            ('unique_id', self.gf('poll.fields.UUIDField')(max_length=64, primary_key=True)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Poll'])

        # Adding M2M table for field variants on 'Poll'
        db.create_table('poll_poll_variants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('variant', models.ForeignKey(orm['poll.variant'], null=False))
        ))
        db.create_unique('poll_poll_variants', ['poll_id', 'variant_id'])

        # Adding M2M table for field clients on 'Poll'
        db.create_table('poll_poll_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('client', models.ForeignKey(orm['poll.client'], null=False))
        ))
        db.create_unique('poll_poll_clients', ['poll_id', 'client_id'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('poll_client')

        # Deleting model 'Variant'
        db.delete_table('poll_variant')

        # Deleting model 'Poll'
        db.delete_table('poll_poll')

        # Removing M2M table for field variants on 'Poll'
        db.delete_table('poll_poll_variants')

        # Removing M2M table for field clients on 'Poll'
        db.delete_table('poll_poll_clients')


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