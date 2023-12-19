from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('SELLER', 'Seller'),
        ('CUSTOMER', 'Customer')
    ]

    email = models.EmailField(unique=True, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(null=True, blank=True)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='CUSTOMER')
    email_confirmed = models.BooleanField(default=False)
    profile_image = CloudinaryField('image')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'ADMIN'
        super(CustomUser, self).save(*args, **kwargs)
