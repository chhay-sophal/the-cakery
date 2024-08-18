from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Cake, CakeImage
from reviews.models import Review
from reviews.views import reviews

def get_all_cakes(request): 
    cakes = Cake.objects.all()
    cake_images = CakeImage.objects.all()
    return render(request, "cakes/cakes_page.html", {'cakes': cakes, 'cake_images': cake_images})

def get_cake_detail(request, cake_name):
    cake = get_object_or_404(Cake, name=cake_name)  
    cake_images = cake.images.all()
    cake_sizes = cake.sizes.all()
    cake_content_type = ContentType.objects.get_for_model(Cake)
    reviews = Review.objects.filter(content_type=cake_content_type, object_id=cake.id)

    cake_reviews = []
    for review in reviews:
        review_data = {
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }
        cake_reviews.append(review_data)

    context = {
        'cake': cake,
        'cake_images': cake_images,
        'cake_sizes': cake_sizes,
        'cake_reviews': cake_reviews,
    }

    return render(request, 'cakes/cake_detail.html', context)
def chocolate(request):
    return render(request, 'cakes/cake_detail.html',chocolate)