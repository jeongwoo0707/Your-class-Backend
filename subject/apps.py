from django.apps import AppConfig


class SubjectConfig(AppConfig):
    name = 'subject'
    verbose_name = 'subject configuration'
    def ready(self):
        import subject.signals