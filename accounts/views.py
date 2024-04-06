from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignupForm, GetStartedForm
from .models import UserRegistration
from django.contrib.auth.decorators import login_required

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
        print('Form checking...')
        print(form.errors)
        if form.is_valid():
            form.save()
            print('Form saved')
            return redirect('home')  # Redirect to the home page after form submission
    else:
        form = GetStartedForm(instance=user_registration)
    
    return render(request, 'get_started.html', {'form': form})





