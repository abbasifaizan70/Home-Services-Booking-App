# views.py
from django.shortcuts import render, redirect
from django.core.cache import cache
import datetime
from .forms import SignUpForm
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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
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
            return HttpResponse('Please confirm your email address to complete the registration')
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
        return HttpResponse('Email confirmed, you can now login')
    else:
        return HttpResponse('Activation link is invalid!')
      
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Lockout key and failed attempts key
        lockout_key = f'lockout_{email}'
        attempts_key = f'attempts_{email}'

        # Check for lockout
        lockout_time = cache.get(lockout_key)
        if lockout_time and timezone.now() < lockout_time:
            time_remaining = (lockout_time - timezone.now()).total_seconds()
            return HttpResponse(f'Account locked. Try again in {int(time_remaining)} seconds.')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.email_confirmed:
            login(request, user)
            # Reset the failed attempts counter and lockout key
            cache.delete(attempts_key)
            cache.delete(lockout_key)
            return redirect('signup')  # Redirect to the desired page
        else:
            # Increment failed attempts
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, timeout=60)  # Store count for 5 minutes

            if attempts >= 1:
                # Lock the account for 5 minutes
                lockout_until = timezone.now() + datetime.timedelta(minutes=1)
                cache.set(lockout_key, lockout_until, timeout=60)
                cache.delete(attempts_key)  # Reset attempts after lockout
                return HttpResponse('Too many failed login attempts. Account locked for 5 minutes.')

            return HttpResponse('Invalid login')

    else:
        return render(request, 'registration/login.html')
