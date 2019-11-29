from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    name attribute for Django to determine which application this
    configuration applies to.
    """
    name = 'user'
