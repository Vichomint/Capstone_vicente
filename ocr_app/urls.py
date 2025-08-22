from django.urls import path
from .views import upload_pdf, pdf_detail, download_text

urlpatterns = [
    path('', upload_pdf, name='upload_pdf'),
    path('pdf/<int:pk>/', pdf_detail, name='pdf_detail'),
    path('pdf/<int:pk>/download/', download_text, name='download_text')
]
