from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from cakes.models import Cake
from .forms import ReviewForm

def cake_reviews(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    reviews = Review.objects.filter(cake=cake)

    reviews_data = []
    for review in reviews:
        review_data = {
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }
        reviews_data.append(review_data)

    if len(reviews_data) == 0:
        reviews_data.append({'message': f'No reviews for {cake.name}.'})

    return JsonResponse(reviews_data, safe=False)

@login_required
def add_review(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cake = cake
            review.user = request.user
            review.save()
            return redirect('cake_reviews', cake_id=cake.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_reviews.html', {'form': form, 'cake': cake})
    