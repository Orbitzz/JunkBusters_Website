from django.contrib.auth.models import User
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=10, blank=True, default='TN')
    zip_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.email
