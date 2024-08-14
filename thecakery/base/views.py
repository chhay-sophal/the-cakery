from django.shortcuts import render
from cakes.models import Cake, CakeImage, Flavour

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

def chocolate(request):
    return render(request, 'base/chocolate.html')

def strawberry(request):
    return render(request, 'base/strawberry.html')

def vanilla(request):
    return render(request, 'base/vanilla.html')

def brownie(request):
    return render(request, 'base/brownie.html')

def sign_up(request):
    return render(request,'base/signup.html')

def dessert(request):
    return render(request, 'base/dessert.html')
