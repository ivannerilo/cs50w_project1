from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
from random import randrange
import markdown2



def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

def show_content(request, title):
	text = util.get_entry(title)
	if text is None:
		return render(request, "encyclopedia/errorpage.html")
	
	return render(request, "encyclopedia/content.html", {
		"mkd_text": markdown2.markdown(text),
		"title": title.lower()
	})

def search(request):
	if request.method == "GET":
		entries = util.list_entries()
		query = request.GET['q']
		if query.lower() in [entry.lower() for entry in entries]:
			return HttpResponseRedirect(f"wiki/{query}")
		search_results = [entry for entry in entries if query in entry.lower()]
		return render(request, "encyclopedia/search_results.html", {
			"entries": search_results
		})
	return render(request, "encyclopedia/index.html")

class newPageForm(forms.Form):
	new_text = forms.CharField(
		widget=forms.Textarea(attrs={'rows':15, 'cols': 50, 'placeholder': "Type here the new page content: "}),
		label="Create a new page here!",
		max_length= 1000
	)

def create(request):
	if request.method == 'POST':
		form = newPageForm(request.POST)
		if form.is_valid():
			title, _ = util.title_separator(form.cleaned_data["new_text"])
			util.save_entry(title, form.cleaned_data["new_text"])
			return HttpResponseRedirect(reverse("encyclopedia:index"))
		return render(request, "encyclopedia/create.html", {
			"form": form
		})
	return render(request, "encyclopedia/create.html", {
		"form": newPageForm()
	})

def edit(request):
	if request.method == 'POST':
		form = newPageForm(request.POST)
		if form.is_valid():
			title, _ = util.title_separator(form.cleaned_data["new_text"])
			util.save_entry(title, form.cleaned_data["new_text"])
			return HttpResponseRedirect(f'wiki/{title}')
		return render(request, 'encyclopedia:edit.html', {
			"form": form
		})
	
	editable_text = util.get_entry(request.GET['e'])
	editForm = newPageForm(initial={'new_text': editable_text})
	return render(request, 'encyclopedia/edit.html', {
		"form": editForm
	})

def random(request):
	entries = util.list_entries()
	random_page = entries[randrange(0, len(entries))]
	return HttpResponseRedirect(f"wiki/{random_page.lower()}")