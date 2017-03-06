

__title__ = 'pygster_logparsers'
__version__ = '0.1'
__author__ = 'Serg Belyakov  <serg@itlbs.ru>'
__copyright__ = 'Copyright 2014 OnBeep, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


from distutils.core import setup

setup(
  name = __title__,
  packages = [__title__, ],
  version = __version__,
  description = 'Parsers for pygster https://pypi.python.org/pypi/pygster',
  author = 'Serg Belyakov',
  author_email = 'serg@itlbs.ru',
  url = 'https://github.com/serg-it/pygster-parsers',
  license=open('LICENSE').read(),
  install_requires=['pygster'],
  zip_safe=False,
)
