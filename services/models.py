from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from admin_management.models import AdminActions
from django.db.models import Avg
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
      
class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sample_image = CloudinaryField('image', folder='Service Sample Images')

    def __str__(self):
        return self.title
    
    def calculate_average_rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] # type: ignore
        return average_rating if average_rating is not None else "No ratings yet"



@receiver(post_save, sender=Service)
def create_admin_action(sender, instance, created, **kwargs):
    if created:
        AdminActions.objects.create(service=instance, status='Pending')
