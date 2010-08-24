from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.utils import is_interval_expired


def invoke_notification(obj, event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.
    
    """
    if is_interval_expired():
        return IReportNotifier(obj)()
