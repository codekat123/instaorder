from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','name','external_id','timestamp')
    search_fields = ('name','external_id')