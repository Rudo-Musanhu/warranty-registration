# warranty_backend/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib import admin

# Import views for token authentication
from rest_framework_simplejwt.views import (
    # Note: These are now named 'login' and 'token_refresh' in warranty/urls.py
    TokenObtainPairView, 
    TokenRefreshView,
)

# 1. API Root View
@api_view(['GET'])
def custom_api_root(request, format=None):
    # This lists the main entry points for the API
    return Response({
        'api_root': reverse('api_root', request=request, format=format),
        # Assuming we keep top-level JWT paths for DRF browsing:
        'token_obtain_pair': reverse('token_obtain_pair', request=request, format=format),
        'token_refresh': reverse('token_refresh', request=request, format=format),
        
        # Link to the root of your main application API (e.g., /api/warranty/)
        'warranty_api_root': reverse('index', request=request, format=format), 
        
    })

# 2. Router for ViewSets (If any models are registered)
router = DefaultRouter()
# router.register(r'warranties', WarrantyViewSet, basename='warranty')

# 3. Define URL Patterns
urlpatterns = [
    # --- ADMIN PATH ---
    path('admin/', admin.site.urls),
    
    # --- DRF ROOT PATHS ---
    # Defines the root of the entire API structure (e.g., /api/)
    path('api/', custom_api_root, name='api_root'),
    path('api/', include(router.urls)), 

    # --- TOP-LEVEL TOKEN AUTHENTICATION (Optional, for DRF Browsable API) ---
    # These paths are now redundant if the client uses /api/warranty/login/, 
    # but they are kept here to resolve the names 'token_obtain_pair' and 
    # 'token_refresh' that are referenced in custom_api_root.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- WARRANTY APP PATHS ---
    # Include warranty app URLs at the root for web pages and at /api/warranty/ for API
    path('', include('warranty.urls')),
    path('api/warranty/', include('warranty.urls')), 
]