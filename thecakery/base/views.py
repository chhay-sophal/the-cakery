from django.shortcuts import render
from cakes.models import Cake, CakeImage

def home_page(request):
    cakes = Cake.objects.all()
    cake_images = CakeImage.objects.all()
    return render(request, "base/homepage.html", {'cakes': cakes, 'cake_images': cake_images})

def about(request):
    return render(request, 'base/about_us.html')

def contact(request):
    return render(request, 'base/contact_us.html')
def catalog(request):
    return render(request, 'base/catalog.html')
