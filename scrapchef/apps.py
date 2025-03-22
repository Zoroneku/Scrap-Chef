from django.apps import AppConfig


class ScrapchefConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrapchef'

    def ready(self):
        import scrapchef.signals
