from django.shortcuts import render
from django.http.response import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from random import choice

from . import util


def index(request):
    if request.method == "POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        util.save_entry(title,content)
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def search(request):
    srch=""
    entries = util.list_entries()
    if request.method == "POST":
        srch = request.POST.get("q")
        for entry in entries:
            if srch.upper()==entry.upper():
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))                
    return render(request, "encyclopedia/search.html",{
        "entries": entries,
        "search" : srch
        })

def entry(request,title):
    if request.method == "POST":
        content=request.POST.get("content")
        util.save_entry(title,content)
    return render(request, "encyclopedia/content.html", {
        "content": util.get_entry(title),
        "title": title
    })

def random(request):
    entries=util.list_entries()
    entry=choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))

def create(request):
    return render(request, "encyclopedia/create.html")

def edit(request,title):
    content=util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })