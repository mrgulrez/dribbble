from django.shortcuts import render,  redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from .forms import RegisterForm

# Create your views here.

class UserSignUpView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})
