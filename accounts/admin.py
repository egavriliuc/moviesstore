from django.contrib import admin

from django.core.exceptions import PermissionDenied

from django.db.models import Sum

from django.template.response import TemplateResponse

from cart.models import Item
from .models import TopBuyers



# Register your models here.


@admin.register(TopBuyers)
class TopBuyerAdmin(admin.ModelAdmin):
    change_list_template = "accounts/top_buyer.html"
    
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False
    
   
    
    def changelist_view(self, request, extra_context = None):
        if not self.has_view_permission(request):
            raise PermissionDenied
        
        top_buyer = (
            Item.objects.values("order__user_id", "order__user__username").annotate(total_purchased=Sum("quantity"))
            .order_by("-total_purchased", "order__user_id").first()
        )
        
        context = {
            **self.admin_site.each_context(request),
            **(extra_context or {}),
            "opts": self.model._meta,
            "title": "User with the most movies purchased",
            "top_buyer": top_buyer
        }
        
        return TemplateResponse(
            request,
            self.change_list_template,
            context,
        )