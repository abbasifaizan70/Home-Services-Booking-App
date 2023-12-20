# views.py
from django.shortcuts import render, redirect
from django.core.cache import cache
import datetime
from .forms import SignUpForm,  CustomUserForm
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from .utils import account_activation_token
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            user.email_user(subject, message)
            messages.add_message(request, messages.ERROR, 'Please confirm your email address to complete the registration')
            return redirect('custom_login')
        else:
            for field, errors in form.errors.items():
                field_name = field.capitalize().replace('_', ' ')
                messages.add_message(request, messages.ERROR, f"{field_name}: {errors[0]}")
                break
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def send_confirmation_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"
    message = render_to_string('registration/account_activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })
    user.email_user(subject, message)
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.is_active = True
        user.save()
        messages.add_message(request, messages.ERROR, 'Email confirmed, you can now login')
        return redirect('custom_login')
    else:
        messages.add_message(request, messages.SUCCESS, "Activation link is invalid! Activate again.")
        return redirect('activate')
      
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        lockout_key = f'lockout_{email}'
        attempts_key = f'attempts_{email}'
        lockout_time = cache.get(lockout_key)
        if lockout_time and timezone.now() < lockout_time:
            time_remaining = (lockout_time - timezone.now()).total_seconds()
            messages.add_message(request, messages.ERROR, f'Account locked. Try again in {int(time_remaining)} seconds.')
            return render(request, 'registration/login.html')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.email_confirmed:
            login(request, user)
            cache.delete(attempts_key)
            cache.delete(lockout_key)
            messages.add_message(request, messages.SUCCESS, f'Login Successfully!')
            return redirect('service_list')
        else:
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, timeout=300)

            if attempts >= 1:
                lockout_until = timezone.now() + datetime.timedelta(minutes=1)
                cache.set(lockout_key, lockout_until, timeout=300)
                cache.delete(attempts_key)
                messages.add_message(request, messages.ERROR, 'Too many failed login attempts. Account locked for 5 minutes.')
                return render(request, 'registration/login.html')
            return HttpResponse('Invalid login')
    else:
        return render(request, 'registration/login.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile Updated!")
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = field.capitalize().replace('_', ' ')
                    messages.add_message(request, messages.ERROR, f"{field_name}: {error}")
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})