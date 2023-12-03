# # summarizer_app/urls.py
# from django.urls import path
# from .views import upload_file

# urlpatterns = [
#     path('upload/', upload_file, name='upload_file'),
#     # Add more URL patterns as needed
# ]
# summarizer_app/urls.py
from django.urls import path
from .views import upload_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    # Add more URL patterns as needed
]
