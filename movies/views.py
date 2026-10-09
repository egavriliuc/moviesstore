from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating, Statistic
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from cart.models import Item

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    rating = None
    if request.user.is_authenticated:
        rating = Rating.objects.filter(movie=movie, user=request.user).values_list('rating', flat=True).first()

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['rating'] = rating 
    template_data['positive_ratings'] = rating_percentage(movie, True)
    template_data['negative_ratings'] = rating_percentage(movie, False)
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)

# For rating system: creates or updates a user's rating on a movie
@login_required
def create_rating(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        rate = request.POST.get('rating') == 'True'
        
        rating, created = Rating.objects.get_or_create(
            movie = movie,
            user = request.user,
            defaults={'rating': rate}
        )

        if not created:
            rating.rating = rate
            rating.save()

        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

# helper method to get average rating of a movie
def rating_percentage(movie, rating):
    total = Rating.objects.filter(movie=movie).count()
    subset = Rating.objects.filter(movie=movie, rating=rating).count()
    if (total != 0):
        return subset / total * 100    
    else:
        return 0
    
def statistics(request):
    most_reviewed = Review.objects.values('movie').annotate(
        total=Count('id')
    ).order_by('-total', 'movie').first()

    most_purchased = Item.objects.values('movie').annotate(
        total=Sum('quantity')
    ).order_by('-total', 'movie').first()

    reviewed_movie = (
        Movie.objects.filter(id=most_reviewed['movie']).first()
        if most_reviewed else None
    )

    purchased_movie = (
        Movie.objects.filter(id=most_purchased['movie']).first()
        if most_purchased else None
    )

    stats, _  = Statistic.objects.get_or_create(id=1)
    stats.most_reviewed_movie = reviewed_movie
    stats.most_purchased_movie = purchased_movie
    stats.save()

    return render(request, 'admin/statistics.html', {
        'reviewed_movie': reviewed_movie,
        'purchased_movie': purchased_movie,
    })
