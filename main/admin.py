from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Post, Like, Comment, Profile, Preference

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class PreferenceInline(admin.StackedInline):
    model = Preference
    can_delete = False
    verbose_name_plural = "preference"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, PreferenceInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
