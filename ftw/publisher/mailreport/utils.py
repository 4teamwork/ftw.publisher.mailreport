from ftw.publisher.mailreport.config import INTERVAL_CONFIG
from ftw.publisher.mailreport.config import LAST_NOTIFICATIONS_KEY
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
import datetime
import re


def is_interval_expired():
    """Returns `True` if the interval is expired. Returns `True`
    if there is no last notification date set. It does not modify
    the date.
    """
    # get the last notification date
    lndate = get_last_notification_date()
    if not lndate:
        return True
    # get the configurated interval timedelta
    delta = get_interval_delta()
    # is `lndate` + `delta` already past?
    return lndate + delta < datetime.datetime.now()


def get_last_notification_date():
    """Returns the `datetime` of the last sent notification or `None`
    if there is nothing set.
    """
    portal = getSite()
    annotations = IAnnotations(portal)
    ttuple = annotations.get(LAST_NOTIFICATIONS_KEY)
    if ttuple:
        return datetime.datetime(*ttuple)
    else:
        return None


def set_last_notification_date_to_now():
    """Sets the "last sent notification date" to the current time.
    """
    portal = getSite()
    annotations = IAnnotations(portal)
    now = datetime.datetime.now()
    annotations[LAST_NOTIFICATIONS_KEY] = now.timetuple()[:6]


def get_interval_delta():
    """Returns a `timedelta` object of the configured interval or `None`.
    """
    portal = getSite()
    interval = INotifierConfigurationSchema(portal).get_interval()
    for key, _label, delta in INTERVAL_CONFIG:
        if key == interval:
            return delta


def email_addresses_validator(value):
    """Validator for validating e-mail addresses.
    `value` is a string of carriage-return-seperated bulk of e-mail addresses.
    Returns `True` if all addresses are valid, otherwise `False`.
    """

    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +
                      r"?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +
                      r"\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$",
                      re.IGNORECASE)

    if value is None:
        # empty field is ok
        return True

    addresses = value.strip().split('\n')
    for addr in addresses:
        addr = addr.strip()
        if not expr.match(addr):
            return False
    return True
