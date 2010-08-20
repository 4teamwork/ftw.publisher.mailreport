from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.fieldsets.form import FieldsetsEditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.publisher.mailreport import _
from z3c.form.button import buttonAndHandler
from zope.formlib import form
from z3c.form.validator import SimpleFieldValidator
from z3c.form.validator import WidgetValidatorDiscriminators
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.component import provideAdapter
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import implements
import re


ANNOTATIONS_KEY = 'ftw.publisher.mailqueue-configuration'


class INotifierConfigurationSchema(Interface):
    """Schema interface for notifier configuration.
    """

    enabled = schema.Bool(
        title=_(u'label_notification_enabled',
                default=u'Notification enabled'))

    detailed_report = schema.Bool(
        title=_(u'label_detailed_report',
                default=u'Detailed report'),
        description=_(u'help_detailed_report',
                      default=u'Include details of erroneous jobs.'))

    receivers = schema.Text(
        title=_(u'label_receivers', default=u'Receivers'),
        description=_(u'help_receivers',
                      default=u'Enter one e-mail address per line.'))


class AddressesValidator(SimpleFieldValidator):
    """Validator for validating the e-mail addresses field
    """

    MAIL_EXPRESSION = r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +\
        "?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +\
        "\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"

    def __init__(self, *args, **kwargs):
        super(AddressesValidator, self).__init__(*args, **kwargs)
        self.email_expression = re.compile(AddressesValidator.MAIL_EXPRESSION,
                                           re.IGNORECASE)

    def validate(self, value):
        """Validates the `value`, expects a list of carriage-return-separated
        email addresses.

        """
        super(AddressesValidator, self).validate(value)
        addresses = value.strip().split('\n')
        self._validate_addresses(addresses)

    def _validate_addresses(self, addresses):
        """E-Mail address validation
        """
        for addr in addresses:
            addr = addr.strip()
            if not self.email_expression.match(addr):
                msg = _(u'error_invalid_addresses',
                        default=u'At least one of the defined addresses '
                        'are not valid.')
                raise Invalid(msg)


WidgetValidatorDiscriminators(AddressesValidator,
                              field=INotifierConfigurationSchema['receivers'])
provideAdapter(AddressesValidator)


class NotifierConfigurationAdapter(SchemaAdapterBase):
    """Stores the notifier configuration
    """

    adapts(IPloneSiteRoot)
    implements(INotifierConfigurationSchema)

    def __init__(self, context):
        super(NotifierConfigurationAdapter, self).__init__(self, context)
        self.annotations = IAnnotations(context)
        self.storage = self.annotations.get(ANNOTATIONS_KEY, None)
        if not isinstance(self.storage, PersistentDict):
            self.annotations[ANNOTATIONS_KEY] = PersistentList()
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

    def get_receivers(self):
        return self.storage.get('receivers', [])

    def set_receivers(self, value):
        self.storage['receivers'] = PersistentList(value)

    receivers = property(get_receivers, set_receivers)
        

class NotificationConfigurationForm(FieldsetsEditForm):
    """Notification confugration form
    """
    
    template = ViewPageTemplateFile('config.pt')

    label = _(u'label_notifier_configuration',
              default=u'Notifier configuration')
    form_name = label
    form_fields = form.FormFields(INotifierConfigurationSchema)

    @buttonAndHandler(_(u'button_save', default=u'Save'))
    def handle_save(self, action):
        """"Save" button handler.
        """
        import pdb; pdb.set_trace()
        
        
    @buttonAndHandler(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action):
        """"Cancel" button handler.
        """
        portal = getSite()
        url = portal.portal_url.getPortalObject() + '/@@publisher-config'
        return portal.RESPONSE.redirect(url)
