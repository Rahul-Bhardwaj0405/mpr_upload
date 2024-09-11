from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_files, name='upload_files'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('delete_files/', views.delete_files, name='delete_files'),  # Route for file deletion
]
