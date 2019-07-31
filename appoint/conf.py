"""
The DEFAULT configuration is loaded when the named _CONFIG dictionary
is not present in your settings.
"""
#######################################################################

from django.urls import reverse_lazy

#######################################################################

CONFIG_NAME = "APPOINT_CONFIG"  # must be uppercase!


DEFAULT = {
    "exclude_current": True,
    "notification_methods": {
        "email": "appoint.methods.email",
        #'messages': 'appoint.methods.messages',
    },
    # You'll probably want to define this for your site,
    # e.g., url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='site-jsi18n'),
    "jsi18n_url": reverse_lazy("admin:jsi18n"),
}


#########################################################################

from django.conf import settings


def get(setting):
    """
    get(setting) -> value

    setting should be a string representing the application settings to
    retrieve.
    """
    assert setting in DEFAULT, "the setting %r has no default value" % setting
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return app_settings.get(setting, DEFAULT[setting])


def get_all():
    """
    Return all current settings as a dictionary.
    """
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return dict(
        [(setting, app_settings.get(setting, DEFAULT[setting])) for setting in DEFAULT]
    )


#########################################################################
