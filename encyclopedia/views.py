from django.shortcuts import render, redirect
from django.http import Http404
from markdown import Markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def show_wiki(request, title):
    markdowner = Markdown()
    current_page = util.get_entry(title)
    if current_page:
        return render(request, 'encyclopedia/show_wiki.html',
                      {'page': markdowner.convert(current_page), 'pageTitle': title})
    else:
        return render(request, 'encyclopedia/none.html')


def search(request):
    if request.method == 'GET':
        title = request.GET.get('q')
        entries = util.list_entries()
        sub_pages = []

        for entry in entries:
            if title.upper() in entry.upper():
                sub_pages.append(entry)

        for entry in entries:
            if title.upper() == entry.upper():
                markdowner = Markdown()
                return render(request, 'encyclopedia/show_wiki.html',
                              {'page': markdowner.convert(util.get_entry(title)), 'pageTitle': title})
            elif sub_pages:
                return render(request, 'encyclopedia/search.html', {'subs': sub_pages})
            else:
                return render(request, 'encyclopedia/none.html')


def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        list_entry = util.list_entries()
        if title not in list_entry:
            util.save_entry(title, content)
            return redirect('index')
        else:
            raise Http404

    return render(request, 'encyclopedia/create.html')


def edit(request, title):
    current_content = util.get_entry(title)
    if request.method == 'POST':
        new_content = request.POST.get('edit')
        util.save_entry(title, new_content)
        return redirect('show', title=title)
    return render(request, 'encyclopedia/edit.html', {'page': current_content})


def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect('show', title=random_title)
