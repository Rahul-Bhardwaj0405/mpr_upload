from django.contrib import admin
from .models import UploadedFile  # Import your models

# Register your models here.


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'merchant_name', 'bank_name', 'txn_type', 'uploaded_at')
    search_fields = ('merchant_name', 'bank_name', 'txn_type')

