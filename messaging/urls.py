from django.urls import path
from .views import (
    meta_webhook
)


urlpatterns = [
    path("webhook/", meta_webhook, name="meta-webhook"),
]