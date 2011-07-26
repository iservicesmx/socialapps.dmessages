from django import forms
from django.utils.translation import ugettext_lazy as _

from socialapps.dmessages.fields import CommaSeparatedUserField
from socialapps.dmessages.models import Message, MessageRecipient

import datetime

class ComposeForm(forms.ModelForm):
    to = CommaSeparatedUserField(label=_("To"))
    body = forms.CharField(label=_("Message"),
                           widget=forms.Textarea({'class': 'message'}),
                           required=True)
    class Meta:
        model = Message

    def save(self, sender):
        """
        Save the message and send it out into the wide world.

        :param sender:
            The :class:`User` that sends the message.

        :param parent_msg:
            The :class:`Message` that preceded this message in the thread.

        :return: The saved :class:`Message`.

        """
        to_user_list = self.cleaned_data['to']
        body = self.cleaned_data['body']

        msg = Message.objects.send_message(sender,
                                           to_user_list,
                                           body)

        return msg

