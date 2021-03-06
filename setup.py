from setuptools import setup, find_packages
import os

version = '2.0b1.dev0'
maintainer = 'Jonas Baumann'

tests_require = [
    'pyquery',
    'mocker',
    'unittest2',
    'ftw.testing',
    'zope.configuration',
    'plone.testing',
    'plone.app.testing',
    ]


setup(name='ftw.publisher.mailreport',
      version=version,
      description='An ftw.publisher addon for sending scheduled '
      'publishing report mails.',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw publisher mail report scheduled',
      author='4teamwork AG',
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

        'zope.annotation',
        'zope.app.component',
        'zope.component',

        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',

        'ZODB3',
        'Zope2',

        'plone.fieldsets',
        'plone.app.layout',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFPlone',
        'Plone',

        'ftw.publisher.core',
        'ftw.publisher.sender',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
