from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import PhoneForm, PinForm
from .models import Pay, CustomUser
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


def send_phone(request):
    if request.method == 'POST':
        if 'phone' in request.POST:
            form = PhoneForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                consent = form.cleaned_data['consent']

                code = get_code()
                customer, created = CustomUser.objects.get_or_create(phone_number=phone)
                customer.pin = code
                customer.is_superuser = True
                customer.is_staff = True
                customer.save()

                request.session['verification_code'] = code
                request.session['phone'] = phone

                return JsonResponse({'status': 'success', 'phone': phone, 'code': code})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
        elif 'pin' in request.POST:
            form = PinForm(request.POST)
            if form.is_valid():
                pin = form.cleaned_data['pin']
                saved_code = request.session.get('verification_code')
                phone = request.session.get('phone')
                if pin == saved_code:
                    user = CustomUser.objects.get(phone_number=phone)
                    if user is not None:
                        login(request, user)
                        return JsonResponse({'status': 'success', 'redirect_url': 'account'})
                return JsonResponse({'status': 'success', 'pin': pin})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        phone_form = PhoneForm()
        pin_form = PinForm()
    return render(request, 'index.html',
                  {'phone_form': phone_form, 'pin_form': pin_form})
