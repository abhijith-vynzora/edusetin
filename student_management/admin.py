from django.contrib import admin
from .models import Subject, Question


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subject', 'source', 'year', 'is_active', 'created_at']
    list_filter = ['is_active', 'source', 'subject']
    search_fields = ['question_text']
