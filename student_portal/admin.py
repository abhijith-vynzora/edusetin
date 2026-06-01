from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'is_active', 'created_at')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('is_active', 'created_at')
