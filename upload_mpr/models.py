from django.db import models

# Create your models here.


class UploadedFile(models.Model):
    merchant_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    txn_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
