from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def serviceFinally(request):
    return render(request, 'serviceFinally.html')


def account(request):
    return render(request, 'account.html')


def popup(request):
    return render(request, 'popup.html')