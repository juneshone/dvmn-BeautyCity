from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

import json

from .models import Pay, Salon, Master, Service, ServiceCategory, Appointment, Address, CustomUser



def index(request):
    return render(request, 'index.html')


def service(request):
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.all().prefetch_related('services')
    masters = Master.objects.all()
    context = {
        'salons': salons,
        'categories': categories,
        'masters': masters,
    }
    return render(request, 'service.html', context)
    return render(request, 'service.html')


def serviceFinally(request):
    return render(request, 'serviceFinally.html')


@login_required
def notes(request):
    """
    Записи
    """
    notes = Appointment.objects.filter(client=request.user,)
    past_notes = notes.filter(date__lt=timezone.now())
    future_notes = notes.filter(date__gte=timezone.now())
    context = {
        'f_notes': future_notes,
        'p_notes': past_notes,
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


        operation_id = cd.get('operation_id')
        amount = round(float(cd.get('amount')), 2)
        is_success = cd.get('unaccepted') == 'false'
        label = str(cd.get('label'))
        if label:
            labels = label.split(':')
            _type = labels[0]
            appointment = int(labels[1])
        else:
            _type = 'service'
            appointment = 100
        Pay.objects.create(
            operation_id=operation_id,
            amount=amount,
            is_success=is_success,
            _type=_type,
            appointment=appointment
        )
    except Exception as e:
        print(e)
        return HttpResponseServerError('Error save pay')
    return JsonResponse({'status': 'ok'})
