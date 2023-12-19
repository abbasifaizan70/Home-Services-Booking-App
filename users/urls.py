from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as views

urlpatterns = [
  path("accounts/", include("django.contrib.auth.urls")),
  path('signup/', views.signup, name='signup'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('login/', views.custom_login, name='custom_login'),
]