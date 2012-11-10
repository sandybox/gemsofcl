# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.active'
        db.add_column('craigslist_item', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Item.num_views'
        db.add_column('craigslist_item', 'num_views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Item.num_likes'
        db.add_column('craigslist_item', 'num_likes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Item.num_dislikes'
        db.add_column('craigslist_item', 'num_dislikes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.active'
        db.delete_column('craigslist_item', 'active')

        # Deleting field 'Item.num_views'
        db.delete_column('craigslist_item', 'num_views')

        # Deleting field 'Item.num_likes'
        db.delete_column('craigslist_item', 'num_likes')

        # Deleting field 'Item.num_dislikes'
        db.delete_column('craigslist_item', 'num_dislikes')


    models = {
        'craigslist.item': {
            'Meta': {'object_name': 'Item'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_dislikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'craigslist.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['craigslist.Item']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['craigslist']