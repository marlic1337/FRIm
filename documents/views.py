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

import operator


def index(request):
    subjects = Predmet.objects.all()
    query_text = None
    if request.method == 'GET' and 'query' in request.GET.keys():
        form = SearchForm(request.GET)
        if form.is_valid():
            query_text = request.GET['query']
            for string in query_text.split(" "):
                subjects = subjects.filter(predmet_name__icontains=string)
            #vector = SearchVector('predmet_name', weight='A')
            #query = SearchQuery(query_text)
            #subjects = subjects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
    context = {
        'user': request.user,
        'title': 'FRIm - Datoteke',
        'navbar_active': 'None',
        'subjects': subjects,
        'query_text': query_text,
    }
    return render(request, 'documents/index.html', context)

@login_required
def list(request, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    documents = None
    query_text = None
    documents = Document.objects.filter(subject__predmet_id=class_id)
    if request.method == 'GET' and 'query' in request.GET.keys():
        form = SearchForm(request.GET)
        if form.is_valid():
            query_text = request.GET['query']
            for string in query_text.split(" "):
                documents = documents.filter(title__icontains=string)
            #vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            #query_text = request.GET['query']
            #query = SearchQuery(query_text)
            #documents = documents.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
    else:
        form = SearchForm()
        documents = documents.order_by('-date')
    context = {
        'user': request.user,
        'title': 'FRIm - Datoteke ' + class_object.predmet_name,
        'navbar_active': 'None',
        'class': class_object,
        'query_text': query_text,
        'documents': documents,
        'form': form,
    }
    return render(request, 'documents/list.html', context)

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
    context = {
        'user': request.user,
        'title': 'FRIm - Prenesi datoteko',
        'navbar_active': 'None',
        'class': class_object,
        'form': form,
    }
    return render(request, 'documents/upload.html', context)

@login_required
def detail(request, document_id, class_id):
    class_object = get_object_or_404(Predmet, pk=class_id)
    document = get_object_or_404(Document, pk=document_id)
    is_owner = False
    if document.owner is not None and request.user.studentId == document.owner.studentId:
        is_owner = True
    context = {
        'user': request.user,
        'title': 'FRIm - Datoteka ' + document.title,
        'navbar_active': 'None',
        'class': class_object,
        'document': document,
        'is_owner': is_owner,
    }
    return render(request, 'documents/detail.html', context)

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
    context = {
        'user': request.user,
        'title': 'FRIm - Posodobi datoteko',
        'navbar_active': 'None',
        'class': class_object,
        'document': document,
        'form': form,
    }
    return render(request, 'documents/update.html', context)