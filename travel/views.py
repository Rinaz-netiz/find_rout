from django.shortcuts import render


def home(request):
    name = 'Bob'
    # from django.http import HttpResponse
    # return HttpResponse('<h1>Hello, Bob!</1>')
    return render(request, 'home.html', {'name': name, 'title': name})


def about(request):
    name = 'About us'
    return render(request, 'about.html', {'name': name, 'title': name})
