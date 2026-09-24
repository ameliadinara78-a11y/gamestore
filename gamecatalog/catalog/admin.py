from django.contrib import admin

from .models import Game, License, Platform, Tag


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name", "is_copyleft")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "license", "stars", "is_published")
    list_filter = ("is_published", "license", "platforms", "tags")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("platforms", "tags")
    autocomplete_fields = ()
