from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.publisher.mailreport.handlers import invoke_notification
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.testing import MAILREPORT_FUNCTIONAL_TESTING
from ftw.publisher.mailreport.utils import is_interval_expired
from ftw.publisher.mailreport.utils import set_last_notification_date_to_now
from ftw.publisher.sender.interfaces import IConfig
from ftw.testing import MockTestCase
from zope.component import getGlobalSiteManager
from zope.component import provideAdapter


class TestEventhandler(MockTestCase):

    layer = MAILREPORT_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEventhandler, self).setUp()
        self.portal = self.layer['portal']

        notifier_config = INotifierConfigurationSchema(self.portal)
        notifier_config.set_enabled(True)

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
        super(TestEventhandler, self).tearDown()

    def test_eventhandler_calls_notifier(self):
        self.expect(self.notifier())
        self.replay()

        invoke_notification(self.portal, None)

    def test_adapter_called_after_queue_execution(self):
        self.expect(self.notifier())
        self.replay()

        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()

    def test_adapter_not_called_when_inverval_not_expired(self):
        self.expect(self.notifier()).count(0)
        self.replay()

        set_last_notification_date_to_now()
        self.assertFalse(is_interval_expired())
        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()

    def test_adapter_not_called_when_publishing_disabled(self):
        self.expect(self.notifier()).count(0)
        self.replay()

        config = IConfig(self.portal)
        config.set_publishing_enabled(False)
        self.portal.unrestrictedTraverse('@@publisher.executeQueue')()
