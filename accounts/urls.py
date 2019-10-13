# ACCOUNTS URLS.PY FILE

from django.urls import path

# Django provides LogIn/LogOut views with this import
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # No logout template connection because Django provides a default view
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    path('signup',views.SignUp.as_view(),name='signup'),
]
