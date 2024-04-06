from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import UserRegistration

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if email or username already exists
            if UserRegistration.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Email already exists.')
            if UserRegistration.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'Username already exists.')

            if not form.errors:
                # Associate the UserRegistration instance with the current user
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])
                user_registration = form.save(commit=False)
                user_registration.user = user
                user_registration.save()
                return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})
