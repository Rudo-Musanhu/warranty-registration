# warranty/views.py

from rest_framework import generics, permissions, status
# Use your project's default authentication settings, usually handled by 
# 'rest_framework.permissions.IsAuthenticated' + JWT setup in settings.py
from rest_framework.response import Response 

# Imports for traditional Web Views (Requirement 4)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 

# --- Import your models and serializers ---
# Assuming these are correct names:
from .models import WarrantyRegistration 
from .serializers import WarrantySerializer 
from django.db.models import F 
# ----------------------------------------


# --- 1. API Endpoint (For Next.js - Requirement 2) ---

class RegisterWarrantyAPIView(generics.CreateAPIView):
    """
    API endpoint for Next.js to register a device. Requires JWT token authentication.
    """
    queryset = WarrantyRegistration.objects.all()
    serializer_class = WarrantySerializer 
    
    # CRITICAL FIX: Rely on global DRF authentication (likely JWT) defined in settings.py
    # and the IsAuthenticated permission.
    # No need for specific authentication_classes unless overriding global settings.
    permission_classes = [permissions.IsAuthenticated] 

    def perform_create(self, serializer):
        # Automatically set the user who registered the warranty (authenticated via JWT)
        serializer.save(registered_by=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        # Requirement 3: Return a specific success result
        return Response(
            {
                "status": "success", 
                "message": "Asset successfully registered for warranty.",
                "asset_status": "Warranty Registered", # Explicitly return the new status
                "warranty_id": serializer.instance.id
            },
            status=status.HTTP_201_CREATED # Use DRF status constant
        )


# --- 2. API Endpoint for Listing (Alternative to Web View) ---
# It is best practice to serve data for the list view (Requirement 4) via API,
# even if the list template rendering is done server-side.

class WarrantyListAPIView(generics.ListAPIView):
    """
    API endpoint to list registered warranties for authenticated users.
    (This view can be used to serve data to the Next.js app or a template)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WarrantySerializer 
    
    def get_queryset(self):
        # Requirement 4: Filter list by user authority (staff sees all, others see only theirs).
        registrations_queryset = WarrantyRegistration.objects.select_related('registered_by').order_by('-registration_date')
        
        if self.request.user.is_staff:
            return registrations_queryset # Staff see all
        
        # Non-staff users only see registrations they performed
        return registrations_queryset.filter(registered_by=self.request.user)


# --- 3. Web App Views (If you must render HTML for Requirement 4) ---
# NOTE: If your frontend is 100% Next.js, these traditional views are redundant.

def login_view(request):
    """Handles user login via form submission."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('warranty_list')  # Redirect to warranty list after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    # If user is already authenticated, redirect to warranty list
    if request.user.is_authenticated:
        return redirect('warranty_list')
    
    return render(request, 'login.html')


def logout_view(request):
    """Handles user logout."""
    logout(request)
    return redirect('login') 


@login_required(login_url='login')
def warranty_list_view(request):
    """
    Traditional Django view to render the list of registered warranties.
    Filters by user authority: staff sees all, others see only theirs.
    """
    if request.user.is_staff:
        registrations = WarrantyRegistration.objects.select_related('registered_by').order_by('-registration_date')
    else:
        registrations = WarrantyRegistration.objects.filter(registered_by=request.user).select_related('registered_by').order_by('-registration_date')
    
    context = {
        'registrations': registrations,
        'page_title': 'Warranty Centre - Registered Assets'
    }
    return render(request, 'warranty/warranty_list.html', context)