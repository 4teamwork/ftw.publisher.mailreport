from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.publisher.mailreport import _
from ftw.publisher.mailreport.interfaces import INotifierConfigurationSchema
from ftw.publisher.mailreport.utils import email_addresses_validator
from persistent.dict import PersistentDict
from plone.fieldsets.form import FieldsetsEditForm
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements


ANNOTATIONS_KEY = 'ftw.publisher.mailqueue-configuration'


class NotifierConfigurationAdapter(SchemaAdapterBase, object):
    """Stores the notifier configuration
    """

    adapts(IPloneSiteRoot)
    implements(INotifierConfigurationSchema)

    def __init__(self, context):
        super(NotifierConfigurationAdapter, self).__init__(self)
        self.annotations = IAnnotations(context)
        self.storage = self.annotations.get(ANNOTATIONS_KEY, None)
        if not isinstance(self.storage, PersistentDict):
            self.annotations[ANNOTATIONS_KEY] = PersistentDict()
            self.storage = self.annotations.get(ANNOTATIONS_KEY)

    def is_enabled(self):
        return self.storage.get('enabled', False) and True or False

    def set_enabled(self, value):
        self.storage['enabled'] = value and True or False

    enabled = property(is_enabled, set_enabled)

    def get_detailed_report(self):
        return self.storage.get('detailed_report', False) and True or False

    def set_detailed_report(self, value):
        self.storage['detailed_report'] = value and True or False

    detailed_report = property(get_detailed_report, set_detailed_report)

    def get_interval(self):
        return self.storage.get('interval', 'daily')

    def set_interval(self, value):
        self.storage['interval'] = value

    interval = property(get_interval, set_interval)

    def get_receivers_plain(self):
        return self.storage.get('receivers', '')

    def get_receivers(self):
        """Get receivers as list
        """
        data = self.storage.get('receivers', '')
        if data:
            return data.split('\n')
        else:
            return []

    def set_receivers_plain(self, value):
        self.storage['receivers'] = value

    receivers = property(get_receivers_plain, set_receivers_plain)


class NotificationConfigurationForm(FieldsetsEditForm):
    """Notification confugration form
    """

    template = ViewPageTemplateFile('config.pt')

    label = _(u'label_notifier_configuration',
              default=u'Notifier configuration')
    description = _(u'help_notifier_configuration',
                    default=u'Publisher notification configuration')

    form_name = label
    form_fields = form.FormFields(INotifierConfigurationSchema)

    def __init__(self, *args, **kwargs):
        super(NotificationConfigurationForm, self).__init__(*args, **kwargs)
        self.status = None

    @form.action(_(u'button_save', default=u'Save'))
    def handle_edit_action(self, action, data):
        """"Save" button handler.
        """
        if not email_addresses_validator(data.get('receivers')):
            self.status = _(u'error_invalid_addresses',
                            default=u'At least one of the defined addresses '
                            'are not valid.')
        else:
            # call the super handle_edit_action, but the method is
            # wrapped in a @form.action(), so we need to extract it...
            super_action = FieldsetsEditForm.handle_edit_action
            super_action_method = super_action.success_handler
            return super_action_method(self, action, data)

    @form.action(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action, data):
        """"Cancel" button handler.
        """
        portal = getSite()
        portal_url = getToolByName(self.context, 'portal_url')()
        url = portal_url + '/@@publisher-config'
        return portal.REQUEST.RESPONSE.redirect(url)
