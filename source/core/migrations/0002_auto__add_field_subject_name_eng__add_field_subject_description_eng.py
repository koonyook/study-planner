# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Subject.name_eng'
        db.add_column('core_subject', 'name_eng', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Subject.description_eng'
        db.add_column('core_subject', 'description_eng', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Subject.name_eng'
        db.delete_column('core_subject', 'name_eng')

        # Deleting field 'Subject.description_eng'
        db.delete_column('core_subject', 'description_eng')


    models = {
        'core.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'required_free_subject_units': ('django.db.models.fields.IntegerField', [], {}),
            'required_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Group']", 'symmetrical': 'False'}),
            'required_subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Subject']", 'symmetrical': 'False'}),
            'units_limit_in_first_semester': ('django.db.models.fields.IntegerField', [], {}),
            'units_limit_in_second_semester': ('django.db.models.fields.IntegerField', [], {}),
            'units_limit_in_summer_semester': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.field': {
            'Meta': {'object_name': 'Field'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Subject']", 'symmetrical': 'False'})
        },
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'required_units': ('django.db.models.fields.IntegerField', [], {}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Subject']", 'symmetrical': 'False'})
        },
        'core.institution': {
            'Meta': {'object_name': 'Institution'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.subject': {
            'Meta': {'object_name': 'Subject'},
            'available_in_first_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'available_in_second_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'available_in_summer_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_eng': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_eng': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'required_by'", 'symmetrical': 'False', 'to': "orm['core.Subject']"}),
            'units': ('django.db.models.fields.IntegerField', [], {}),
            'years_available': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['core']
