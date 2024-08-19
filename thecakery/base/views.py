from django.shortcuts import render
from cakes.models import Cake, CakeImage, Flavour
from party_accessories.models import PartyAccessory
from django.db.models import Q

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
    query = request.GET.get('q')
    cakes = Cake.objects.prefetch_related('trending_entries__trend_type', 'images')

    if query:
        cakes = cakes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(flavours__name__icontains=query)
        ).distinct()

    user = request.user

    context = {
        'cakes': cakes,
        'user': user,
        'query': query,  # Pass the query to the template to display in the search form
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
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        accessories = PartyAccessory.objects.filter(name__icontains=query)
    else:
        accessories = PartyAccessory.objects.all()
    
    return render(request, 'base/accessory.html', {'accessories': accessories, 'query': query})
