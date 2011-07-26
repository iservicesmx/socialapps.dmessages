# encoding: utf-8

from socialapps.dmessages.models import MessageRecipient

#TODO: Caching

def messages_new(request):
    if request.user.is_authenticated():
        return {'messages_new_count': MessageRecipient.objects.count_unread_messages_for(request.user)}
    else:
        return {}
