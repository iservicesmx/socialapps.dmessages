from django import forms
from django.utils.translation import ugettext_lazy as _

from socialapps.dmessages.fields import CommaSeparatedUserIdField
from socialapps.dmessages.models import Message, MessageRecipient

import datetime

class ComposeForm(forms.ModelForm):
    to = CommaSeparatedUserIdField(label=_("To"),
                                    widget= forms.HiddenInput())
    body = forms.CharField(label=_("Message"),
                           widget=forms.Textarea({'class': 'message', 'cols': 85, 'rows': 3}),
                           required=True)
    class Meta:
        model = Message
        fields = ('to','body')
        
