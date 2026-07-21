from django.contrib import admin
from .models import Story, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'priority', 'updated_at')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'priority')
    search_fields = ('title', 'headline', 'slug')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'category', 'language', 'published')
    list_filter = ('category', 'language', 'source')
    search_fields = ('title', 'source')
