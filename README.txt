Introduction
============


Using socialapps.messages
=========================

Download
--------

socialapp.dmessages is only currently available on our private repositories. It
is available at this git URL:

    git://git@github.com:iservicesmx/socialapps.dmessages.git

Installing with Buildout
-----------------------

Open your buildout.cfg file and add `socialapps.dmessages` to your list of
eggs; for example:

    [django]
    recipe = djangorecipe
    version = 1.3
    eggs=
        ...
        socialapps.messages


After updating the configuration you need to run the ''bin/buildout'', which
will take care of updating your system.

Configure your Dajngo app
==========================

Open your settings.py file and modify where appropiate:

    TEMPLATE_CONTEXT_PROCESSORS = [
       ...
       "socialapps.dmessages.context_processors.messages_new",
    ]

    ...

    INSTALLED_APPS = [
        ...
        'socialapps.dmessages',
    ]

Open your urls.py file and modify where apropriate:

    urlpatterns = patterns(
        ...
        (r'^messages/', include('socialapps.dmessages.urls')),
    )

Copyright and Credits
======================

`socialapps.dmessages` is Licensed under the MIT License. See LICENSE.txt for
details.

Author: iServices Developers <devel@iservices.mx>

HomePage: http://iservices.mx

