try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Cryptopals CTF',
    'author': 'Jeremy Fox',
    'url': 'github.com/cryptopals-py',
    'download_url': 'github.com/cryptopals-py',
    'author_email': 'foxjerem@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['crypt'],
    'scripts': [],
    'name': 'cryptopals-py'
}

setup(**config)
