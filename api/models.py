from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

import uuid

class User(AbstractUser):
    '''
    Extending the default model class
    '''
    phone = PhoneNumberField(null=True, blank=True, unique=True)

class Rider(models.Model):
    rider_name = models.CharField(max_length=32, blank=False, null=False)
    rider_motor = models.CharField(max_length=32, blank=False, null=False)
    rider_phone = PhoneNumberField(null=True, blank=True, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    item_name = models.CharField(max_length=32, blank=False, null=False)
    item_description = models.TextField(max_length=300, blank=False, null=False)    
    location_from = models.CharField(max_length=32, blank=False, null=False)
    location_to = models.CharField(max_length=32, blank=False, null=False)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    estimated_cost = models.IntegerField(blank=True, null=True)
    client_review_status = models.BooleanField(default=False)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')

    def __str__(self):
        return self.item_name

class Order(models.Model):
    PLA = "PLACED"
    WAR = "WAREHOUSE"
    REL = "RELEASED"
    TRA = "TRANSIT"
    DEL = "DELIVERED"

    DELIVERY_CHOICES = (
        (PLA, "Order Placed"),
        (WAR, "In the warehouse"),
        (REL, "Released to rider"),
        (TRA, "On transit"),
        (DEL, "Delivered")
    )

    tracking_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_ref = models.CharField(max_length=32, blank=True)
    payment_complete_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default=PLA)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE, related_name='riderorder', blank=True, null=True)
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name='order')


class Invoice(models.Model):
    total_amount = models.IntegerField(blank=True, null=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    amount_due = models.IntegerField(blank=True, null=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='orderinvoice')
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name='quoteinvoice')
