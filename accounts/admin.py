from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

from .forms import EmailAdminAuthenticationForm
from .models import Account, UserProfile
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture and object.profile_picture.name:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">', object.profile_picture.url)
        else:
            return "No Image"
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
class MyAdminSite(AdminSite):
    login_form = EmailAdminAuthenticationForm
    login_template = 'admin/login.html'  # optional if you want to customize login page
    site_header = 'My Admin'
    site_title = 'My Admin Portal'

admin_site = MyAdminSite(name='myadmin')

# Register your model with the custom site
admin_site.register(Account)
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
