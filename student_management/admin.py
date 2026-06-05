from django.contrib import admin
from django.utils.html import format_html
from .models import Subject, Question, QuestionMedia, MediaLibrary, PendingMediaReference


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


class QuestionMediaInline(admin.TabularInline):
    model = QuestionMedia
    extra = 0
    fields = ['media_type', 'image', 'media_library', 'created_at']
    readonly_fields = ['created_at']


class PendingMediaReferenceInline(admin.TabularInline):
    model = PendingMediaReference
    extra = 0
    fields = ['media_type', 'expected_media_name', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'subject', 'source', 'year', 'is_active',
        'has_media', 'media_uploaded', 'created_at',
    ]
    list_filter = ['is_active', 'source', 'subject', 'media_uploaded']
    search_fields = ['question_text']
    inlines = [QuestionMediaInline, PendingMediaReferenceInline]
    readonly_fields = ['media_uploaded']


@admin.register(QuestionMedia)
class QuestionMediaAdmin(admin.ModelAdmin):
    list_display = ['question', 'media_type', 'image', 'media_library', 'created_at']
    list_filter = ['media_type', 'question__subject']
    search_fields = ['question__question_text']


@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'is_active', 'usage_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'image_preview_large']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;max-width:80px;object-fit:cover;border-radius:4px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:400px;object-fit:contain;border-radius:6px;" />',
                obj.image.url
            )
        return '—'
    image_preview_large.short_description = 'Current Image'

    def usage_count(self, obj):
        count = obj.usages.count()
        return count
    usage_count.short_description = 'Used By'


@admin.register(PendingMediaReference)
class PendingMediaReferenceAdmin(admin.ModelAdmin):
    list_display = ['question', 'media_type', 'expected_media_name', 'created_at']
    list_filter = ['media_type']
    search_fields = ['expected_media_name', 'question__question_text']
