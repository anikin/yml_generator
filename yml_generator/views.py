from django.shortcuts import render
from django.utils.functional import curry, memoize
from .loader import get_providers


def market_xml(request):

    providers = get_providers()
    for item in providers:
        provider = item()
        shop = provider.get_properties()
        currencies = provider.get_currencies()
        categories = provider.get_categories()
        return render(request, 'market/market.xml',
                      {'shop': shop,
                       'currencies': currencies,
                       'categories': categories,}, 
                      content_type='application/xml')
