from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Auction(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', _("Active")
        CLOSED = 'CL', _("Closed")
        SOLD = 'SO', _('Sold')

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='auction')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.get_auction_status_display()}) - ${self.current_price}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.auction.product.name}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} liked {self.product.name}"


class Transaction(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.auction.product.name} for ${self.final_price}"
