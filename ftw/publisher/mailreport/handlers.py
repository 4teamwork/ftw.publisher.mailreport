from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.utils import is_interval_expired
from ftw.publisher.mailreport.utils import set_last_notification_date_to_now


def invoke_notification(event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.
    
    """
    if is_interval_expired():
        set_last_notification_date_to_now()
        return IReportNotifier(event.object)()
