from yml_generator.provider import BaseProvider

class MyProvider(BaseProvider):

    name = 'My Shop'
    company = 'My Super Compaly'
    url = 'http://google.com'


    def get_currencies(self):
        return (
            ('RUR', 1),
            ('USD', 29.3),
            ('EUR', 40.62),
        )


    def get_categories(self):
        return (
            (1, None, 'Books'),
            (2, 1, 'Detectives'),
            (3, 1, 'Romans'),
            (4, 1, 'Faritails'),
            (1, None, 'DVD'),
        )
