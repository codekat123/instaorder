from django.contrib import admin
from .models import Conversation , Lead , Order , Product


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'current_product', 'current_intent', 'updated_at')
    list_filter = ('current_product', 'current_intent')
    search_fields = ('lead__name', 'current_product__name', 'current_intent')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','name','external_id','timestamp')
    search_fields = ('name','external_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'product', 'confirmed_at', 'status', 'created_at')
    list_filter = ('status','created_at')
    search_fields = ('lead__name', 'product__name', 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)