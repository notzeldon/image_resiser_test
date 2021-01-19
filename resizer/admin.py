from django.contrib import admin

from .models import *


@admin.register(SourceImage)
class SourceImageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ModifiedImage)
class ModifiedImageModelAdmin(admin.ModelAdmin):
    pass
