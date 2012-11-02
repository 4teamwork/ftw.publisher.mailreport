from setuptools import setup, find_packages
import os

version = '2.0b1.dev0'
maintainer = 'Jonas Baumann'

tests_require = [
    'collective.testcaselayer',
    'Products.PloneTestCase',
    'plone.app.testing',
    'ftw.testing',
    'pyquery',
    ]


setup(name='ftw.publisher.mailreport',
      version=version,
      description='An ftw.publisher addon for sending scheduled '
      'publishing report mails.',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw publisher mail report scheduled',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.publisher.mailreport',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.publisher'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'z3c.autoinclude',
        'ftw.publisher.sender',
        'plone.fieldsets',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
