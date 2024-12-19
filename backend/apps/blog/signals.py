from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.blog.models import Preference, Slideshow, Navbar, SocialMedia

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    # Default Preferences
    if not Preference.objects.exists():
        preference = Preference.objects.create(
            site_title="Site Title",
            site_subtitle="Site Subtitle",
            site_description="This is the default site description.",
            contact_email="admin@example.com",
            contact_phone="+1234567890"
        )
        print("Default Preferences created.")
        
        # Default Navbar
        Navbar.objects.bulk_create([
            Navbar(preference=preference, title="Beranda", link="/", order=1, icon="fa-home"),
        ])
        print("Default Navbars created.")


    # Default Social Media
    if not SocialMedia.objects.exists():
        SocialMedia.objects.create(
            preference=preference,
            facebook_url="https://facebook.com",
            twitter_url="https://twitter.com",
            instagram_url="https://instagram.com",
            linkedin_url="https://linkedin.com"
        )
        print("Default Social Media created.")
