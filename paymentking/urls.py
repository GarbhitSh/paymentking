# payment_gateway_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('businesses.urls')),
    path('transactions/', include('transactions.urls')),
]
