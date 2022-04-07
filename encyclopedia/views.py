import random
import markdown2 
from importlib.metadata import entry_points
from importlib.resources import contents
from ssl import TLSVersion
from urllib.request import Request
from django.shortcuts import redirect, render

from . import util
from .forms import EntryCreatForm

def index(request):
    q = request.GET.get('q').lower
    entries = util.list_entries()
    
    if q: 
        entries = [ e for e in entries if q in e.lower()]
    if q in entries:
        return redirect('encyclopedia/single_entry', q)

    return render(request, "encyclopedia/index.html", {
         "entries": util.list_entries()
    })

def single_entry(request, title:str):
    content = markdown2.markdown(util.get_entry(title))
    if not content:

         return  render(request,'encyclopedia/error.html', {
                 'title': '404'
                  }) 

    return render(request,"encyclopedia/single_entry.html", {
        "title" : title,
        "content" : content
    })




def create_entry(request):
    form = EntryCreatForm()
   
    if request.method == 'post':
        form = EntryCreatForm(request.POST)
        if form.is_valid():
           title = form.cleaned_data['title']
           if title in util.list_entries():
             return  render(request, 'encyclopedia/error.html', {
                 'title': f'The entry {title} already exists!'
             })

           content = form.cleaned_data['content']
           util.save_entry(title, content)
           return redirect('create_entry')

    return  render(request, 'encyclopedia/create_entry.html', { 
       'form': form,
    })


def edit_entry(request, title:str):
    form = EntryCreatForm(request.GET)
    title = form.cleaned_data['title'] 
    content = form.cleaned_data['content']

    return render(request,"encyclopedia/single_entry.html", {
          "title" : title,
          "content" : content
    
    })

    


def random_entry(request):
   entries = util.list_entries()
   random_choice = random.choice(entries)
   return redirect('single_entry', random_choice
   )