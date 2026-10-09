from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Region
# Create your views here.

# step 2. 
@login_required
def index(req):
    regions = []
    for region in Region.objects.all():
        top = region.regionaltrend_set.order_by('-score')[:5]
        regions.append({
            'name': region.name,
            'lat': region.latitude,
            'lng': region.longitude,
            'movies': [t.movie.name for t in top],
        })
    return render(req, 'index.html', {'regions': regions})