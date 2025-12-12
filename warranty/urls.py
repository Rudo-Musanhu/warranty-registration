# warranty/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Import all necessary views from your app's views.py file explicitly
from .views import (
    login_view,
    RegisterWarrantyAPIView, 
    logout_view, 
    warranty_list_view
) 

urlpatterns = [
    # --- WEB APPLICATION ROUTES (at root level when included at '') ---
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('warranty_list/', warranty_list_view, name='warranty_list'),
    
    # --- API ROUTES (at /api/warranty/ level) ---
    path('login/', TokenObtainPairView.as_view(), name='api_login'), 
    path('register/', RegisterWarrantyAPIView.as_view(), name='register_warranty'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]