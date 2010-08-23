from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.utils import is_interval_expired


def invoke_notification(event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.
    
    """
    if is_interval_expired():
        return IReportNotifier(event.object)()
