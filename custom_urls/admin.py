from django.contrib import admin

# Register your models here.

from .models import CustomUrl

admin.site.register(CustomUrl)
