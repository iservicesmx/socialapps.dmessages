from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from notification.models import NoticeType
from django.contrib.sites import models as site_app

def create_notice_types(app, created_models, verbosity, **kwargs):
    print "create message notifications"
    NoticeType.create("user_message", _("Message you"), _("Someone send you a message"), default = 2)
    
signals.post_syncdb.connect(create_notice_types, sender=site_app)
