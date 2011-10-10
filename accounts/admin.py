from django.contrib import admin
from b4b.accounts.models import UserProfile




class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

admin.site.register(UserProfile, UserProfileAdmin)

