from django.db import models
import os

# models.py
class PDFDocument(models.Model):
    name = models.CharField(max_length=255, blank=True)  # Nuevo campo
    file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Genera automáticamente el nombre si no se provee"""
        if not self.name:
            self.name = os.path.splitext(os.path.basename(self.file.name))[0]
        super().save(*args, **kwargs)