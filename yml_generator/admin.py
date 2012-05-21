from django import forms
from lemon import extradmin
from lemon.extradmin import generic
from lemon.extradmin.admin import SiteExtrAdmin

from yml_generator.models import Offer, Category, Shop


class ItemForm(forms.ModelForm):

    def has_changed(self):
        return True


class ShopInline(extradmin.StackedInline):

    model = Shop
    can_delete = False


class OfferInline(generic.GenericStackedInline):

    form = ItemForm
    model = Offer
    exclude = ('sites', 'url_path',)
    extra = 1
    max_num = 1


class CategoryInline(generic.GenericStackedInline):

    form = ItemForm
    model = Category
    exclude = ('sites', 'url_path',)
    extra = 1
    max_num = 1


extradmin.site.register(Offer)
extradmin.site.register(Category)
