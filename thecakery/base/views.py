from django.shortcuts import render, render
from django.urls import path
from cakes.models import Cake, CakeImage

def home_page(request): 
    cakes = Cake.objects.all()
    cake_images = CakeImage.objects.all()

    return render(request, "base/homepage.html", {'cakes': cakes, 'cake_images': cake_images})



