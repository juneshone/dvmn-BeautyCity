from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Pay, Customer
from .utils import get_code


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def serviceFinally(request):
    return render(request, 'serviceFinally.html')


def account(request):
    return render(request, 'account.html')


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
        operation_id = cd.get('operation_id')
        amount = round(float(cd.get('amount')), 2)
        is_success = cd.get('unaccepted') == 'false'
        appointment = 155
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


def send_code(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        customer, created = Customer.objects.get_or_create(phone_number=phone)
        if not created:
            pin = get_code()
            customer.pin = pin
            customer.save()
        pin = customer.pin
        request.session['pin'] = pin
        request.session['phone'] = phone
        return JsonResponse({'pin': pin})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        phone = request.session.get('phone')
        pin = request.session.get('pin')
        if code == pin:
            user = Customer.objects.get(phone_number=phone)
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/account/'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid code'})