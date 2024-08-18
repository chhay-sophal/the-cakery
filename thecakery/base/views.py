from django.shortcuts import render
from cakes.models import Cake, CakeImage, Flavour
from party_accessories.models import PartyAccessory

def home_page(request):
    cakes = Cake.objects.all()
    cake_images = CakeImage.objects.all()
    flavours = Flavour.objects.all()
    context = {
        'cakes': cakes, 
        'cake_images': cake_images,
        'flavours': flavours
    }
    return render(request, "base/homepage.html", context)

def about(request):
    return render(request, 'base/about_us.html')

def contact(request):
    return render(request, 'base/contact_us.html')

def catalog(request):
    cakes = Cake.objects.prefetch_related('trending_entries__trend_type', 'images').all()
    user = request.user

    # Pass cakes and user to the template
    context = {
        'cakes': cakes,
        'user': user,
    }

    return render(request, 'base/catalog.html', context)

def birthday(request):
    return render(request, 'base/birthday.html')

def wedding(request):
    return render(request, 'base/wedding.html')

def anniversary(request):
    return render(request, 'base/anniversary.html')

def celebration(request):
    return render(request, 'base/celebration.html')

def sign_up(request):
    return render(request,'base/signup.html')

def dessert(request):
    return render(request, 'base/dessert.html')

def accessory_list(request):
    accessories = PartyAccessory.objects.all()
    return render(request, 'base/accessory.html', {'accessories': accessories})