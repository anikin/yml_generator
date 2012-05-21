from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, pre_delete, m2m_changed

from lemon import extradmin
from yml_generator.admin import OfferInline, CategoryInline
from yml_generator.models import Offer, Category
from yml_generator.options import ModelYMLItem


class AlreadyRegistered(Exception):

    pass


class NotRegistered(Exception):

    pass


class OfferSite(object):

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, model_yml_generator_class=None, **options):
        if not model_yml_generator_class:
            model_yml_generator_class = ModelYMLItem

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered(
                    u'The model %s already registered' % model.__name__)

            admin_object = extradmin.site._registry.get(model)
            if admin_object:
                inline_instance = OfferInline(model, extradmin.site)
                admin_object.inline_instances = \
                    admin_object.inline_instances + [inline_instance]
                if isinstance(admin_object.tabs, (list, tuple)):
                    tab = {'title': inline_instance.verbose_name_plural,
                           'contents': [inline_instance]}
                    admin_object.tabs = admin_object.tabs + [tab]

            if options:
                options['__module__'] = __name__
                model_yml_generator_class = type(
                    '%sYMLGenerator' % model.__name__,
                    (model_yml_generator_class,), options)
            model_yml_generator = model_yml_generator_class()
            self._registry[model] = model_yml_generator

            pre_delete.connect(self.delete_offer, sender=model)
            post_save.connect(self.check_offer_url_path, sender=model)

            sites_field_class = model_yml_generator.sites_field_class(model)
            if sites_field_class is ManyToManyField:
                through_model = getattr(
                    model, model_yml_generator.sites_field_name).through
                m2m_changed.connect(
                    self.check_offer_sites, sender=through_model)
            else:
                post_save.connect(self.check_offer_site, sender=model)

    def delete_offer(self, sender, **kwargs):
        Offer.objects.filter_by_content_object(kwargs['instance']).delete()

    def check_offer_url_path(self, sender, **kwargs):
        instance = kwargs['instance']
        model_yml_generator = self._registry.get(sender)
        if model_yml_generator:
            try:
                yml_generator = Offer.objects.get_for_content_object(instance)
            except Offer.DoesNotExist:
                pass
            else:
                yml_generator.update_url_path()

    def check_offer_site(self, sender, **kwargs):
        instance = kwargs['instance']
        model_yml_generator = self._registry.get(sender)
        if model_yml_generator:
            try:
                yml_generator = Offer.objects.get_for_content_object(instance)
            except Offer.DoesNotExist:
                pass
            else:
                yml_generator.update_sites()

    def check_offer_sites(self, sender, **kwargs):
        instance = kwargs['instance']
        action = kwargs['action']
        model_yml_generator = self._registry.get(instance.__class__)
        if model_yml_generators and action in ('post_add', 'post_remove', 'post_clear'):
            try:
                yml_generator = Offer.objects.get_for_content_object(instance)
            except Offer.DoesNotExist:
                pass
            else:
                yml_generator.update_sites()

class CategorySite(object):

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, model_yml_generator_class=None, **options):
        if not model_yml_generator_class:
            model_yml_generator_class = ModelYMLItem

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered(
                    u'The model %s already registered' % model.__name__)

            admin_object = extradmin.site._registry.get(model)
            if admin_object:
                inline_instance = CategoryInline(model, extradmin.site)
                admin_object.inline_instances = \
                    admin_object.inline_instances + [inline_instance]
                if isinstance(admin_object.tabs, (list, tuple)):
                    tab = {'title': inline_instance.verbose_name_plural,
                           'contents': [inline_instance]}
                    admin_object.tabs = admin_object.tabs + [tab]

            if options:
                options['__module__'] = __name__
                model_yml_generator_class = type(
                    '%sYMLGenerator category' % model.__name__,
                    (model_yml_generator_class,), options)
            model_yml_generator = model_yml_generator_class()
            self._registry[model] = model_yml_generator

            pre_delete.connect(self.delete_category, sender=model)
            post_save.connect(self.check_category_url_path, sender=model)

            sites_field_class = model_yml_generator.sites_field_class(model)
            if sites_field_class is ManyToManyField:
                through_model = getattr(
                    model, model_yml_generator.sites_field_name).through
                m2m_changed.connect(
                    self.check_category_sites, sender=through_model)
            else:
                post_save.connect(self.check_category_site, sender=model)

    def delete_category(self, sender, **kwargs):
        Offer.objects.filter_by_content_object(kwargs['instance']).delete()

    def check_category_url_path(self, sender, **kwargs):
        instance = kwargs['instance']
        model_yml_generator = self._registry.get(sender)
        if model_yml_generator:
            try:
                yml_generator = Category.objects.get_for_content_object(instance)
            except Category.DoesNotExist:
                pass
            else:
                yml_generator.update_url_path()

    def check_category_site(self, sender, **kwargs):
        instance = kwargs['instance']
        model_yml_generator = self._registry.get(sender)
        if model_yml_generator:
            try:
                yml_generator = Category.objects.get_for_content_object(instance)
            except Category.DoesNotExist:
                pass
            else:
                yml_generator.update_sites()

    def check_category_sites(self, sender, **kwargs):
        instance = kwargs['instance']
        action = kwargs['action']
        model_yml_generator = self._registry.get(instance.__class__)
        if model_yml_generator and action in ('post_add', 'post_remove', 'post_clear'):
            try:
                yml_generator = Category.objects.get_for_content_object(instance)
            except Category.DoesNotExist:
                pass
            else:
                yml_generator.update_sites()


offer = OfferSite()
category = CategorySite()