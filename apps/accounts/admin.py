from django.contrib import admin
from models import UserProfile, Permission, ValidSMSCode, ValidPasswordResetKey
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)


admin.site.register(UserProfile)
admin.site.register(Permission)
admin.site.register(ValidSMSCode)
admin.site.register(ValidPasswordResetKey)


__author__ = 'mark'


