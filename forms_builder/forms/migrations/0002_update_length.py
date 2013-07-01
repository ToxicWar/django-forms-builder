# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Field.slug'
        db.alter_column(u'forms_field', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=255))

        # Changing field 'Field.placeholder_text'
        db.alter_column(u'forms_field', 'placeholder_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Form.title'
        db.alter_column(u'forms_form', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Form.button_text'
        db.alter_column(u'forms_form', 'button_text', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Form.slug'
        db.alter_column(u'forms_form', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255))

    def backwards(self, orm):

        # Changing field 'Field.slug'
        db.alter_column(u'forms_field', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100))

        # Changing field 'Field.placeholder_text'
        db.alter_column(u'forms_field', 'placeholder_text', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Form.title'
        db.alter_column(u'forms_form', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Form.button_text'
        db.alter_column(u'forms_form', 'button_text', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Form.slug'
        db.alter_column(u'forms_form', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True))

    models = {
        u'content.site': {
            'Meta': {'object_name': 'Site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Site']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        u'forms.field': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Field'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['forms.Form']"}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'placeholder_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'forms.fieldentry': {
            'Meta': {'object_name': 'FieldEntry'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['forms.FormEntry']"}),
            'field_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        u'forms.form': {
            'Meta': {'object_name': 'Form'},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '100'}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[1]', 'to': u"orm['content.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'forms.formentry': {
            'Meta': {'object_name': 'FormEntry'},
            'entry_time': ('django.db.models.fields.DateTimeField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['forms.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['forms']