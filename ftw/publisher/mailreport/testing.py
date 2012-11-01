from Testing.ZopeTestCase import installPackage
from collective.testcaselayer.common import common_layer
from collective.testcaselayer.ptc import BasePTCLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class MailreportFunctionalLayer(BasePTCLayer):
    """Layer for functional tests."""

    def afterSetUp(self):

        # Load testing zcml (optional)
        from ftw.publisher.mailreport import tests
        self.loadZCML('testing.zcml', package=tests)

        # installPackage() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        installPackage('ftw.publisher.mailreport')

        # Load GS profile
#         self.addProfile('ftw.publisher.mailreport:default')

    def beforeTearDown(self):
        pass


mailreport_functional_layer = MailreportFunctionalLayer(
    bases=[common_layer])


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
