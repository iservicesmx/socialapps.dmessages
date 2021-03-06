from django import forms
from django.forms import widgets
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

class CommaSeparatedUserInput(widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([user.username for user in value]))
        return super(CommaSeparatedUserInput, self).render(name, value, attrs)

# class CommaSeparatedFullName(widgets.Input):

class CommaSeparatedUserIdField(forms.Field):
    """
    A :class:`CharField` that exists of comma separated user ids.

    :param recipient_filter:
        Optional function which receives as :class:`User` as parameter. The
        function should return ``True`` if the user is allowed or ``False`` if
        the user is not allowed.

    :return:
        A list of :class:`User`.

    """
    widget = CommaSeparatedUserInput

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        self._recipient_filter = recipient_filter
        super(CommaSeparatedUserIdField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CommaSeparatedUserIdField, self).clean(value)

        ids = set(value.split(','))
        uids_set = set([int(uid.split(':')[1].strip()) for uid in ids if uid.split(':')[0] == 'u'])
        users = list(User.objects.filter(id__in=uids_set))

        gids_set = set([int(uid.split(':')[1].strip()) for uid in ids if uid.split(':')[0] == 'g'])
        groups = list(Group.objects.filter(id__in=gids_set))

        # Check for unknown names.
        unknown_names = uids_set ^ set([user.id for user in users])

        recipient_filter = self._recipient_filter
        invalid_users = []
        if recipient_filter is not None:
            for r in users:
                if recipient_filter(r) is False:
                    users.remove(r)
                    invalid_users.append(r.username)

        if unknown_names or invalid_users:
            humanized_usernames = ', '.join(list(unknown_names) + invalid_users)
            raise forms.ValidationError(_("The following users ids are incorrect: %(users)s.") % {'users': humanized_usernames})

        return {'users': users, 'groups': groups}
