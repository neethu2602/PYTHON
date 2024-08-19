from django.apps import AppConfig


class Task62Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task62'
    def ready(self):
        import task62.signals