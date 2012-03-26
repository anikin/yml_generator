import django
from django.db import models


class BaseProvider():

    name = ''
    company = ''
    url = ''
    platform = 'Django'
    if platform == 'Django':
        version = ''
        ver = django.VERSION
        ver = ver[:3]
        for item in ver:
            version+=str(item)
    else:
        version = ''
    agency = 'Trilan'
    email = 'order@trilan.ru'


    def get_properties(self):
        props = {
            'name': self.name,
            'company': self.company,
            'url': self.url,
            'platform': self.platform,
            'version': self.version,
            'agency': self.agency,
            'email': self.email,
        }
        return props


    def get_currencies(self):
        return (
            ('RUR', 1),
        )

    
    def get_categories(self):
        return (
            ()
        )

    def get_ofers(self):
        return (
            ()
        )