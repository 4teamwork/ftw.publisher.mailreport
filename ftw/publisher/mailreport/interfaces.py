from zope import schema
from ftw.publisher.mailreport import _
from zope.interface import Interface


class IReportNotifier(Interface):
    """A `IReportNotifier` adapter is executed when the queue was executed
    (`QueueExecutedEvent`) and notifies about published objects - according
    to the configuration.
    """


class INotifierConfigurationSchema(Interface):
    """Schema interface for notifier configuration.
    """

    enabled = schema.Bool(
        title=_(u'label_notification_enabled',
                default=u'Notification enabled'))

    detailed_report = schema.Bool(
        title=_(u'label_detailed_report',
                default=u'Detailed report'),
        description=_(u'help_detailed_report',
                      default=u'Include details of erroneous jobs.'))

    receivers = schema.Text(
        title=_(u'label_receivers', default=u'Receivers'),
        description=_(u'help_receivers',
                      default=u'Enter one e-mail address per line.'),
        required=False)
