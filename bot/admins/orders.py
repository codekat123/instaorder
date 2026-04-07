from django.contrib import admin
from ..models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'product', 'confirmed_at', 'status', 'created_at')
    list_filter = ('status','created_at')
    search_fields = ('lead__name', 'product__name', 'status')