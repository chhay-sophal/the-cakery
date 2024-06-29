from django.db import models
from django.contrib.auth.models import User

class PartyAccessory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PartyAccessoryImage(models.Model):
    accessory = models.ForeignKey(PartyAccessory, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accessory_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.accessory.name} Image"

class PartyAccessoryReview(models.Model):
    accessory = models.ForeignKey(PartyAccessory, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.accessory.name} by {self.user.username}"
