import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Document
from .forms import UploadFileForm, UpdateFileForm


def list(request):
    documents = Document.objects.order_by('-date')
    return render(request, 'documents/list.html', {'documents': documents})

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            document = Document(file = request.FILES['file'], title = request.POST['title'], description = request.POST['description'])
            document.save()
            return HttpResponseRedirect(reverse('documents:detail', args=(document.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'documents/upload.html', {'form': form})

def detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, 'documents/detail.html', {'document': document})

def download(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.file, content_type="application/application")
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(document.file.url)
    return response

def delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return HttpResponseRedirect(reverse('documents:list'))

def update(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        form = UpdateFileForm(request.POST)
        if form.is_valid():
            document.title = request.POST['title']
            document.description = request.POST['description']
            document.save()
            return HttpResponseRedirect(reverse('documents:detail', args=(document.id,)))
    else:
        form = UpdateFileForm(initial={'title': document.title, 'description': document.description})
    return render(request, 'documents/update.html', {'form': form, 'document': document})