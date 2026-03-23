from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messaging/', include('messaging.urls')),
    path('products/', include('products.urls')),
    path('order/', include('order.urls')),
    path('leads/', include('leads.urls')),
]
