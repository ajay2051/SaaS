from django.shortcuts import render

from visits.models import PageVisit


def home_page(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    title = "Home Page"
    context = {
        "title": title,
        "qs": qs,
    }
    html_template = 'home.html'
    return render(request, html_template, context)
