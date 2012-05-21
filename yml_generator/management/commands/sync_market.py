# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand

import yml_generator
from yml_generator.models import Offer, Category


class Command(NoArgsCommand):

    help = 'Sync market.xml with all registered models'

    def handle_noargs(self, **options):
        print 'Starting market.xml synchronization with all registered Offer models.'
        yml_generator.autodiscover()
        for model, offer in yml_generator.offer._registry.items():
            print 'Syncing %s.%s model.' % (model._meta.app_label, model.__name__)
            self.sync_market_offer(model, offer)
        print 'All objects with `get_absolute_url` method was synced.',
        print 'Starting market.xml synchronization with all registered Category models.'
        for model, category in yml_generator.category._registry.items():
            print 'Syncing %s.%s model.' % (model._meta.app_label, model.__name__)
            self.sync_market_category(model, sitemap)
        print 'All objects with `get_absolute_url` method was synced.',
        print 'Removing orphaned sitemap.xml items.'
        self.remove_orphaned()
        print 'Done.'

    def sync_market_offer(self, model, sitemap):
        for obj in model.objects.all():
            try:
                item = Offer.objects.get_for_content_object(obj)
            except Item.DoesNotExist:
                if sitemap.url_path(obj):
                    item = Offer(content_object=obj)
                    item.save()
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  market.xml item for %s (%s) was created.' % (item.url_path, sites)
            else:
                item.update_url_path()
                item.update_sites()
                sites = ', '.join([s.domain for s in item.sites.all()])
                print '  market.xml offer item for %s (%s) was updated.' % (item.url_path, sites)

    def sync_market_category(self, model, sitemap):
        for obj in model.objects.all():
            try:
                item = Category.objects.get_for_content_object(obj)
            except Item.DoesNotExist:
                if sitemap.url_path(obj):
                    item = Category(content_object=obj)
                    item.save()
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  market.xml category item for %s (%s) was created.' % (item.url_path, sites)
            else:
                item.update_url_path()
                item.update_sites()
                sites = ', '.join([s.domain for s in item.sites.all()])
                print '  market.xml category item for %s (%s) was updated.' % (item.url_path, sites)

    def remove_orphaned_offer(self):
        for item in Offer.objects.all():
            if item.content_type and item.object_id:
                if not item.content_object:
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  market.xml offer item for %s (%s) deleted.' % (item.url_path, sites)
                    item.delete()

    def remove_orphaned_category(self):
        for item in Category.objects.all():
            if item.content_type and item.object_id:
                if not item.content_object:
                    sites = ', '.join([s.domain for s in item.sites.all()])
                    print '  market.xml category item for %s (%s) deleted.' % (item.url_path, sites)
                    item.delete()
