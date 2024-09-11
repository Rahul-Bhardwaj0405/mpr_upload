from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['merchant_name', 'bank_name', 'txn_type', 'file']
        widgets = {
            'merchant_name': forms.Select(choices=[('Merchant 1', 'Merchant 1'), ('Merchant 2', 'Merchant 2')]),
            'bank_name': forms.Select(choices=[('Bank 1', 'Bank 1'), ('Bank 2', 'Bank 2')]),
            'txn_type': forms.Select(choices=[('Credit', 'Credit'), ('Debit', 'Debit')]),
        }
