from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


JAZZMIN_SETTINGS = {
    "site_title": "Laboratory Admin",
    "site_header": "Laboratory Admin",
    "site_brand": "Laboratory Admin",
    "site_logo": "logo.png",
    "login_logo": "logo.png",
    "welcome_sign": "Welcome to the Laboratory Admin",
    "copyright": "ArtonLabs",
    "search_model": [],
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {},
    "related_modal_active": True,
    "custom_css": 'api/styles/jazzmin.css',
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": True,
    "custom_links": {
        "scholarship": [{
            "name": _('Toolbox'), 
            "url": f"/laboratory/scholarship/preference/toolbox", 
            "icon": "fas fa-cogs",
            "permissions": ["scholarship.change_preference"]
        }]
    },
    "order_with_respect_to": [
        "auth",
        "blog",
        "scholarship",
        "scholarship.student",
        "scholarship.reviewer",
        "scholarship.scholarship",
        "scholarship.scholarshipattachment",
        "scholarship.scholarshipapplication",
        "scholarship.unit",
        "scholarship.university",
        "scholarship.faculty",
        "scholarship.department",
        "scholarship.office",
    ],
    # "default_icon_parents": "fas fa-caret-right",
    "default_icon_children": "fas fa-caret-right",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user", 
        "auth.group": "fas fa-users", 
        "blog.category": "fas fa-folder-open",
        "blog.post": "fas fa-newspaper",
        "blog.preference": "fas fa-sliders-h",
        "blog.tag": "fas fa-tags",
        "scholarship.preference": "fas fa-sliders-h",
        "scholarship.unit": "fas fa-building",
        "scholarship.university": "fas fa-university",
        "scholarship.faculty": "fa fa-university",
        "scholarship.department": "fa fa-building",
        "scholarship.office": "fa fa-building",
        "scholarship.scholarship": "fas fa-award",
        "scholarship.scholarshipattachment": "fas fa-file-alt",
        "scholarship.scholarshipapplication": "fas fa-file-signature",
        "scholarship.student": "fas fa-user-graduate",
        "scholarship.reviewer": "fas fa-users" 
    }
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": 'bg-white',
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "lumen",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}