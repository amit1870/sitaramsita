from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


from accounts.models import Manushya
from utils import helper as hlp


def account_sitaram(request):
    ''' view to say sitaram to application '''
    return render(request, 'accounts/sitaram.html', {})


@csrf_protect
@require_http_methods(["GET", "POST"])
def account_register(request):
    ''' view to add new user into sitaram application '''

    context = {}

    if request.method == 'POST':
        form_data = request.POST.copy()
        mobile = form_data.get('email_id', '')
        varn = form_data.get('varn', 'SDH')

        if not hlp.verify_mobile(mobile):
            context['message'] = 'check mobile number.'

        if 'message' not in context:
            hexcode = hlp.generate_otp()
            manushya = get_user_model().objects.filter(mobile=mobile).first()

            if not manushya:
                if hlp.send_otp(mobile, hexcode):
                    manushya = Manushya.objects.create(mobile=mobile, varn=varn, hexcode=hexcode)
                    manushya.save()
                    return redirect("accounts:account_activate", manushya.id, mobile)
                else:
                    context['message'] = 'failure !! server error'
            else:
                context['message'] = 'success !! already registered'

    return render(request, 'accounts/register.html', context)



@csrf_protect
@require_http_methods(["GET","POST"])
def account_activate(request, msid, mobile):
    ''' view to activate new user into sitaram application '''

    context = {}


    if request.method == "GET":
        manushya = get_user_model().objects.filter(mobile=mobile).first()
        if manushya and ( manushya.id == msid ):
            context['message'] = 'success !! otp is sent to mobile number.'
            return render(request, 'accounts/password.html', context)
        else:
            context['message'] = "either mobile number or otp not valid."
            return render(request, 'accounts/register.html', context)

    elif request.method == "POST":
        form_data = request.POST.copy()
        hexcode = form_data.get('valid_otp', '')
        password1 = form_data.get('password1', '')
        password2 = form_data.get('password2', '')

        if len(password1) < 4:
            context['message'] = 'failure !! use four plus length password.'
            return render(request, 'accounts/password.html', context)

        elif len(password1) > 3 and password1 != password2:
            context['message'] = 'failure !! password not matching.'
            return render(request, 'accounts/password.html', context)

        manushya = get_user_model().objects.filter(mobile=mobile, hexcode=hexcode).first()
        if manushya:
            manushya.is_active = True
            manushya.set_password(password1)
            manushya.hexcode = ''
            manushya.save()
        else:
            context['message'] = 'failure !! hexcode not valid.'
            return render(request, 'accounts/password.html', context)

        return redirect("accounts:account_login")


@csrf_protect
@require_http_methods(["GET", "POST"])
def account_password(request):
    ''' view to set password for user into sitaram application '''

    context = {}

    if request.method == 'GET':
        return render(request, 'accounts/forgot.html', context)

    form_data = request.POST.copy()
    mobile = form_data.get('email_id', '')

    if not hlp.verify_mobile(mobile):
        context['message'] = 'failure !! check mobile number.'

    if 'message' not in context:
        hexcode = hlp.generate_otp()
        manushya = get_user_model().objects.filter(mobile=mobile).first()

        if manushya:
            if hlp.send_otp(mobile, hexcode):
                manushya.hexcode = hexcode
                manushya.save()
                return redirect("accounts:account_activate", manushya.id, mobile)
            else:
                context['message'] = 'failure !! server error'
                return render(request, 'accounts/forgot.html', context)
        else:
            context['message'] = 'info !! please register here.'
            return render(request, 'accounts/register.html', context)


    return render(request, 'accounts/forgot.html', context)



@csrf_protect
@require_http_methods(["GET", "POST"])
def account_login(request):
    ''' view to login into sitaram application '''

    context = {}

    if request.method == 'GET':
        return render(request, 'accounts/login.html', context)

    form_data = request.POST.copy()
    mobile = form_data.get('email_id','')
    password = form_data.get('password','')
    user = authenticate(request, username=mobile, password=password)

    if user:
        login(request, user)
        return redirect("dukan:view_all_product")

    context['message'] = 'failure !! check email and password'
    return render(request, 'accounts/login.html', context)



@login_required
@require_http_methods(["GET", "POST"])
def account_logout(request):
    ''' view to logout from sitaram application '''

    context = {}

    logout(request)

    if request.method == 'GET':
        return render(request, 'accounts/login.html', context)
