from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.testing import MAILREPORT_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from unittest2 import TestCase
import os.path


class TestConfig(TestCase):

    layer = MAILREPORT_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestConfig, self).setUp()
        self.portal = self.layer['portal']
        self.app = self.layer['app']

        self.browser = Browser(self.app)
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        self.browser.handleErrors = False
        self.portal_url = self.portal.portal_url()

        self.config_url = os.path.join(self.portal_url,
                                       '@@publisher-notification-config')

    def test_link_is_in_controlpanel(self):
        self.browser.open('%s/@@publisher-config' % self.portal_url)

        link = self.browser.getLink('Notifier configuration')
        self.assertNotEqual(
            link, None,
            'Notifier configuration not found in control panel')

        link.click()
        self.assertEqual(self.browser.url, self.config_url,
                         'Notifier configuration link points to wrong URL')

    def test_default_configuration(self):
        self.browser.open(self.config_url)
        config = INotifierConfigurationSchema(self.portal)

        self.assertFalse(config.enabled)
        self.assertFalse(self.browser.getControl(name='form.enabled').value)

        self.assertFalse(config.detailed_report)
        self.assertFalse(self.browser.getControl(
                name='form.detailed_report').value)

        self.assertEqual(config.interval, 'daily')
        self.assertEqual(self.browser.getControl(name='form.interval').value,
                         ['daily'])

        self.assertEqual(config.get_receivers(), [])
        self.assertEqual(self.browser.getControl(name='form.receivers').value,
                         '')

    def test_save_with_defaults(self):
        self.browser.open(self.config_url)
        self.assertEqual(
            self.browser.getControl(name='form.receivers').value, '')
        self.browser.getControl('Save').click()

    def test_change_configuration(self):
        self.browser.open(self.config_url)
        self.browser.getControl(name='form.enabled').value = True
        self.browser.getControl(name='form.detailed_report').value = True
        self.browser.getControl(name='form.interval').value = ('weekly',)
        self.browser.getControl(name='form.receivers').value = '\n'.join((
            'my@test.local',
            'foo@bar.com'))

        self.browser.getControl('Save').click()
        self.assertEqual(self.browser.url, self.config_url)
        self.assertIn('Updated on', self.browser.contents)

        config = INotifierConfigurationSchema(self.portal)
        self.assertTrue(config.enabled)
        self.assertTrue(config.detailed_report)
        self.assertEqual(config.interval, 'weekly')
        self.assertEqual(config.get_receivers(), [
                'my@test.local', 'foo@bar.com'])

    def test_receier_mail_validation(self):
        self.assertEqual(
            INotifierConfigurationSchema(self.portal).get_receivers(), [])

        self.browser.open(self.config_url)
        self.browser.getControl(name='form.receivers').value = 'not an email'
        self.browser.getControl('Save').click()

        self.assertEqual(self.browser.url, self.config_url)
        self.assertNotIn('Updated on', self.browser.contents)
        self.assertIn('At least one of the defined addresses are not valid.',
                      self.browser.contents)

        self.assertEqual(
            INotifierConfigurationSchema(self.portal).get_receivers(), [])
