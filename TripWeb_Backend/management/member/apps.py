from django.apps import AppConfig

class MemberConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "management.member"

    def ready(self):
        import management.member.signals 
