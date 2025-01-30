from django.shortcuts import render
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