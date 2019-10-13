# ACCOUNTS VIEWS.PY FILE

# from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    # Once signed up, reverse to login when they click submit
    success_url = reverse_lazy('login')

    template_name = 'accounts/signup.html'

# LOGIN/LOGOUT VIEWS PROVIDED BY from django.contrib.auth import views as auth_views IN URLS FILE
