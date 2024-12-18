from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.scholarship.models import Preference

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if not Preference.objects.exists():
        preference = Preference.objects.create(
            sister_api = Preference.EnableDisableChoice.ENABLED,
            sevima_api = Preference.EnableDisableChoice.ENABLED,
        )
        print("Default Preferences created.")
        