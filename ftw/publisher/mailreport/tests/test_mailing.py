from Products.CMFCore.utils import getToolByName
from ftw.publisher.core.states import ObjectUpdatedState
from ftw.publisher.core.states import UIDPathMismatchError
from ftw.publisher.mailreport import utils
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.testing import MAILREPORT_FUNCTIONAL_TESTING
from ftw.publisher.sender.interfaces import IQueue
from ftw.publisher.sender.persistence import Job
from ftw.publisher.sender.persistence import Realm
from ftw.testing import MockTestCase
from mocker import ARGS, KWARGS
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from pyquery import PyQuery as pq
import datetime
import re


class TestEmailNotification(MockTestCase):

    layer = MAILREPORT_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEmailNotification, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.folder = self.portal.get(self.portal.invokeFactory(
                'Folder', 'mailing-test', title='Mailing Test Folder'))
        self.queue = IQueue(self.portal)
        self.realm = Realm(True, 'http://localhost:0/', 'pub_user', 'pw')

        mtool = getToolByName(self.portal, 'portal_membership')
        self.user = mtool.getMemberById(TEST_USER_ID)

        # Enable notifier
        self.notifier_config = INotifierConfigurationSchema(self.portal)
        self.notifier_config.set_enabled(True)
        self.notifier_config.set_detailed_report(True)
        self.notifier_config.set_receivers_plain('demo@user.com')
        self.notifier_config.set_interval('hourly')

        # configure mail settings
        properties_tool = getToolByName(self.portal, 'portal_properties')
        properties_tool.email_from_name = 'Plone'
        properties_tool.email_from_address = 'test@plone.org'

        # patch MailHost
        self.mail_host = self.stub()
        self.mock_tool(self.mail_host, 'MailHost')
        self.mails = []
        self.expect(self.mail_host.send(ARGS, KWARGS)).call(
            lambda *args, **kwargs: self.mails.append((args, kwargs)))
        self.expect(self.mail_host.secureSend(ARGS, KWARGS)).call(
            lambda *args, **kwargs: self.mails.append((args, kwargs)))

        # mock datetime.now
        self.now = datetime.datetime(2010, 1, 2, 3, 4, 5)

        self._ori_datetime = datetime.datetime
        dt = self.mocker.proxy(datetime.datetime, count=False)
        self.expect(dt.now()).call(lambda: self.now).count(0, None)
        datetime.datetime = dt

        self.replay()

    def tearDown(self):
        datetime.datetime = self._ori_datetime
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        super(TestEmailNotification, self).tearDown()

    def suppose_job_was_executed(self, successful=True):
        """ Adds a job to the "executed" list
        """

        if successful:
            response = ObjectUpdatedState()
        else:
            response = UIDPathMismatchError()

        job = Job('push', self.folder, self.user)
        job.executed_with_states({
                'date': datetime.datetime.now(),
                self.realm: response})
        self.queue.append_executed_job(job)
        return job

    def set_time(self, hour, minute=None):
        if minute is None:
            minute = hour
        self.now = datetime.datetime(2010, 12, 27, hour, minute)

    def get_normalize_statistics_table_from_message(self, message):
        message = pq(str(message))
        statistics_table = message('table:first').html()
        # "normalize" whitspace
        statistics_table = re.sub('\s{1,}', ' ', statistics_table)
        statistics_table = statistics_table.replace('> <', '><')
        return statistics_table

    def test_report_sent_after_executing_queue(self):
        self.set_time(1)
        utils.set_last_notification_date_to_now()

        self.set_time(2)
        self.suppose_job_was_executed(successful=True)
        self.suppose_job_was_executed(successful=True)
        self.suppose_job_was_executed(successful=False)

        self.set_time(3)
        self.assertTrue(utils.is_interval_expired())

        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 1)
        args, kwargs = self.mails.pop()

        self.assertEqual(kwargs.get('mfrom'), 'test@plone.org')
        self.assertEqual(kwargs.get('mto'), 'demo@user.com')
        self.assertEqual(kwargs.get('subject'),
                         u'Publisher report: Plone site')

        statistics_table = self.get_normalize_statistics_table_from_message(
            args[0])

        self.assertIn('<tr><th>Successfull jobs:</th><td>2</td></tr>',
                      statistics_table)

        self.assertIn('<tr><th>Jobs with errors:</th><td>1</td></tr>',
                      statistics_table)

        self.assertIn('<tr><th>Total executed jobs:</th><td>3</td></tr>',
                      statistics_table)

    def test_report_does_only_contain_new_jobs(self):
        self.set_time(1)
        self.suppose_job_was_executed(successful=True)
        self.suppose_job_was_executed(successful=True)

        self.set_time(2)
        utils.set_last_notification_date_to_now()

        self.set_time(3)
        self.suppose_job_was_executed(successful=True)

        self.set_time(4)
        self.assertTrue(utils.is_interval_expired())
        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 1)
        args, kwargs = self.mails.pop()

        statistics_table = self.get_normalize_statistics_table_from_message(
            args[0])

        self.assertIn('<tr><th>Total executed jobs:</th><td>1</td></tr>',
                      statistics_table)

    def test_report_is_sent_to_each_receivers(self):
        self.notifier_config.set_receivers_plain('\n'.join((
                    'demo@user.com',
                    'hugo@boss.com')))

        self.set_time(1)
        self.suppose_job_was_executed(successful=True)

        self.set_time(2)
        utils.set_last_notification_date_to_now()

        self.set_time(3)
        self.assertTrue(utils.is_interval_expired())
        self.portal.restrictedTraverse('@@publisher.executeQueue')()

        self.assertEqual(len(self.mails), 2)

        # we pop it reversed, therfore we test in opposite order than
        # it is configured.
        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'hugo@boss.com')

        args, kwargs = self.mails.pop()
        self.assertEqual(kwargs.get('mto'), 'demo@user.com')
