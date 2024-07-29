from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import PhoneForm, PinForm
from .models import Pay, CustomUser, Service, Address
from .models import Salon, Master, ServiceCategory, Appointment
from .utils import get_code


def service(request):
    if request.method == 'POST':
        if 'phone' in request.POST:
            form = PhoneForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                consent = form.cleaned_data['consent']

                code = get_code()
                customer, created = CustomUser.objects.get_or_create(phone_number=phone, username=phone)
                customer.pin = code
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
                        if user.is_superuser:
                            link = '/account'
                        else:
                            link = '/notes'
                        login(request, user)
                        return JsonResponse({'status': 'success', 'redirect_url': link})
                return JsonResponse({'status': 'success', 'pin': pin})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        phone_form = PhoneForm()
        pin_form = PinForm()
    salons = Salon.objects.all()
    categories = ServiceCategory.objects.all().prefetch_related('services')
    masters = Master.objects.all()
    context = {
        'phone_form': phone_form,
        'pin_form': pin_form,
        'salons': salons,
        'categories': categories,
        'masters': masters,
    }
    return render(request, 'service.html', context)


def serviceFinally(request):
    context = {'appointment': get_object_or_404(Appointment, id=1)}
    if request.method == "POST":
        r = request.POST
        print(request.POST)
        context['salon_choice'] = r.get('salon_choice')
        context['service_choice'] = r.get('service_choice')
        master = get_object_or_404(Master, name=r.get('master_choice'))
        context['master_choice'] = master
        context['address_choice'] = r.get('address_choice')
        context['price_choice'] = r.get('price_choice')
        context['time_choice'] = r.get('time_choice')
        context['date_choice'] = r.get('date_choice')

        return render(request, 'serviceFinally.html', context=context)


def appointment(request):
    if request.method == "POST":
        r = request.POST
        Appointment.objects.create(
            name=get_object_or_404(Service, name=r.get('service_choice')),
            salon=get_object_or_404(Salon, title=r.get('salon_choice')),
            master=get_object_or_404(Master, name=r.get('master_choice')),
            client=get_object_or_404(CustomUser, phone_number=request.user.phone_number),
            date=r.get('date_choice'),
            time=r.get('time_choice'),
        )
    return redirect('notes')


@login_required
def account(request):
    return render(request, 'account.html')


# @login_required
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


def index(request):
    if request.method == 'POST':
        if 'phone' in request.POST:
            form = PhoneForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                consent = form.cleaned_data['consent']

                code = get_code()
                customer, created = CustomUser.objects.get_or_create(phone_number=phone, username=phone)
                customer.pin = code
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
                        if user.is_superuser:
                            link = '/account'
                        else:
                            link = '/notes'
                        login(request, user)
                        return JsonResponse({'status': 'success', 'redirect_url': link})
                return JsonResponse({'status': 'success', 'pin': pin})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        phone_form = PhoneForm()
        pin_form = PinForm()

    masters = Master.objects.all()
    salons = Salon.objects.all()
    services = Service.objects.all()
    addresses = Address.objects.all()

    return render(request, 'index.html', {
        'phone_form': phone_form,
        'pin_form': pin_form,
        'masters': masters,
        'salons': salons,
        'services': services,
        'addresses': addresses,
    })
