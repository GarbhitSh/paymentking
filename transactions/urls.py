from django.urls import path
from . import views
from . import api_views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('create/', views.create_transaction, name='create-transaction'),
    path('<str:transaction_id>/', views.transaction_detail, name='transaction-detail'),
    path('callback/', views.upi_callback, name='upi-callback'),
    path('api/process_payment/', api_views.process_payment, name='process-payment'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/generate-qr/', api_views.generate_qr_code_api, name='generate_qr_code_api'),
    path('api-key/', views.api_key_dashboard, name='api_key_dashboard'),
    path('api-key/delete/', views.delete_api_key, name='delete_api_key'),
    path('api/generate-qr/', api_views.generate_qr_code_api, name='generate_qr_code_api'),
    path('transactions-overview/', views.transactions_overview, name='transactions-overview'),  # New route



]
