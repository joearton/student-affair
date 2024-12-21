from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Post, Category, Tag, Slideshow, Navbar, SocialMedia, Preference


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    """
    list_display = ('title', 'author', 'status', 'publication_date', 'is_deleted')
    list_filter = ('status', 'author', 'date_created')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (_('General Information'), {
            'fields': ('title', 'subtitle', 'content', 'categories', 'tags')
        }),
        (_('Content'), {
            'fields': ('slug', 'featured_image')
        }),
        (_('Publication Settings'), {
            'fields': ('status', 'publication_date')
        }),
        (_('Audit Information'), {
            'fields': ('date_created', 'date_modified', 'date_deleted'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('date_created', 'date_modified', 'date_deleted')


    def save_model(self, request, obj, form, change):
        """
        Override save_model to set the author automatically for new objects.
        """
        if not obj.pk:  # Jika objek baru dibuat (bukan update)
            obj.author = request.user
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        """
        Customize the queryset to allow superusers to see all posts,
        and regular users to see only their own posts.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


    def get_readonly_fields(self, request, obj=None):
        """
        Make the 'author' field readonly for existing objects.
        """
        if obj:  # Jika sedang mengedit objek yang sudah ada
            return self.readonly_fields + ('author',)
        return self.readonly_fields
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    """
    Admin configuration for the Category model.
    """

    list_display = ('name', 'slug', 'description')  # Kolom yang ditampilkan di daftar
    search_fields = ('name', 'slug')  # Kolom yang dapat dicari
    prepopulated_fields = {'slug': ('name',)}  # Otomatis mengisi slug berdasarkan nama
    ordering = ('name',)  # Menyortir berdasarkan nama

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
    )
    # Untuk menambahkan kontrol akses lebih lanjut
    # readonly_fields = ('slug',)  # Jika ingin menjadikan slug hanya baca


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    list_display = ('name', 'slug')  # Kolom yang ditampilkan di daftar
    search_fields = ('name', 'slug')  # Kolom yang dapat dicari
    prepopulated_fields = {'slug': ('name',)}  # Otomatis mengisi slug berdasarkan nama
    ordering = ('name',)  # Menyortir berdasarkan nama

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
    )
    # readonly_fields = ('slug',)  # Jika ingin menjadikan slug hanya baca
    
    
class SlideshowInline(admin.StackedInline):
    model = Slideshow
    extra = 1


class NavbarInline(admin.StackedInline):
    model = Navbar
    extra = 1


class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
    extra = 1


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    inlines = [SlideshowInline, NavbarInline, SocialMediaInline]

    def has_add_permission(self, request):
        return not Preference.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # Redirect to the change form if an object already exists
        try:
            preference = Preference.objects.get()
            return HttpResponseRedirect(reverse("admin:blog_preference_change", args=[preference.id]))
        except Preference.DoesNotExist:
            return HttpResponseRedirect(reverse("admin:blog_preference_add"))


