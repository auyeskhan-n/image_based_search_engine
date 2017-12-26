from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from main.core.models import Document
from main.core.forms import DocumentForm
from main.core.classify_image import run_inference_on_image, maybe_download_and_extract
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from subprocess import call

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        call("python main/core/classify_image.py --image_file "+
        settings.MEDIA_ROOT+"/"+filename+" >123.out", shell=True)  
        lines = [line.rstrip('\n') for line in open('123.out')]
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url, "result": lines
        }) 
    return render(request, 'core/simple_upload.html')
 
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })