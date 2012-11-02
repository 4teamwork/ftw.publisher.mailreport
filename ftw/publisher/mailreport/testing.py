from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class MailReportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        from ftw.publisher.mailreport import tests
        xmlconfig.file('testing.zcml', tests,
                       context=configurationContext)


MAILREPORT_FIXTURE = MailReportLayer()
MAILREPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MAILREPORT_FIXTURE, ),
    name="ftw.publisher.mailreport:Integration")
MAILREPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MAILREPORT_FIXTURE, ),
    name="ftw.publisher.mailreport:Functional")
