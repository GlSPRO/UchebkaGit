from django.shortcuts import render, HttpResponse
from django.core.handlers.wsgi import WSGIHandler
# Create your views here.
def first_page(request: WSGIHandler):
#    if request.GET:
    return render(request, 'firstapp/first_page.html')


def second_page(request: WSGIHandler):
    return render(request, 'firstapp/second_page.html')