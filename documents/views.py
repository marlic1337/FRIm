import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.decorators import login_required

from .models import Document
from classes.models import Predmet
from User.models import CustomUser
from .forms import UploadFileForm, UpdateFileForm, SearchForm


def list(request, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    documents = None
    query_text = None
    documents = Document.objects.filter(subject__predmet_id=class_id)
    if request.method == 'GET' and 'query' in request.GET.keys():
        form = SearchForm(request.GET)
        if form.is_valid():
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            query_text = request.GET['query']
            query = SearchQuery(query_text)
            documents = documents.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
    else:
        form = SearchForm()
        documents = documents.order_by('-date')
    return render(request, 'documents/list.html', {'documents': documents, 'form': form, 'query_text': query_text, 'class': class_object})

@login_required
def upload(request, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            document = Document(file = request.FILES['file'], title = request.POST['title'], description = request.POST['description'], subject = class_object, owner = request.user)
            document.save()
            return HttpResponseRedirect(reverse('documents:detail', args=(class_object.predmet_id, document.id)))
    else:
        form = UploadFileForm()
    return render(request, 'documents/upload.html', {'form': form, 'class': class_object})

@login_required
def detail(request, document_id, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    document = get_object_or_404(Document, pk=document_id)
    is_owner = False
    if document.owner is not None and request.user.studentId == document.owner.studentId:
        is_owner = True
    return render(request, 'documents/detail.html', {'document': document, 'class': class_object, 'is_owner': is_owner})

#request.user
@login_required
def download(request, document_id, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.file, content_type="application/application")
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(document.file.url)
    return response

@login_required
def delete(request, document_id, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    document = get_object_or_404(Document, pk=document_id)
    if document.owner is not None and request.user.studentId != document.owner.studentId:
        return HttpResponse('Unauthorized', status=401)
    document.delete()
    return HttpResponseRedirect(reverse('documents:list', args=(class_object.predmet_id,)))

@login_required
def update(request, document_id, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    document = get_object_or_404(Document, pk=document_id)
    if document.owner is not None and request.user.studentId != document.owner.studentId:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = UpdateFileForm(request.POST)
        if form.is_valid():
            document.title = request.POST['title']
            document.description = request.POST['description']
            document.save()
            return HttpResponseRedirect(reverse('documents:detail', args=(class_object.predmet_id, document.id)))
    else:
        form = UpdateFileForm(initial={'title': document.title, 'description': document.description})
    return render(request, 'documents/update.html', {'form': form, 'document': document, 'class': class_object})