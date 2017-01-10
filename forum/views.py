from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from forum.models import *
from django.views.generic import ListView,DetailView
from django.core.paginator import *
from django.urls import reverse
from django.http import HttpResponseForbidden
from .forms import PostForm,PostEditForm

# Create your views here.

def make_paginator(request,items,num_items):
    paginator = Paginator(items,num_items)
    page = request.GET.get("page")
    try:
        items= paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items



def index(request):
    forumi = Forum.objects.all()
    return render(request, 'forum/forums.html', {"forums" : forumi})
    #return HttpResponse("<h2>HEY</h2>")

def forum(request,pk=1):
    forums = Forum.objects.filter(forum=pk).order_by("-time")
    forums = make_paginator(request,forums,20)
    return render(request, 'forum/forums.html', {"forums" : forums, "pk" : pk})


def subforum(request,pk=1):
    threads = Thread.objects.filter(forum=pk).order_by("-time")
    threads = make_paginator(request,threads,15)
    return render(request, 'forum/thread_list.html', {"subforum" : threads, "pk" : pk})


def thread(request,pk=1):
    posts = Post.objects.filter(thread=pk).order_by("time")
    posts = make_paginator(request,posts,15)
    title = Thread.objects.get(id=pk).title
    return render(request, 'forum/post_list.html', {"posts" : posts, "pk" : pk, "title" : title})

def postForm(request,ptype,id=1):
    body=""
    if ptype == "new_thread":
        title = "Nova Tema"
        subject = ""
    elif ptype == "reply":
        title = "Odgovor"
        subject = "Re: " + Thread.objects.get(id=id).title
    elif ptype == "edit":
        post = Post.objects.get(id=id)
        if request.user ==  post.created_by:
            title = "Uredi"
            subject = post.title
            body = post.body
        else:
            return HttpResponseForbidden()
    return render(request, "forum/post.html", {"title" : title , "subject" : subject, "action":reverse(ptype, kwargs={'id':id}),"body":body,"edit" : ptype=="edit"})

def new_thread(request,id):
    p = request.POST
    form = PostForm(p)
    if form.is_valid():
        if p["body"]:
            forum = Forum.objects.get(id=id)
            thread = Thread.objects.create(forum=forum,title=p["subject"],created_by = request.user)
            Post.objects.create(thread=thread,title=p["subject"],body = p["body"],created_by = request.user)
    else:
        return HttpResponseForbidden()
    return HttpResponseRedirect(reverse('subforum',kwargs={'pk':id}))

def reply(request,id):
    p = request.POST
    form = PostForm(p)
    if form.is_valid():
        if p["body"]:
            thread = Thread.objects.get(id=id)
            Post.objects.create(thread=thread,title=p["subject"],body = p["body"],created_by = request.user)
    else:
        return HttpResponseForbidden()
    return HttpResponseRedirect(reverse('thread',kwargs={'pk':id}))

def edit(request,id):
    form = PostEditForm(request.POST)
    p = request.POST
    if form.is_valid():
        post = Post.objects.get(id=id)
        if request.user ==  post.created_by:
            if p.get("delete",False):
                id = post.thread.id
                print(post.delete())
                if (Post.objects.all().filter(thread = id).count()==0):
                    Thread.objects.get(id=id).delete()
                    return HttpResponseRedirect(reverse('index'))
                return HttpResponseRedirect(reverse('thread', kwargs={'pk': id}))
            else:
                post.title = p["subject"]
                post.body = p["body"]
                post.save()
                return HttpResponseRedirect(reverse('thread', kwargs={'pk': post.thread.id}))
        else:
            return HttpResponseForbidden()
    return HttpResponseForbidden()
