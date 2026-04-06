from django.contrib import admin
from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'current_product', 'current_intent', 'updated_at')
    list_filter = ('current_product', 'current_intent')
    search_fields = ('lead__name', 'current_product__name', 'current_intent')
