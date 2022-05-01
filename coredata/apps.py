from django.apps import AppConfig


class CoredataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coredata'

    def ready(self):
        # everytime server restarts
        import coredata.signals
