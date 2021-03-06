from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.db.models import Q
from socialapps.core.utils import python_to_json

from socialapps.core.views import CreateView, JSONTemplateView
from socialapps.dmessages.models import Message, MessageRecipient, MessageContact
from socialapps.dmessages.forms import ComposeForm


import datetime
from socialapps import settings
if "notification" in settings.INSTALLED_APPS:
    import socialapps.core.notifications.functions as notification
    # from notification import models as notification
else:
    notification = none

class MessageList(ListView):
    """
    Returns the message list for this user. This is a list contacts
    which at the top has the user that the last conversation was with. This is
    an imitation of the iPhone SMS functionality.
    """
    template_name   = "messages/message_list.html"
    paginate_by     = 10
    context_object_name = "message_list"

    def get_queryset(self):
        return MessageContact.objects.get_contacts_for(self.request.user)

class MessageDetail(ListView):
    """
    Returns a conversation between two users
    """
    template_name   = "messages/message_detail.html"
    paginate_by     = 10
    context_object_name = "message_list"

    def get_queryset(self):
        uid = self.kwargs.get('userid', None)
        self.recipient = get_object_or_404(User, id=uid)
        return Message.objects.get_conversation_between(self.request.user,
                                                        self.recipient)

    def get_context_data(self, **kwargs):
        message_pks = [m.pk for m in kwargs['object_list']]
        unread_list = MessageRecipient.objects.filter(message__in=message_pks,
                                                      user=self.request.user,
                                                      read_at__isnull=True)
        now = datetime.datetime.now()
        unread_list.update(read_at=now)

        kwargs['recipient'] = self.recipient
        return super(MessageDetail, self).get_context_data(**kwargs)

class MessageCompose(CreateView):
    """
    Compose a new message

    :recipients:
        String containing the uids to whom the message is send to. Can be
        multiple uids by seperating them with a ``+`` sign.
    """
    action_title    = _("Create")
    type_title      = _("Message")
    form_class      = ComposeForm
    template_form   = "messages/message_form.html"

    def get_initial(self):
        initial = {}
        recipients = self.kwargs.get('recipients',None)

        if recipients:
            uids_list = [r.strip() for r in recipients.split("+")]
            recipients = ['u:' + str(u.id) for u in User.objects.filter(id__in=uids_list)]
            initial["to"] = ','.join(recipients)
        return initial

    def get_context_data(self, *args, **kwargs):
        if not self.get_initial():
            kwargs.update({
                'autocomplete' : True,
            })
        return super(MessageCompose, self).get_context_data(*args, **kwargs)

    def form_valid(self, form):

        sender = self.request.user
        recipients = form.cleaned_data['to']
        body = form.cleaned_data['body']
        for item in recipients['groups']:
            msg_group = Message.objects.send_message(sender, item.user_set.all(), body, True)

            if notification:
                notification.send_now(item.user_set.all(), 'user_message', {'from_user' : sender.get_profile(), 'message' : body });

        msg_users = Message.objects.send_message(sender, recipients['users'], body)

        if notification:
            notification.send_now(recipients['users'], 'user_message', {'from_user' : sender.get_profile(), 'message' : body });

        messages.success(self.request, _('The message was sent.'), fail_silently=True)

        requested_redirect = self.request.REQUEST.get(REDIRECT_FIELD_NAME, False)

        # Redirect mechanism
        self.success_url = reverse('socialapps_messages_list')

        if requested_redirect:
            self.success_url = requested_redirect
        elif len(recipients) == 1:
            self.success_url = reverse('socialapps_messages_detail', kwargs={'userid': recipients[0].id})
        return HttpResponse(python_to_json({"success": True, "success_url": self.success_url}), content_type='application/json')

    def form_invalid(self, form):
        return HttpResponse(python_to_json({"errors" : form.errors}), content_type='application/json')

class MessageRecipients(JSONTemplateView):
    template_name = 'messages/message_list.html'
    def get_context_data(self, *args, **kwargs):
        items = [{'label': item.name, 'category': 'user', 'id': item.user.id } for item in self.request.site.school.members] + [{'label': item.group.name, 'id': item.group.id, 'category': 'group'} for item in self.request.site.school.groups]
        term = self.request.GET.get('term', None)
        if term:
            users = self.request.site.school.members.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(user__email__icontains=term))
            groups = self.request.site.school.groups.filter(group__name__icontains=term)
        else:
            users = self.request.site.school.members
            groups = self.request.site.school.groups

        return [{'label': item.name, 'category': 'user', 'id': item.user.id } for item in users] + [{'label': item.group.name, 'id': item.group.id, 'category': 'group'} for item in groups]

def message_remove(request, undo=False):
    """
    A ``POST`` to remove messages.

    :param undo:
        A Boolean that if ``True`` unremoves messages.

    POST can have the following keys:

        ``message_pks``
            List of message id's that should be deleted.

        ``next``
            String containing the URI which to redirect to after the keys are
            removed. Redirect defaults to the inbox view.

    The ``next`` value can also be supplied in the URI with ``?next=<value>``.

    """
    message_pks = request.POST.getlist('message_pks')
    redirect_to = request.REQUEST.get('next', False)

    if message_pks:
        # Check that all values are integers.
        valid_message_pk_list = set()
        for pk in message_pks:
            try: valid_pk = int(pk)
            except (TypeError, ValueError): pass
            else:
                valid_message_pk_list.add(valid_pk)

        # Delete all the messages, if they belong to the user.
        now = datetime.datetime.now()
        changed_message_list = set()
        for pk in valid_message_pk_list:
            message = get_object_or_404(Message, pk=pk)

            # Check if the user is the owner
            if message.sender == request.user:
                if undo:
                    message.sender_deleted_at = None
                else:
                    message.sender_deleted_at = now
                message.save()
                changed_message_list.add(message.pk)

            # Check if the user is a recipient of the message
            if request.user in message.recipients.all():
                mr = message.messagerecipient_set.get(user=request.user,
                                                      message=message)
                if undo:
                    mr.deleted_at = None
                else:
                    mr.deleted_at = now
                mr.save()
                changed_message_list.add(message.pk)

        # Send messages
        if (len(changed_message_list) > 0):
            if undo:
                message = ungettext('Message is succesfully restored.',
                                    'Messages are succesfully restored.',
                                    len(changed_message_list))
            else:
                message = ungettext('Message is successfully removed.',
                                    'Messages are successfully removed.',
                                    len(changed_message_list))

            messages.success(request, message, fail_silently=True)

    if redirect_to: return redirect(redirect_to)
    else: return redirect(reverse('socialapps_messages_list'))
