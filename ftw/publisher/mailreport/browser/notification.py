from Products.Five import BrowserView


class TriggerNotification(BrowserView):
    """This view triggers the notification.
    """

    def __call__(self):
        raise NotImplemented
