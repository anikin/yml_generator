from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

#from django.conf.settings import YML_GENERATOR

from django.utils.translation import ugettext_lazy as _

from yml_generator.managers import ItemManager


CURRENCIES = (
    ('RUR', 'RUR'),
    ('RUB', 'RUB'),
    ('USD', 'USD'),
    ('BYR', 'BYR'),
    ('KZT', 'KZT'),
    ('EUR', 'EUR'),
    ('UAH', 'UAH'),
)


class Shop(models.Model):

    name = models.CharField(
        _(u'name'), max_length=20,
        help_text= _(u'Short name of shop, maximum 20 leters'))
    company = models.CharField(
        _(u'company'), max_length=255,
        help_text=_(u'Full name of the company that owns the store.'))
    platform = models.CharField(
        _(u'platform'), max_length=255, blank=True, null=True,
        help_text=_(u'Content Management System, which operates on the basis of the store (CMS)'))
    version = models.CharField(
        _(u'version'), max_length=255, blank=True, null=True,
        help_text=_(u'Version of CMS'))
    agency = models.CharField(
        _(u'agency'), max_length=255, blank=True, null=True,
        help_text=_(u'The name of the agency, which provides technical support online store'))
    email = models.CharField(_(u'email'), max_length=255, blank=True, null=True,
        help_text=_(u'Contact email of CMS developers or agencies carrying out technical support.'))

    site = models.OneToOneField(Site, related_name='shop settings')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'shop')
        verbose_name_plural = _(u'shop settings')




class Currenciy(models.Model):

    shop = models.ForeignKey(Shop, verbose_name=_(u'shop'))
    name = models.CharField(
        _(u'name'), max_length=3, unique=True, choices=CURRENCIES,
        help_text=_(u'Currency indifier'))
    rate = models.CharField(_(u'rate'), max_length=5)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'currency')
        verbose_name_plural = _(u'currencies')


class Category(models.Model):

    url_path = models.CharField(_('URL path'), max_length=255, db_index=True)
    enabled = models.BooleanField(
        _(u'enabled'), default=True,
        help_text=_(u'If not set, product will not be export to XML-file'))
    sites = models.ManyToManyField(
        Site, null=True, blank=True, related_name='yml_category', verbose_name=_(u'sites'))
    content_type = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = ItemManager()

    def __unicode__(self):
        return self.content_object.title

    class Meta:
        verbose_name = _(u'category')
        verbose_name_plural = _(u'Yandex.Market')

    def save(self, *args, **kwargs):
        self.update_url_path(commit=False)
        super(Category, self).save(*args, **kwargs)
        self.update_sites()

    def update_url_path(self, commit=True):
        obj = self.content_object
        if obj:
            from yml_generator import category
            model_yml_generator = category._registry.get(obj.__class__)
            url_path = model_yml_generator.url_path(obj)
            if url_path:
                self.url_path = url_path
                if commit:
                    super(Category, self).save(False, False)

    def update_sites(self):
        obj = self.content_object
        if obj:
            from yml_generator.sites import category
            model_yml_generator = category._registry.get(obj.__class__)
            sites = model_yml_generator.sites(obj)
            self.sites.clear()
            if sites:
                self.sites.add(*sites)



class Offer(models.Model):

    url_path = models.CharField(_('URL path'), max_length=255, db_index=True, blank=True)
    store = models.BooleanField(_(u'store'), default=False)
    pickup = models.BooleanField(_(u'pickup'), default=False)
    delivery = models.BooleanField(_(u'delivery'), default=False)
    local_delivery_cost = models.CharField(_(u'local_delivery_cost'),
                                           max_length=10, blank=True, null=True)
    typeprefix = models.CharField(_(u'typeprefix'), max_length=255, blank=True, null=True)
    vendor = models.CharField(_(u'vendor'), max_length=255, blank=True, null=True)
    vendorcode = models.CharField(_(u'vendorcode'), max_length=255, blank=True, null=True)
    sales_notes = models.CharField(_(u'sales_notes'), max_length=255, blank=True, null=True)
    manufacturer_warrant = models.CharField(_(u'manufacturer_warrant'), max_length=255, blank=True, null=True)
    country_of_origin = models.CharField(_(u'country_of_origin'), max_length=255, blank=True, null=True)
    barcode = models.CharField(_(u'barcode'), max_length=255, blank=True, null=True)
    enabled = models.BooleanField(
        _(u'enabled'), default=True,
        help_text=_(u'If not set, product will not be export to XML-file'))
    sites = models.ManyToManyField(
        Site, null=True, blank=True, related_name='yml_offer', verbose_name=_(u'sites'))
    content_type = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    objects = ItemManager()

    def __unicode__(self):
        return self.content_object.title

    class Meta:
        verbose_name = _(u'offer')
        verbose_name_plural = _(u'Yandex.Market Offers')

    def save(self, *args, **kwargs):
        self.update_url_path(commit=False)
        super(Offer, self).save(*args, **kwargs)
        self.update_sites()

    def update_url_path(self, commit=True):
        obj = self.content_object
        if obj:
            from yml_generator import offer
            model_yml_generator = offer._registry.get(obj.__class__)
            url_path = model_yml_generator.url_path(obj)
            if url_path:
                self.url_path = url_path
                if commit:
                    super(Offer, self).save(False, False)

    def update_sites(self):
        obj = self.content_object
        if obj:
            from yml_generator.sites import offer
            model_yml_generator = offer._registry.get(obj.__class__)
            sites = model_yml_generator.sites(obj)
            self.sites.clear()
            if sites:
                self.sites.add(*sites)

