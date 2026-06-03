from django.contrib import admin
from .models import Subject, Question, QuestionMedia


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


class QuestionMediaInline(admin.TabularInline):
    model = QuestionMedia
    extra = 0
    fields = ['media_type', 'image', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'subject', 'source', 'year', 'is_active',
        'has_media', 'media_uploaded', 'created_at',
    ]
    list_filter = ['is_active', 'source', 'subject', 'media_uploaded']
    search_fields = ['question_text']
    inlines = [QuestionMediaInline]
    readonly_fields = ['media_uploaded']


@admin.register(QuestionMedia)
class QuestionMediaAdmin(admin.ModelAdmin):
    list_display = ['question', 'media_type', 'image', 'created_at']
    list_filter = ['media_type', 'question__subject']
    search_fields = ['question__question_text']
