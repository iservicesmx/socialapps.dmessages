from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required

from socialapps.dmessages import views as messages_views

urlpatterns = patterns('',
    url(r'^compose/$',
        login_required(messages_views.MessageCompose.as_view()),
        name='socialapps_messages_compose'),

    url(r'^compose/(?P<recipients>[\+\w]+)/$',
        messages_views.MessageCompose.as_view(),
        name='socialapps_messages_compose_to'),

    url(r'^reply/(?P<parent_id>[\d]+)/$',
        messages_views.MessageCompose.as_view(),
        name='socialapps_messages_reply'),

    url(r'^view/(?P<userid>\d+)/$',
        login_required(messages_views.MessageDetail.as_view()),
        name='socialapps_messages_detail'),


    url(r'^remove/$',
        messages_views.message_remove,
        name='socialapps_messages_remove'),

    url(r'^unremove/$',
        messages_views.message_remove,
        {'undo': True},
        name='socialapps_messages_unremove'),

    url(r'^$',
        login_required(messages_views.MessageList.as_view()),
        name='socialapps_messages_list'),
)
