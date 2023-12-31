from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
path('login/', auth_views.LoginView.as_view(), name='login'),
]
