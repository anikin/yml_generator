from django.conf.urls.defaults import patterns, url
from yml_generator.views import market_xml


urlpatterns = patterns('',
    url(r'^$', market_xml, name="market_xml"),
)