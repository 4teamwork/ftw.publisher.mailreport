from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from ftw.publisher.mailreport.interfaces import IReportNotifier
from zope.component import getAdapter


class TriggerNotification(BrowserView):
    """This view triggers the notification.
    """

    def __call__(self):
        # get the notification adapter and call it
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return getAdapter(portal, IReportNotifier)()
