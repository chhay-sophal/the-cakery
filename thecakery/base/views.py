from django.shortcuts import render, render
from cakes.models import Cake, CakeImage

def home_page(request): 
    cakes = Cake.objects.all()
    cake_images = CakeImage.objects.all()
    return render(request, "base/home.html", {'cakes': cakes, 'cake_images': cake_images})