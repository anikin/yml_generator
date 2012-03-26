from setuptools import setup, find_packages


setup(
    name = 'yml-generator',
    version = '0.1.dev',
    author = 'Anikin Sergey',
    author_email = 'anikin@trilan.ru',
    description = 'XML file generator for Yandex.Market',
    packages = find_packages(exclude=[
    	'test_project', 'test_project.*']),
    include_package_data=True,
    zip_safe = False,
)
