from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.functional import curry, memoize


def load_provider(provider_name):
    module_name, attr = provider_name.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing modifier %s: "%s"' % (provider_name, e))
    try:
        provider = getattr(module, attr)
    except AttributeError, e:
        raise ImproperlyConfigured(
            'Error importing modifier %s: "%s"' % (provider_name, e))
    return provider


def get_class(setting_name):
    providers = []
    for provider_name in getattr(settings, setting_name, ()):
        providers.append(load_provider(provider_name))
    return providers


get_providers = memoize(
    func = curry(get_class, 'YML_GENERATOR_PROVIDERS'),
    cache = {},
    num_args = 0,
)