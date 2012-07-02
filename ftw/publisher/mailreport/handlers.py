from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.utils import is_interval_expired
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema


def invoke_notification(obj, event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.
    """

    config = INotifierConfigurationSchema(obj)
    if config.enabled and is_interval_expired():
        return IReportNotifier(obj)()
