from django.db import models


class BookingRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='.')
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    service_requested = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.service_requested} ({self.created_at:%Y-%m-%d})"
