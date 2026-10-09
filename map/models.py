from django.db import models
# STEP 1: models
from movies.models import Movie
# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class RegionalTrend(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default = 0) # this is for views/ purchases

    def __str__(self):
        return f"{self.movie} in {self.region} ({self.score})"