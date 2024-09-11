

# Create your views here.

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile
import pandas as pd
from django.conf import settings
import os




def upload_files(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')

        # Collect a list of filenames already uploaded to avoid duplicates
        existing_files = set(os.path.basename(upload.file.name) for upload in UploadedFile.objects.all())

        if form.is_valid():
            for f in files:
                # Check if the file is already uploaded by comparing the file name
                if f.name in existing_files:
                    continue  # Skip the file if it is already uploaded

                try:
                    # Process the file based on its extension
                    if f.name.endswith('.csv'):
                        # Read CSV files with more robust error handling
                        file_data = pd.read_csv(f, on_bad_lines='warn', engine='python')
                    elif f.name.endswith('.xls') or f.name.endswith('.xlsx'):
                        file_data = pd.read_excel(f, engine='openpyxl')
                    else:
                        # Handle unsupported file formats
                        continue

                    # Save the uploaded file info in the model
                    UploadedFile.objects.create(
                        merchant_name=form.cleaned_data['merchant_name'],
                        bank_name=form.cleaned_data['bank_name'],
                        txn_type=form.cleaned_data['txn_type'],
                        file=f
                    )
                    
                    # Optionally: Convert non-CSV files to CSV and save them
                    if not f.name.endswith('.csv'):
                        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'converted', f'{os.path.splitext(f.name)[0]}.csv')
                        file_data.to_csv(csv_file_path, index=False)

                except pd.errors.ParserError as e:
                    print(f"Error parsing file {f.name}: {e}")
                    # Optionally: Log the error or notify the user
                except Exception as e:
                    print(f"An unexpected error occurred with file {f.name}: {e}")
                    # Optionally: Handle other exceptions

            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    files = UploadedFile.objects.all()
    return render(request, 'upload_success.html', {'files': files})

def delete_files(request):
    if request.method == 'POST':
        # If specific files are selected for deletion
        files_to_delete = request.POST.getlist('files_to_delete')

        if files_to_delete:
            # Loop through the selected files and delete only the database record
            for file_id in files_to_delete:
                file = UploadedFile.objects.get(id=file_id)
                file.delete()  # This deletes the record from the database only

        # If 'delete_all' button is clicked, delete all file records from the database
        if 'delete_all' in request.POST:
            UploadedFile.objects.all().delete()

        return redirect('upload_success')

    # Render success page with uploaded files if method is GET
    files = UploadedFile.objects.all()
    return render(request, 'upload_success.html', {'files': files})

# def upload_files(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         files = request.FILES.getlist('file')

#         # Collect a list of filenames already uploaded to avoid duplicates
#         existing_files = set(os.path.basename(upload.file.name) for upload in UploadedFile.objects.all())

#         if form.is_valid():
#             for f in files:
#                 # Check if the file is already uploaded by comparing the file name
#                 if f.name in existing_files:
#                     continue  # Skip the file if it is already uploaded

#                 try:
#                     # Process the file based on its extension
#                     if f.name.endswith('.csv'):
#                         # Read CSV files with more robust error handling
#                         file_data = pd.read_csv(f, on_bad_lines='warn', engine='python')
#                     elif f.name.endswith('.xls') or f.name.endswith('.xlsx'):
#                         file_data = pd.read_excel(f, engine='openpyxl')
#                     else:
#                         # Handle unsupported file formats
#                         continue

#                     # Save the uploaded file info in the model
#                     UploadedFile.objects.create(
#                         merchant_name=form.cleaned_data['merchant_name'],
#                         bank_name=form.cleaned_data['bank_name'],
#                         txn_type=form.cleaned_data['txn_type'],
#                         file=f
#                     )
                    
#                     # Optionally: Convert non-CSV files to CSV and save them
#                     if not f.name.endswith('.csv'):
#                         csv_file_path = os.path.join(settings.MEDIA_ROOT, 'converted', f'{os.path.splitext(f.name)[0]}.csv')
#                         file_data.to_csv(csv_file_path, index=False)

#                 except pd.errors.ParserError as e:
#                     print(f"Error parsing file {f.name}: {e}")
#                     # Optionally: Log the error or notify the user
#                 except Exception as e:
#                     print(f"An unexpected error occurred with file {f.name}: {e}")
#                     # Optionally: Handle other exceptions

#             return redirect('upload_success')
#     else:
#         form = FileUploadForm()
#     return render(request, 'upload.html', {'form': form})

# def upload_success(request):
#     files = UploadedFile.objects.all()
#     return render(request, 'upload_success.html', {'files': files})


# def delete_files(request):
#     if request.method == 'POST':
#         # If specific files are selected for deletion
#         files_to_delete = request.POST.getlist('files_to_delete')

#         if files_to_delete:
#             # Loop through the selected files and delete only the database record
#             for file_id in files_to_delete:
#                 file = UploadedFile.objects.get(id=file_id)
#                 file.delete()  # This deletes the record from the database only

#         # If 'delete_all' button is clicked, delete all file records from the database
#         if 'delete_all' in request.POST:
#             UploadedFile.objects.all().delete()

#         return redirect('upload_success')

#     # Render success page with uploaded files if method is GET
#     files = UploadedFile.objects.all()
#     return render(request, 'upload_success.html', {'files': files})

# # def delete_files(request):
# #     if request.method == 'POST':
# #         action = request.POST.get('action')
        
# #         if action == 'delete_all':
# #             # Delete all files
# #             UploadedFile.objects.all().delete()
# #         elif action == 'delete_selected':
# #             # Delete selected files
# #             file_ids_to_delete = request.POST.getlist('files_to_delete')
# #             for file_id in file_ids_to_delete:
# #                 try:
# #                     file_obj = UploadedFile.objects.get(id=file_id)
# #                     file_obj.file.delete(save=False)  # Delete the file from the file system
# #                     file_obj.delete()  # Delete the record from the database
# #                 except UploadedFile.DoesNotExist:
# #                     continue

# #         return redirect('upload_success')

# #     return redirect('upload_success')  # Redirect if not a POST request


# def upload_success(request):
#     files = UploadedFile.objects.all()
#     return render(request, 'upload_success.html', {'files': files})
