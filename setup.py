try:
    from setuptools import setuptools
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'space_shooter_game',
    'author': 'Adam M Deeley',
    'url': 'https://github.com/ADeeley/pygames',
    'download_url': 'https://github.com/ADeeley/pygames',
    'author_email': 'ad.deeley@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pygame'],
    'scripts': [],
    'name': 'space_shooter_game'
}

setup(**config)