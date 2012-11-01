import unittest
import doctest
from Testing import ZopeTestCase as ztc
from ftw.publisher.mailreport.tests.base import MailreportBasicTestCase

OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)


def test_suite():
    return unittest.TestSuite([
            # doctests in file bar.txt
            ztc.ZopeDocFileSuite(
                'mailing.txt', package='ftw.publisher.mailreport.tests',
                test_class=MailreportBasicTestCase, optionflags=OPTIONFLAGS),
            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
