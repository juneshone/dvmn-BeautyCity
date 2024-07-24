from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def serviceFinally(request):
    return render(request, 'serviceFinally.html')


# @login_required
def notes(request):
    """
    Записи
    """
    context = {
        'title': 'Записи',
    }
    # context['user'] = request.user
    return render(request,
                  'notes.html',
                  context)


@csrf_exempt
@require_http_methods(['POST'])
def save_pay(request):
    data = request.POST
    print(data)
    return JsonResponse({'status': 'ok'})
