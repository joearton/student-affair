from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_summernote.fields import SummernoteTextField
from apps.api.models import BaseModel


class Preference(BaseModel):
    site_title = models.CharField(_('Site Title'), max_length=255)
    site_subtitle = models.CharField(_('Site Subtitle'), max_length=512, blank=True, null=True)
    site_description = models.TextField(_('Site Description'), blank=True, null=True)
    site_logo = models.ImageField(_('Site Logo'), upload_to='preference/', blank=True, null=True)
    site_favicon = models.ImageField(_('Site Favicon'), upload_to='preference/', blank=True, null=True)    
    contact_email = models.EmailField(_('Contact Email'), blank=True, null=True)
    contact_phone = models.CharField(_('Contact Phone'), max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = _("Preference")
        verbose_name_plural = _("Preference")
        
    def __str__(self):
        return self.site_title
    

class Slideshow(BaseModel):
    preference = models.ForeignKey('Preference', on_delete=models.CASCADE, related_name="slideshows", verbose_name=_("Preference"))
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="slideshows/images/")
    link = models.URLField(_("Link"), null=True, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        ordering = ["order"]
        verbose_name = _("Slideshow")
        verbose_name_plural = _("Slideshow")


class Navbar(BaseModel):
    preference = models.ForeignKey('Preference', on_delete=models.CASCADE, related_name="navbars", verbose_name=_("Preference"))
    title = models.CharField(_("Title"), max_length=255)
    link = models.CharField(_("Link"), max_length=128)    
    icon = models.CharField(_("Icon"), max_length=255, null=True, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Navigation Item")
        verbose_name_plural = _("Navigation Items")
        ordering = ["order"]
        
    def __str__(self):
        return self.title


class SocialMedia(BaseModel):
    preference = models.OneToOneField('Preference', on_delete=models.CASCADE, related_name="social_medias", verbose_name=_("Preference"))
    facebook_url = models.URLField(_('Facebook URL'), max_length=512, blank=True, null=True)
    twitter_url = models.URLField(_('Twitter URL'), max_length=512, blank=True, null=True)
    instagram_url = models.URLField(_('Instagram URL'), max_length=512, blank=True, null=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), max_length=512, blank=True, null=True)
    youtube_url = models.URLField(_('Youtube URL'), max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Media')

    def __str__(self):
        return self.preference.__str__()
    

class Category(BaseModel):
    name = models.CharField(_("Category Name"), max_length=100, help_text=_("Enter the category name."))
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, help_text=_("Enter a unique slug for the category (used in the URL)."))
    description = models.TextField(_("Description"), blank=True, help_text=_("Optional: Enter a description for the category."))
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(_("Tag Name"), max_length=100, unique=True, help_text=_("Enter the tag name."))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Enter a unique slug for the tag (used in the URL)."))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Post(BaseModel):
    
    class PostStatus(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")
        
    class PostType(models.TextChoices):
        PAGE = "PAGE", _("Page")
        POST = "POST", _("Post")

    title = models.CharField(_("Title"), max_length=255, help_text=_("Enter the title of the post."))
    subtitle = models.CharField(_("Subtitle"), max_length=512, null=True, blank=True, help_text=_("Enter the subtitle of the post."))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Enter a unique slug for the post (used in the URL)."))    
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="posts", help_text=_("Select the author of the post."))
    content = SummernoteTextField(_("Content"), help_text=_("Enter the full content of the post."))
    publication_date = models.DateTimeField(_("Publication Date"), default=now, help_text=_("Enter the publication date and time."))
    kind = models.CharField(_("Type"), max_length=10, choices=PostType.choices, default=PostType.POST)
    status = models.CharField(_("Status"), max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT, help_text=_("Select the status of the post."))
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), related_name="posts", blank=True, help_text=_("Select categories for the post."))
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), related_name="posts", blank=True, help_text=_("Select tags for the post."))
    featured_image = models.ImageField(
        _("Featured Image"),
        upload_to="posts/images/",
        null=True, blank=True,
        help_text=_("Upload a featured image for the post.")
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-publication_date", "-date_created"]

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        """
        Check if the post is published.
        """
        return self.status == self.PostStatus.PUBLISHED and self.publication_date <= now()



