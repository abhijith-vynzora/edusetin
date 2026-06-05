from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    # Dashboard
    path('', views.student_management_dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/<int:id>/', views.student_detail, name='student_detail'),
    path('students/<int:id>/activate/', views.student_activate, name='student_activate'),
    path('students/<int:id>/deactivate/', views.student_deactivate, name='student_deactivate'),
    path('students/<int:id>/delete/', views.student_delete, name='student_delete'),

    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:id>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:id>/activate/', views.subject_activate, name='subject_activate'),
    path('subjects/<int:id>/deactivate/', views.subject_deactivate, name='subject_deactivate'),
    path('subjects/<int:id>/delete/', views.subject_delete, name='subject_delete'),

    # Questions
    path('questions/', views.question_list, name='question_list'),
    path('questions/create/', views.question_create, name='question_create'),
    path('questions/import/', views.question_import, name='question_import'),
    path('questions/import/download-template/', views.download_question_template, name='download_question_template'),
    path('questions/<int:id>/', views.question_detail, name='question_detail'),
    path('questions/<int:id>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:id>/activate/', views.question_activate, name='question_activate'),
    path('questions/<int:id>/deactivate/', views.question_deactivate, name='question_deactivate'),
    path('questions/<int:id>/delete/', views.question_delete, name='question_delete'),

    # Media Management – Question-level
    path('media/pending/', views.media_pending, name='media_pending'),
    path('media/question/<int:id>/', views.media_upload, name='media_upload'),
    path('media/question/<int:id>/delete/<str:media_type>/', views.media_delete, name='media_delete'),

    # Media Library (two-section page)
    path('media/library/', views.media_library, name='media_library'),

    # Media Assets CRUD (MediaLibrary model)
    path('media/assets/upload/', views.media_assets_upload, name='media_assets_upload'),
    path('media/assets/<int:id>/edit/', views.media_assets_edit, name='media_assets_edit'),
    path('media/assets/<int:id>/delete/', views.media_assets_delete, name='media_assets_delete'),
    path('media/assets/<int:id>/toggle/', views.media_assets_toggle, name='media_assets_toggle'),
    path('media/assets/api/', views.media_assets_api, name='media_assets_api'),
]
