from django.db.models import signals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_noop as _


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("user_message", _("Message you"), _("Someone send you a message"), default = 2)
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)

else:
    print "Skipping creation of NoticeTypes as notification app not found"