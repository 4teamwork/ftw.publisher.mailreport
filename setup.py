from setuptools import setup, find_packages
import os

version = open('ftw/publisher/mailreport/version.txt').read().strip()
maintainer = 'Jonas Baumann'

tests_require = [
    'collective.testcaselayer',
    ]


setup(name='ftw.publisher.mailreport',
      version=version,
      description="Sends scheduled status report mails (for ftw.publisher)" +\
          ' (Maintainer: %s)' % maintainer,
      long_description=open("README.txt").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='ftw.publisher mail report scheduled',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='http://psc.4teamwork.ch/4teamwork/ftw/ftw-publisher-mailreport',
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
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
