from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json

from .models import Pay


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
    cd = request.POST
    print(cd)
    try:
        operation_id = int(cd.get('operation_id')[0])
        amount = round(float(cd.get('amount')[0]), 2)
        is_success = cd.get('unaccepted')[0] == 'false'
        appointment = int(cd.get('label')[0])
        Pay.objects.create(
            operation_id=operation_id,
            amount=amount,
            is_success=is_success,
            appointment=appointment
        )
    except Exception as e:
        print(e)
        return HttpResponseServerError('Error save pay')
    return JsonResponse({'status': 'ok'})
