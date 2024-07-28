from django.db import models

class CakeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Flavour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='flavour_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Cake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cake_type = models.ForeignKey(CakeType, related_name='cakes', on_delete=models.CASCADE)
    flavours = models.ManyToManyField(Flavour, related_name='cakes', blank=True)
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

class TrendingType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)  # Optional description for the trend type

    def __str__(self):
        return self.name

class TrendingCake(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='trending_entries')
    trend_type = models.ForeignKey(TrendingType, on_delete=models.CASCADE, related_name='trending_cakes')
    trend_score = models.IntegerField(default=0)  # Score to rank trends
    description = models.TextField(blank=True)  # Description for why this cake is trending
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trend_score', '-created_at']

    def __str__(self):
        return f"{self.cake.name} ({self.trend_type.name})"
