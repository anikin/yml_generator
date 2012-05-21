from django.shortcuts import render
from yml_generator.models import Shop, Category, Offer
from datetime import datetime


def market_xml(request):

    shop = Shop.objects.filter(site=request.site)
    try:
        shop = shop[0]
    except:
        shop = None
    categories = Category.objects.filter(enabled=True)
    offers = Offer.objects.filter(enabled=True)
    date = datetime.now()
    return render(request, 'yml_generator/market.xml',
                  {'shop': shop,
                   'categories': categories,
                   'offers': offers,
                   'date': date}, content_type='application/xml')
