from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util


def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

def show_content(request, title):
	text = util.get_entry(title)
	if text is None:
		return render(request, "encyclopedia/errorpage.html")
	else:
		s_title, content = util.title_separator(text)
		return render(request, "encyclopedia/content.html", {
		"content": content,
		"title": s_title
	})

def search(request):
	if request.method == "GET":
		entries = util.list_entries()
		query = request.GET['q']
		if query.lower() in [entry.lower() for entry in entries]:
			return HttpResponseRedirect(f"/{query}")
		search_results = [entry for entry in entries if query in entry.lower()]
		return render(request, "encyclopedia/search_results.html", {
			"entries": search_results
		})
	return render(request, "encyclopedia/index.html")
	