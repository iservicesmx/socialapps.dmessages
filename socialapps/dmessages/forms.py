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
        exclude = ('sender','recipients')
        
