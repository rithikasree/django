from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('register/', register, name='register'),  # Registration page  
    path('submit/', submit, name='submit'),  # Form submission 
    path('login/', login_view, name='login'),  # ✅ Fixed function name 
    path('logout/', logout_view, name='logout'),  # ✅ Fixed function name & added slash
    path('menu/', menu, name='menu'),  
    path('booking/', booking, name='booking'),  
    path('bookings/', booking_list, name='booking_list'),  # List all bookings
    path('bookings/delete/<int:booking_id>/', delete_booking, name='delete_booking'),  # Delete booking
    path('bookings/update/<int:booking_id>/', update_booking, name='update_booking'),  # Update booking
]
