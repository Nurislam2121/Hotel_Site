from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('booking/', views.booking_view, name='booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),  # Новый маршрут
    path('reviews/', views.reviews_view, name='reviews'),
    path('contact/', views.contact_view, name='contact'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('room/<int:pk>/', views.room_info_view, name='room_info'),
]