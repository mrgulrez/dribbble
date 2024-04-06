from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=25, unique=True, validators=[MinLengthValidator(3)], error_messages={'unique': 'This username is already taken.'}, default='')
    email = models.EmailField(max_length=255, unique=True, error_messages={'unique': 'This email is already taken.'}, default='')
    password = models.CharField(max_length=255, validators=[MinLengthValidator(7)], default='')
    agree_to_terms = models.BooleanField(default=False, error_messages={'required': 'You must agree to the terms.'})
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    location = models.CharField(max_length=255, default='')
    

    def __str__(self):
        return self.username
