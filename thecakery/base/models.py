from django.db import models
from django.contrib.auth.models import User

class CakeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Cake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cake_type = models.ForeignKey(CakeType, related_name='cakes', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CakeImage(models.Model):
    cake = models.ForeignKey(Cake, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cake_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.cake.name} Image"
    
class CakeSize(models.Model):
    cake = models.ForeignKey(Cake, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.size} for {self.cake.name}"