from ftw.publisher.mailreport.interfaces import IReportNotifier

def invoke_notification(event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.
    
    """
    IReportNotifier(event.object)()
