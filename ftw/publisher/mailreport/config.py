from ftw.publisher.mailreport import _
from datetime import timedelta
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


# annotation key of the date, when the last notification was triggered
LAST_NOTIFICATIONS_KEY = 'ftw.publisher.mailreport-last-notification'


INTERVAL_CONFIG = (
    # stored value, label i18n key, datetime dict
    ('hourly', _(u'interval_hourly'), timedelta(hours=1)),
    ('daily',  _(u'interval_daily'),  timedelta(days=1)),
    ('weekly', _(u'interval_weekly'), timedelta(days=7)),
    )


INTERVAL_VOCABULARY = SimpleVocabulary([
        SimpleTerm(key, title=_(label))
        for key, label, td
        in INTERVAL_CONFIG])
