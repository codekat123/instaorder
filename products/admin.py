from django.contrib import admin

from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    readonly_fields = ("link",)
    list_filter = ("is_active",)
    search_fields = ("name",)