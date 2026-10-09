from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .models import Region, RegionalTrend
# Create your views here.

# step 2. 
@login_required
def index(req):
    movies = list(Movie.objects.all())
    regions = []

    for region in Region.objects.all():
        # score
        scores = {
            t.movie_id: t.score
            for t in RegionalTrend.objects.filter(region=region)
        }

        # movies
        movie_list = [ 
            {'name': m.name, 'score': scores.get(m.id, 0)}
            for m in movies
        ]

        # sort highest score
        movie_list.sort(key=lambda m: (-m['score'], m['name']))

        regions.append({
            'name': region.name,
            'lat': region.latitude,
            'lng': region.longitude,
            'movies': movie_list,
        })
    return render(req, 'index.html', {'regions': regions})