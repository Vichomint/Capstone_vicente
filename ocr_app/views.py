from django.shortcuts import render
import os
import pytesseract
from pdf2image import convert_from_path
from django.shortcuts import render, redirect
from .models import PDFDocument
from .forms import PDFUploadForm
from django.http import HttpResponse
from django.core.exceptions import ValidationError

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)  #--> convertimos las paginas en imagenesa
    text = ""
    for page in pages:                                 # español
        text += pytesseract.image_to_string(page, lang='spa') + "\n\n" # ---> utilizamos Tesseract 
    return text

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES) #---> tomamos el archivo
        if form.is_valid():
            try:
                pdf_doc = form.save() #---> guardamos el documento
                pdf_path = pdf_doc.file.path #-----> tomamos la ruta
                
                if not pdf_path.lower().endswith('.pdf'):
                    raise ValidationError("Solo se permiten archivos PDF") #---> solo admite PDF
                
                extracted_text = extract_text_from_pdf(pdf_path) #--- ejecutamos la funcion para extraer el texto proporcionando el path del archivo
                pdf_doc.extracted_text = extracted_text # ---> lo guardamos 
                pdf_doc.save()
                
                return redirect('pdf_detail', pk=pdf_doc.pk)
            
            except Exception as e:
                form.add_error(None, f"Error procesando PDF: {str(e)}") # --> manejo de errores
    
    else:
        form = PDFUploadForm()
    
    return render(request, 'ocr_app/upload.html', {'form': form})

def pdf_detail(request, pk):
    pdf_doc = PDFDocument.objects.get(pk=pk)
    return render(request, 'ocr_app/detail.html', {'pdf_doc': pdf_doc}) #--> realizamos a un request a la vista de detail para ver el boton de descarga

def download_text(render, pk):
    pdf_doc = PDFDocument.objects.get(pk=pk)
 

    original_filename = os.path.splitext(os.path.basename(pdf_doc.file.name))[0]
    safe_filename = original_filename.replace(" ", "_") 
    
    response = HttpResponse(pdf_doc.extracted_text, content_type='text/plain')                 #----> creacion de la respeusta
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}_extracted.txt"'
    
    return response

