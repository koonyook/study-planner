# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Institution'
        db.create_table('core_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['Institution'])

        # Adding model 'Course'
        db.create_table('core_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('units_limit_in_first_semester', self.gf('django.db.models.fields.IntegerField')()),
            ('units_limit_in_second_semester', self.gf('django.db.models.fields.IntegerField')()),
            ('units_limit_in_summer_semester', self.gf('django.db.models.fields.IntegerField')()),
            ('required_free_subject_units', self.gf('django.db.models.fields.IntegerField')()),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Institution'])),
        ))
        db.send_create_signal('core', ['Course'])

        # Adding M2M table for field required_subjects on 'Course'
        db.create_table('core_course_required_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['core.course'], null=False)),
            ('subject', models.ForeignKey(orm['core.subject'], null=False))
        ))
        db.create_unique('core_course_required_subjects', ['course_id', 'subject_id'])

        # Adding M2M table for field required_groups on 'Course'
        db.create_table('core_course_required_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['core.course'], null=False)),
            ('group', models.ForeignKey(orm['core.group'], null=False))
        ))
        db.create_unique('core_course_required_groups', ['course_id', 'group_id'])

        # Adding model 'Subject'
        db.create_table('core_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('units', self.gf('django.db.models.fields.IntegerField')()),
            ('available_in_first_semester', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('available_in_second_semester', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('available_in_summer_semester', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('years_available', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Institution'])),
        ))
        db.send_create_signal('core', ['Subject'])

        # Adding M2M table for field prerequisites on 'Subject'
        db.create_table('core_subject_prerequisites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_subject', models.ForeignKey(orm['core.subject'], null=False)),
            ('to_subject', models.ForeignKey(orm['core.subject'], null=False))
        ))
        db.create_unique('core_subject_prerequisites', ['from_subject_id', 'to_subject_id'])

        # Adding model 'Group'
        db.create_table('core_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('required_units', self.gf('django.db.models.fields.IntegerField')()),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Institution'])),
        ))
        db.send_create_signal('core', ['Group'])

        # Adding M2M table for field subjects on 'Group'
        db.create_table('core_group_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['core.group'], null=False)),
            ('subject', models.ForeignKey(orm['core.subject'], null=False))
        ))
        db.create_unique('core_group_subjects', ['group_id', 'subject_id'])

        # Adding model 'Field'
        db.create_table('core_field', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Institution'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Course'])),
        ))
        db.send_create_signal('core', ['Field'])

        # Adding M2M table for field subjects on 'Field'
        db.create_table('core_field_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('field', models.ForeignKey(orm['core.field'], null=False)),
            ('subject', models.ForeignKey(orm['core.subject'], null=False))
        ))
        db.create_unique('core_field_subjects', ['field_id', 'subject_id'])


    def backwards(self, orm):
        
        # Deleting model 'Institution'
        db.delete_table('core_institution')

        # Deleting model 'Course'
        db.delete_table('core_course')

        # Removing M2M table for field required_subjects on 'Course'
        db.delete_table('core_course_required_subjects')

        # Removing M2M table for field required_groups on 'Course'
        db.delete_table('core_course_required_groups')

        # Deleting model 'Subject'
        db.delete_table('core_subject')

        # Removing M2M table for field prerequisites on 'Subject'
        db.delete_table('core_subject_prerequisites')

        # Deleting model 'Group'
        db.delete_table('core_group')

        # Removing M2M table for field subjects on 'Group'
        db.delete_table('core_group_subjects')

        # Deleting model 'Field'
        db.delete_table('core_field')

        # Removing M2M table for field subjects on 'Field'
        db.delete_table('core_field_subjects')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'required_by'", 'symmetrical': 'False', 'to': "orm['core.Subject']"}),
            'units': ('django.db.models.fields.IntegerField', [], {}),
            'years_available': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['core']
