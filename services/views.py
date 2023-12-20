from sre_constants import SUCCESS
from django.shortcuts import render
from .models import Service, Category
from bookings.models import Booking
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from .forms import ServiceForm
from django.contrib.auth.decorators import login_required
from .forms import ResolveCommentsForm 
from django.contrib import messages
from users.decorators import seller_required
import json

def service_list(request):
    sort_order = request.GET.get('sort', 'newest')
    category_id = request.GET.get('category')
    services = Service.objects.all().select_related('category').prefetch_related('adminactions_set')
    if category_id:
        services = services.filter(category_id=category_id)
        
    if not request.user.is_anonymous:
      if request.user.role == 'SELLER':
          services = services.filter(seller=request.user)
          
      if request.user.role == 'CUSTOMER':
          services = services.filter(adminactions__status='Approved')
    
    if request.user.is_anonymous:
          services = services.filter(adminactions__status='Approved')

    if sort_order == 'oldest':
        services = services.order_by('created_at') 
    else:
        services = services.order_by('-created_at') 
    
    paginator = Paginator(services, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'service_list.html', {'page_obj': page_obj, 'categories': categories})

def service_reviews(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    reviews = service.reviews.all()
    return render(request, 'service_reviews.html', {'service': service, 'reviews': reviews})

@login_required
@seller_required
def resolve_comments(request, service_id):
    service = get_object_or_404(Service, pk=service_id, seller=request.user)
    admin_action = service.adminactions_set.first()

    if request.method == 'POST':
        form = ResolveCommentsForm(request.POST)
        if form.is_valid():
            admin_action.status = 'Pending'
            admin_action.response = form.cleaned_data['response']
            admin_action.save()
            return redirect('service_list')
    else:
        form = ResolveCommentsForm(initial={'response': ''})

    return render(request, 'resolve_comments.html', {'form': form, 'service': service})

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    booked_dates = Booking.objects.filter(service=service, status= 'On Going').values_list('booking_date', flat=True)
    booked_dates = [date.strftime('%Y-%m-%d') for date in booked_dates]
    return render(request, 'service_detail.html', {'service': service, 'booked_dates': json.dumps(booked_dates),})

@login_required
@seller_required
def register_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.seller = request.user
            service.save()
            messages.add_message(request, messages.SUCCESS, "Service added successful!") 
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'register_service.html', {'form': form})

