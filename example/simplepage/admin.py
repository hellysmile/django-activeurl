from django.contrib import admin
from simplepage.models import SimplePage


class SimplePageAdmin(admin.ModelAdmin):
    pass

admin.site.register(SimplePage, SimplePageAdmin)
