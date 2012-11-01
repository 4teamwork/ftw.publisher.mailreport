from ftw.publisher.mailreport import utils
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.testing import MAILREPORT_INTEGRATION_TESTING
from ftw.testing import MockTestCase
import datetime


class TestUtils(MockTestCase):

    layer = MAILREPORT_INTEGRATION_TESTING

    def setUp(self):
        super(TestUtils, self).setUp()

        self.now = datetime.datetime(2010, 1, 2, 3, 4, 5)

        self._ori_datetime = datetime.datetime
        dt = self.mocker.proxy(datetime.datetime, count=False)
        self.expect(dt.now()).call(lambda: self.now).count(0, None)
        datetime.datetime = dt

        self.mocker.replay()

        portal = self.layer['portal']
        self.config = INotifierConfigurationSchema(portal)

    def tearDown(self):
        datetime.datetime = self._ori_datetime
        super(TestUtils, self).tearDown()

    def test_default_values(self):
        import datetime
        self.assertEqual(utils.get_last_notification_date(), None)
        self.assertEqual(utils.is_interval_expired(), True)
        self.assertEqual(utils.get_interval_delta(), datetime.timedelta(1))

    def test_set_set_last_notification_date_to_now(self):
        self.assertEqual(utils.get_last_notification_date(), None)
        utils.set_last_notification_date_to_now()
        self.assertEqual(utils.get_last_notification_date(), self.now)

    def test_is_interval_expired__hourly(self):
        self.config.set_interval('hourly')

        self.assertEqual(utils.get_last_notification_date(), None)
        self.assertEqual(utils.is_interval_expired(), True)

        self.now = datetime.datetime(2010, 12, 27, 10, 00)
        utils.set_last_notification_date_to_now()
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 27, 10, 31)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 27, 11, 01)
        self.assertEqual(utils.is_interval_expired(), True)

    def test_is_interval_expired__daily(self):
        self.config.set_interval('daily')

        self.assertEqual(utils.get_last_notification_date(), None)
        self.assertEqual(utils.is_interval_expired(), True)

        self.now = datetime.datetime(2010, 12, 25, 01, 00)
        utils.set_last_notification_date_to_now()
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 25, 03, 00)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 26, 00, 30)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 26, 01, 01)
        self.assertEqual(utils.is_interval_expired(), True)

    def test_is_interval_expired__weekly(self):
        self.config.set_interval('weekly')

        self.assertEqual(utils.get_last_notification_date(), None)
        self.assertEqual(utils.is_interval_expired(), True)

        self.now = datetime.datetime(2010, 12, 10, 01, 00)
        utils.set_last_notification_date_to_now()
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 10, 03, 00)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 12, 01, 00)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 17, 00, 30)
        self.assertEqual(utils.is_interval_expired(), False)

        self.now = datetime.datetime(2010, 12, 17, 01, 01)
        self.assertEqual(utils.is_interval_expired(), True)
