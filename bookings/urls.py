from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),

    path('booking-success/', views.booking_success, name='booking_success'),
    path('add-review/<int:service_id>/', views.add_review, name='add_review'),
    path('review-success/', views.review_success, name='review_success'),
    path('create-checkout-session/<int:service_id>/', views.create_checkout_session, name='create_checkout_session'), # type: ignore
    path('payment-success/<int:service_id>/', views.payment_success, name='payment_success'), # type: ignore
    path('bookings/complete/<int:booking_id>/',  views.complete_booking, name='complete_booking'),
    path('services/review/<int:service_id>/', views.submit_review, name='submit_review'), # type: ignore
    # path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
