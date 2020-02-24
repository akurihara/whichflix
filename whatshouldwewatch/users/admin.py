from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from whatshouldwewatch.users.models import Device, User

admin.site.register(Device)
admin.site.register(User, UserAdmin)
