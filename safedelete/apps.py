from django.apps import AppConfig


class SafeDeleteConfig(AppConfig):

    name = 'safedelete'
    verbose_name = 'Safe Delete'

    def ready(self):
        # Import checks to ensure they are registered
        from . import checks
