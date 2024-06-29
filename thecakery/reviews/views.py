from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Review
from cakes.models import Cake
from party_accessories.models import PartyAccessory
from .forms import ReviewForm

def reviews(request, content_type, object_id):
    model_class = None
    if content_type == 'cake':
        model_class = Cake
    elif content_type == 'accessory':
        model_class = PartyAccessory
    else:
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    content_object = get_object_or_404(model_class, id=object_id)
    reviews = Review.objects.filter(content_type=ContentType.objects.get_for_model(model_class), object_id=object_id)

    reviews_data = []
    for review in reviews:
        review_data = {
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }
        reviews_data.append(review_data)

    if not reviews_data:
        reviews_data.append({'message': f'No reviews for {content_object}.'})

    return JsonResponse(reviews_data, safe=False)

@login_required
def add_cake_review(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.content_type=ContentType.objects.get_for_model(Cake)
            review.object_id=cake_id
            review.user = request.user
            review.save()
            return redirect('reviews', content_type='cake', object_id=cake_id)
    else:
        form = ReviewForm()

    context = {
        'form': form, 
        'cake': cake,
    }

    return render(request, 'reviews/add_reviews.html', context)
    
@login_required
def add_accessory_review(request, accessory_id):
    accessory = get_object_or_404(PartyAccessory, id=accessory_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.content_type=ContentType.objects.get_for_model(PartyAccessory)
            review.object_id=accessory_id
            review.user = request.user
            review.save()
            return redirect('reviews', content_type='accessory', object_id=accessory_id)
    else:
        form = ReviewForm()

    context = {
        'form': form, 
        'accessory': accessory,
    }

    return render(request, 'reviews/add_reviews.html', context)
    