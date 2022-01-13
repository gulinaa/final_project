from django.contrib.auth import get_user_model
from django.db import models

from hotel_booking.main.models import Hotel, GuestHouse


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel')
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, related_name='guesthouse')
    notes = models.CharField(max_length=300, blank=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)

