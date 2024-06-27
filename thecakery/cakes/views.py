from django.shortcuts import render, get_object_or_404
from .models import Cake

def get_cake_detail(request, cake_name):
    cake = get_object_or_404(Cake, name=cake_name)  
    cake_images = cake.images.all()
    cake_sizes = cake.sizes.all()
    cake_reviews = cake.reviews.all()

    context = {
        'cake': cake,
        'cake_images': cake_images,
        'cake_sizes': cake_sizes,
        'cake_reviews': cake_reviews,
    }

    return render(request, 'cakes/cake_detail.html', context)
