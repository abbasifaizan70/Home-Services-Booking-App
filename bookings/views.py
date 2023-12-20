from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.views import custom_login
from .models import Service, Booking
from django.urls import reverse
from .forms import BookingForm, ReviewForm
import stripe
from .models import Review
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from users.decorators import customer_required

@login_required
@customer_required
def book_service(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'book_service.html', {'form': form, 'service': service})

def booking_success(request):
    return render(request, 'booking_success.html')

@login_required
@customer_required
def add_review(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.service = service
            review.save()
            return redirect('review_success')
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'service': service})

@login_required
@customer_required
def review_success(request):
    return render(request, 'review_success.html')

@login_required
@customer_required
def create_checkout_session(request, service_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY  
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_date = data['booking_date']
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "pkr",
                        "unit_amount": int(100) * 100,
                        "product_data": {
                            "name": 'Name',
                        },
                    },
                    "quantity": 3,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('payment_success', args=[service_id])) + f"?booking_date={booking_date}",
            # cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        return JsonResponse({'id': checkout_session.id})

@login_required
@customer_required
def payment_success(request, service_id):
    booking_date = datetime.strptime(request.GET.get('booking_date'), '%m/%d/%Y')
    Booking.objects.create(customer=request.user, service_id=service_id, booking_date=booking_date)
    messages.add_message(request, messages.SUCCESS, "Booking has been done successfully!")
    return redirect('booking_list')

@login_required
@customer_required
def booking_list(request):
    status_filter = request.GET.get('status')
    user_bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
    if status_filter:
        user_bookings = user_bookings.filter(status=status_filter)
    return render(request, 'booking_list.html', {'bookings': user_bookings})
  
@login_required
@customer_required
def complete_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id, customer=request.user, status='On Going')
        booking.status = 'Completed'
        booking.save()
        return redirect('booking_list')
    else:
        return redirect('booking_list')

@login_required
@customer_required
def submit_review(request, service_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        Review.objects.create(
            service_id=service_id,
            customer=request.user,
            content=content,
            rating=rating
        )
        messages.add_message(request, messages.SUCCESS, "Review has been added successfully!")
        return redirect('service_reviews', service_id=service_id)
