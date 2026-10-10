from django.contrib import admin
from .models import Movie, Review, Rating, Statistic
from django.db.models import Count, Sum
from django.shortcuts import render
from cart.models import Item

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Rating)
@admin.register(Statistic)
class StatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/statistics.html"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        most_reviewed = (
            Review.objects.values('movie_id', 'movie__name')
            .annotate(total=Count('id'))
            .order_by('-total', 'movie_id')
            .first()
        )

        most_purchased = (
            Item.objects.values('movie_id', 'movie__name')
            .annotate(total=Sum('quantity'))
            .order_by('-total', 'movie_id')
            .first()
        )

        most_comments = (
            Review.objects.values('user_id', 'user__username')
            .annotate(total=Count('id'))
            .order_by('-total', 'user_id')
            .first()
        )

        top_buyers = (
            Item.objects.values('order__user_id', 'order__user__username')
            .annotate(total=Sum('quantity'))
            .order_by('-total', 'order__user_id')[:5]
        )

        context = self.admin_site.each_context(request)
        context.update({
            'opts': self.model._meta,
            'reviewed_movie': most_reviewed,
            'purchased_movie': most_purchased,
            'user_comments': most_comments,
            'top_buyers': top_buyers,
        })

        return render(request, self.change_list_template, context)
# Register your models here.
