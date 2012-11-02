from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.testing import MAILREPORT_FUNCTIONAL_TESTING
from ftw.testing import MockTestCase
from zope.component import getGlobalSiteManager
from zope.component import provideAdapter


class TestNotificationView(MockTestCase):

    layer = MAILREPORT_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestNotificationView, self).setUp()
        self.portal = self.layer['portal']

        self.notifier_class = self.stub_interface(IReportNotifier)
        self.notifier = self.mock_interface(IReportNotifier)
        self.expect(self.notifier_class(self.portal)).result(self.notifier)

        provideAdapter(factory=self.notifier_class,
                       provides=IReportNotifier,
                       adapts=(IPloneSiteRoot,))

    def tearDown(self):
        sm = getGlobalSiteManager()
        sm.unregisterAdapter(factory=self.notifier_class,
                             provided=IReportNotifier,
                             required=(IPloneSiteRoot,))
        super(TestNotificationView, self).tearDown()

    def test_trigger_notification_view_calls_report_notifier(self):
        self.expect(self.notifier())
        self.replay()

        self.portal.unrestrictedTraverse(
            '@@publisher-notification-trigger-notification')()
