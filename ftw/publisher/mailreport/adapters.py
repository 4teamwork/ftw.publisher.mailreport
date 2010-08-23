from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from email.Header import Header
from email.MIMEText import MIMEText
from ftw.publisher.core import states
from ftw.publisher.mailreport import _
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.interfaces import IReportNotifier
from ftw.publisher.mailreport.utils import get_last_notification_date
from ftw.publisher.mailreport.utils import set_last_notification_date_to_now
from ftw.publisher.sender.interfaces import IQueue
from zope.component import getUtility
from zope.interface import implements


class MailReportNotifier(object):
    """Default report notifier. Sends notification emails.
    """
    implements(IReportNotifier)

    def __init__(self, portal):
        self.context = portal

    def __call__(self):
        self.send_email()
        set_last_notification_date_to_now()

    def send_email(self):
        """Sends the email
        """
        properties = getUtility(IPropertiesTool)
        mh = getToolByName(self.context, 'MailHost')
        from_addr = properties.email_from_address
        # prepare from address for header
        header_from = Header(properties.email_from_name.decode('utf-8'),
                             'iso-8859-1')
        header_from.append(u'<%s>' % from_addr.decode('utf-8'),
                           'iso-8859-1')

        # Subject
        subject = self.get_subject()
        header_subject = Header(unicode(subject), 'iso-8859-1')

        html_body = self.render_template().encode('utf-8')
        msg = MIMEText(html_body, 'html', 'utf-8')
        msg['From'] = header_from
        msg['Subject'] = header_subject

        for rcpt in self.get_configuration().get_receivers():
            msg['To'] = rcpt
            mh.secureSend(msg, mto=rcpt, mfrom=from_addr, subject=subject)

    def get_subject(self):
        return _(u'mail_subject',
                 default=u'Publisher report: ${site}',
                 mapping=dict(site=self.context.getProperty('title')))

    def get_configuration(self):
        """Returns the configuration adapter.
        """
        return INotifierConfigurationSchema(self.context)

    def get_options(self):
        """Returns a `dict` of data needed for rendering the mail template.
        """
        config = self.get_configuration()
        last_date = get_last_notification_date()
        queue = IQueue(self.context)
        data = {'success': 0,
                'warning': 0,
                'error': 0,
                'total': 0,
                'jobs_in_queue': 0,
                'erroneous_jobs': [],
                'show_details': config.detailed_report,
                'subject': self.get_subject()}

        # count the jobs by group and total
        for key, job in queue.get_executed_jobs():
            # get the runs
            runs = getattr(job, 'executed_list', None)
            if not runs or len(runs) == 0:
                continue

            # was it published since last notification?
            if last_date and runs[-1]['date'] < last_date:
                break

            # count it
            state = job.get_latest_executed_entry()
            if isinstance(state, states.ErrorState):
                data['error'] += 1
                data['erroneous_jobs'].append(job)
            elif isinstance(state, states.WarningState):
                data['warning'] += 1
            if isinstance(state, states.SuccessState):
                data['success'] += 1
            data['total'] += 1

        # get the amount of jobs in the queue
        data['jobs_in_queue'] = queue.countJobs()

        return data

    def render_template(self):
        template = self.context.restrictedTraverse('@@mail_notification_html')
        return template(**self.get_options())
