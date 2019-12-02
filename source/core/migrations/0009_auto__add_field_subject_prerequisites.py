# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field prerequisites on 'Subject'
        db.create_table('core_subject_prerequisites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subject', models.ForeignKey(orm['core.subject'], null=False)),
            ('prerequisite', models.ForeignKey(orm['core.prerequisite'], null=False))
        ))
        db.create_unique('core_subject_prerequisites', ['subject_id', 'prerequisite_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field prerequisites on 'Subject'
        db.delete_table('core_subject_prerequisites')


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
        'core.prerequisite': {
            'Meta': {'object_name': 'Prerequisite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_parallelable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'required_by_prerequisites'", 'symmetrical': 'False', 'to': "orm['core.Subject']"})
        },
        'core.subject': {
            'Meta': {'object_name': 'Subject'},
            'available_in_first_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'available_in_second_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'available_in_summer_semester': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'required_by_subjects'", 'blank': 'True', 'to': "orm['core.Prerequisite']"}),
            'thai_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thai_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'units': ('django.db.models.fields.IntegerField', [], {}),
            'years_available': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['core']
