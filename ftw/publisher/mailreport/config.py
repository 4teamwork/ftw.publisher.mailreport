from ftw.publisher.mailreport import _
from datetime import timedelta
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


INTERVAL_CONFIG = (
    # stored value, label i18n key, datetime dict
    ('hourly', u'interval_hourly', timedelta(hours=1)),
    ('daily',  u'interval_daily',  timedelta(days=1)),
    ('weekly', u'interval_weekly', timedelta(days=7)),
    )


INTERVAL_VOCABULARY = SimpleVocabulary([
        SimpleTerm(key, title=_(label))
        for key, label, td
        in INTERVAL_CONFIG])
