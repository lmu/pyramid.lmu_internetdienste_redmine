# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'docs', 'CHANGES.rst')) as f:
    CHANGES = f.read()

# TODO separate requirements
requires = [
    'pyramid',
    'pyramid_chameleon',
    'waitress',
    'deform',
    'python-redmine',
    'zope.interface',
    # Development Packages
    'pyramid_debugtoolbar',
    'ipdb',
]

setup(name='pyramid.lmu_internetdienste_redmine',
      version='1.0',
      description='pyramid.lmu_internetdienste_redmine',
      long_description=README + '\n\n' + CHANGES,
      author='Alexander Loechel',
      author_email='Alexander.Loechel@lmu.de',
      url='https://github.com/loechel/pyramid.lmu_internetdienste_redmine',
      license="GPL",
      keywords='web pyramid pylons',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['pyramid'],
      include_package_data=True,
      install_requires=requires,
      tests_require=requires,
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      #test_suite="pyramid.lmu_internetdienste_redmine",
      entry_points="""\
      [paste.app_factory]
      main = pyramid.lmu_internetdienste_redmine:main
      """,
      )
