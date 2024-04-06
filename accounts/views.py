from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignupForm, GetStartedForm
from .models import UserRegistration
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import account_activation_token
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings





User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if email or username already exists
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Email already exists.')
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'Username already exists.')

            if not form.errors:
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])
                user_registration = form.save(commit=False)
                user_registration.user = user
                user_registration.save()
                return redirect('get_started')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def get_started(request):
    user_registration, created = UserRegistration.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = GetStartedForm(request.POST, request.FILES, instance=user_registration)
        print(form.errors)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                profile_picture=form.cleaned_data['profile_picture'],
                                                location=form.cleaned_data['location'])
            form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
            )
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = GetStartedForm(instance=user_registration)
    
    return render(request, 'get_started.html', {'form': form})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activated successfully')
    else:
        return HttpResponse('Activation link is invalid or expired')

