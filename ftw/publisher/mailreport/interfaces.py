from zope.interface import Interface


class IReportNotifier(Interface):
    """A `IReportNotifier` adapter is executed when the queue was executed
    (`QueueExecutedEvent`) and notifies about published objects - according
    to the configuration.
    """
