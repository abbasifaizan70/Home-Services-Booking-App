from django.urls import path
from services import views as views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('services/new/', views.register_service, name='register_service'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('<int:service_id>/resolve/', views.resolve_comments, name='resolve_comments'),
    path('<int:service_id>/reviews/', views.service_reviews, name='service_reviews'),
]
