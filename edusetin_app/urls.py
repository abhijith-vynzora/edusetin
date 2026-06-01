from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
        "chatbot-enquiries/export-excel/",
        views.export_chatbot_enquiries_excel,
        name="export_chatbot_enquiries_excel",
    ),
    path(
        "chatbot-enquiries/",
        views.chatbot_enquiries_list,
        name="chatbot_enquiries_list",
    ),
    path(
        "chatbot-enquiries/delete/<int:enquiry_id>/",
        views.delete_chatbot_enquiry,
        name="delete_chatbot_enquiry",
    ),
    path("save-chatbot-data/", views.save_chatbot_data, name="save_chatbot_data"),
    path("get-chatbot-options/", views.get_chatbot_options, name="get_chatbot_options"),
    # userviews >>>>>>>>>
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    # path("country/<int:pk>/", views.country_details, name="country_detail"),
    path("country/<slug:slug>/", views.country_details, name="country_detail"),
    path("university-detail/<slug:slug>/", views.university_detail, name="uni_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("add-team/", views.create_team, name="team_add"),
    path("team/", views.list_team, name="team_list"),
    path("team/<int:pk>/edit/", views.edit_team_member, name="edit_team_member"),
    path("team/<int:pk>/delete/", views.delete_team_member, name="delete_team_member"),
    # gallery
    path("list-images/", views.gallery_images, name="list_image"),
    path("add_image/", views.add_image, name="add_image"),
    path("delete-image/<int:image_id>/", views.delete_image, name="delete_image"),
    # contact
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("admin_contacts/", views.admin_contacts, name="admin_contacts"),
    path(
        "admin_contacts/delete/<int:contact_id>/",
        views.delete_contact,
        name="delete_contact",
    ),
    path("contacts/export/", views.export_contacts_excel, name="export_contacts_excel"),
    path(
        "applications/export/",
        views.export_applications_excel,
        name="export_applications_excel",
    ),
    # blogs
    path("blog/<slug:slug>/", views.blog_details, name="blog_detail"),

    path("view-blogs/", views.index_blog, name="index_blog"),
    path("country-details/", views.country_details, name="country-details"),
    # adminviews >>
    path("subscribe/", views.subscribe_newsletter, name="subscribe_newsletter"),
    path("subscribers/", views.subscriber_list, name="subscriber_list"),
    path(
        "subscribers/delete/<int:pk>/",
        views.delete_subscriber,
        name="delete_subscriber",
    ),
    path("countries/", views.countries_list, name="country_list"),
    path("countries-create/", views.country_create, name="create_country"),
    path("countries/<int:pk>/update/", views.country_update, name="update_country"),
    path("countries/<int:pk>/delete/", views.country_delete, name="delete_country"),
    path("create-universities/", views.add_university, name="create-universities"),
    path("uni-list/", views.universities_list, name="uni-list"),
    path(
        "universities/update/<int:pk>/",
        views.update_university,
        name="update_university",
    ),
    path(
        "universities/delete/<int:pk>/",
        views.delete_university,
        name="delete_university",
    ),
    # create cousre
    path("courses/", views.course_list, name="course_list"),
    path("add-courses/", views.course_add, name="course_add"),
    path("testimonials/", views.testimonial_list, name="testimonial_list"),
    path("add-review", views.testimonial_create, name="testimonial_create"),
    path(
        "testimonials/<int:pk>/edit/",
        views.testimonial_update,
        name="testimonial_update",
    ),
    path(
        "testimonials/<int:pk>/delete/",
        views.testimonial_delete,
        name="testimonial_delete",
    ),
    path("courses/<int:pk>/edit/", views.course_update, name="update_course"),
    path("courses/<int:pk>/delete/", views.course_delete, name="course_delete"),
    # Services
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),

    path("services/", views.service_list, name="service_list"),
    path("add-services", views.service_create, name="service_create"),
    path("services/<int:pk>/edit/", views.service_update, name="service_update"),
    path("services/<int:pk>/delete/", views.service_delete, name="service_delete"),
    # Blogs
    path("blogs/", views.blog_list, name="blog_list"),
    path("add-blogs/", views.blog_create, name="blog_create"),
    path("blogs/<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("blogs/<int:pk>/delete/", views.blog_delete, name="blog_delete"),
    # contact us enquiry userside
    path("inquiry/", views.inquiry_view, name="contact_us"),
    path("inquiries-list/", views.inquiry_list, name="inquiry_list"),
    path("delete/<int:pk>/", views.delete_inquiry, name="delete_inquiry"),
    # apply form userside
    path("apply-form/", views.apply_form, name="apply_form"),
    # user application adminside
    path("applications/", views.application_list, name="application_list"),
    path(
        "applications/delete/<int:app_id>/",
        views.delete_application,
        name="delete_application",
    ),
    path(
        "get-courses/<int:country_id>/",
        views.get_courses_by_country,
        name="get_courses",
    ),
    path(
        "course-category/",
        views.course_category_list_create,
        name="course_category_list_create",
    ),
    path("course-categories/", views.course_category_list, name="course_category_list"),
    path(
        "course-category/update/<int:pk>/",
        views.course_category_update,
        name="course_category_update",
    ),
    path(
        "course-category/delete/<int:pk>/",
        views.course_category_delete,
        name="course_category_delete",
    ),
    path("course-categories/<slug:slug>/", views.course_category_detail, name="course_category_detail"),
    path(
        "export-inquiries-excel/",
        views.export_inquiries_excel,
        name="export_inquiries_excel",
    ),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/update/<int:pk>/", views.update_category, name="update_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    path("login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),
    
    path('universities/reorder/', views.reorder_universities, name='reorder_universities'),
    path('reorder-services/',views.reorder_services, name='reorder_services'),
    path('reorder-countries/', views.reorder_countries, name='reorder_countries'),
    path('reorder-course-categories/', views.reorder_course_categories, name='reorder_course_categories'),
    path('reorder-courses/', views.reorder_courses, name='reorder_courses'),
    
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "edusetin_app.views.page_404"
