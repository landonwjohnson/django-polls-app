from django.apps import AppConfig

class JobsConfig(AppConfig):
    name = 'jobs'  # Adjust based on your app's name

    def ready(self):
        from . import scheduler
        scheduler.start()
