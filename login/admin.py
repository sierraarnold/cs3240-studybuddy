from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', ]}),
    ]
    list_display = ('user', 'username', )
    search_fields = ['username']

admin.site.register(Profile, ProfileAdmin)
