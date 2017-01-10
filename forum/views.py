from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from forum.models import *
from django.views.generic import ListView,DetailView
from django.core.paginator import *
from django.urls import reverse

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
    threads = Thread.objects.filter(forum=pk).order_by("time")
    threads = make_paginator(request,threads,15)
    return render(request, 'forum/thread_list.html', {"subforum" : threads, "pk" : pk})


def thread(request,pk=1):
    posts = Post.objects.filter(thread=pk).order_by("time")
    posts = make_paginator(request,posts,15)
    title = Thread.objects.get(id=pk).title
    return render(request, 'forum/post_list.html', {"posts" : posts, "pk" : pk, "title" : title})

def postForm(request,ptype,id=1):
    if ptype == "new_thread":
        title = "Start new Topic"
        subject = ""
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(id=id).title
    return render(request, "forum/post.html", {"title" : title , "subject" : subject, "action":reverse(ptype, kwargs={'id':id})})

def new_thread(request,id):
    p = request.POST
    if p["body"]:
        forum = Forum.objects.get(id=id)
        thread = Thread.objects.create(forum=forum,title=p["subject"],created_by = request.user)
        Post.objects.create(thread=thread,title=p["subject"],body = p["body"],created_by = request.user)
    return HttpResponseRedirect(reverse('subforum',kwargs={'pk':id}))

def reply(request,id):
    print("Vstavljam vrednosti v tabelo2\n")

    p = request.POST
    if p["body"]:
        thread = Thread.objects.get(id=id)
        Post.objects.create(thread=thread,title=p["subject"],body = p["body"],created_by = request.user)
    return HttpResponseRedirect(reverse('thread',kwargs={'pk':id}))