from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'full_name', 'phone', 'is_verified')
