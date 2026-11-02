from django.contrib import admin
from .models import Story, Topic, RecommendedBook, RecommendedProduct


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


@admin.register(RecommendedBook)
class RecommendedBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'language', 'is_active', 'click_count')
    list_filter = ('category', 'language', 'is_active')
    search_fields = ('title', 'author', 'asin')


@admin.register(RecommendedProduct)
class RecommendedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'language', 'is_active', 'click_count')
    list_filter = ('category', 'language', 'is_active')
    search_fields = ('name', 'search_query')
