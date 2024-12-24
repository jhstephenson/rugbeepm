from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.project'

    def ready(self):
        """
        Import signal handlers and perform other initialization.
        """
        try:
            import apps.project.signals  # noqa
        except ImportError:
            pass
