# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Shop'
        db.create_table('yml_generator_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='shop settings', unique=True, to=orm['sites.Site'])),
        ))
        db.send_create_signal('yml_generator', ['Shop'])

        # Adding model 'Currenciy'
        db.create_table('yml_generator_currenciy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['yml_generator.Shop'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('rate', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('yml_generator', ['Currenciy'])

        # Adding model 'Category'
        db.create_table('yml_generator_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('yml_generator', ['Category'])

        # Adding M2M table for field sites on 'Category'
        db.create_table('yml_generator_category_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['yml_generator.category'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('yml_generator_category_sites', ['category_id', 'site_id'])

        # Adding model 'Offer'
        db.create_table('yml_generator_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('store', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pickup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivery', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('local_delivery_cost', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('typeprefix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('vendorcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sales_notes', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('manufacturer_warrant', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country_of_origin', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('barcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('yml_generator', ['Offer'])

        # Adding M2M table for field sites on 'Offer'
        db.create_table('yml_generator_offer_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['yml_generator.offer'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('yml_generator_offer_sites', ['offer_id', 'site_id'])


    def backwards(self, orm):
        
        # Deleting model 'Shop'
        db.delete_table('yml_generator_shop')

        # Deleting model 'Currenciy'
        db.delete_table('yml_generator_currenciy')

        # Deleting model 'Category'
        db.delete_table('yml_generator_category')

        # Removing M2M table for field sites on 'Category'
        db.delete_table('yml_generator_category_sites')

        # Deleting model 'Offer'
        db.delete_table('yml_generator_offer')

        # Removing M2M table for field sites on 'Offer'
        db.delete_table('yml_generator_offer_sites')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'yml_generator.category': {
            'Meta': {'object_name': 'Category'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'yml_category'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'yml_generator.currenciy': {
            'Meta': {'object_name': 'Currenciy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'rate': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['yml_generator.Shop']"})
        },
        'yml_generator.offer': {
            'Meta': {'object_name': 'Offer'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'country_of_origin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'delivery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_delivery_cost': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'manufacturer_warrant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'pickup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sales_notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'yml_offer'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'store': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'typeprefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vendorcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'yml_generator.shop': {
            'Meta': {'object_name': 'Shop'},
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'shop settings'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['yml_generator']
