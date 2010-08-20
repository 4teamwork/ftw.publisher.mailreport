from ftw.publisher.mailreport.interfaces import IReportNotifier
from zope.interface import implements


class MailReportNotifier(object):
    """Default report notifier. Sends notification emails.
    """
    implements(IReportNotifier)

    def __call__(self):
        pass
