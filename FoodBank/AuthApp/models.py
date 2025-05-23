from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    username = None  # Use email as the primary identifier
    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = (
        ('DONOR', 'Donor'),
        ('FOODBANK', 'Foodbank'),
        ('RECIPIENT', 'Recipient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Donor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, help_text="County/Town")
    DONOR_TYPE_CHOICES = (
        ('FOOD', 'Food'),
        ('FUNDS', 'Funds'),
        ('OTHERS', 'Others'),
    )
    preferred_donor_type = models.CharField(max_length=10, choices=DONOR_TYPE_CHOICES)
    DONATION_PREFERENCE_CHOICES = (
        ('SUBSISTENCE', 'Subsistence'),
        ('FREE', 'Free'),
    )
    donation_preference = models.CharField(max_length=20, choices=DONATION_PREFERENCE_CHOICES)

    def __str__(self):
        return self.user.email if self.user else self.full_name

class Foodbank(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    foodbank_name = models.CharField(max_length=255, help_text="Charity organization name")
    phone_number = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='foodbank_pictures/', blank=True, null=True, help_text="Upload a picture for the foodbank authority and urgent request")
    accepts_subsistence_donations = models.BooleanField(help_text="Required even at the subsistence will of a donor or not")

    def __str__(self):
        return self.foodbank_name

class Recipient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name_or_organization = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, help_text="Requests & sometimes requests can be @ the liberty of the foodbank based on the donor donations")
    donation_preference_status = models.CharField(max_length=100, default='Pending Foodbank Assessment', help_text="To be auto-converted — food can be donated for free or at a subsistence fee")

    def __str__(self):
        return self.user.email if self.user else self.full_name_or_organization
