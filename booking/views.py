from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, BookingForm, ReviewForm, ContactRequestForm
from .models import Room, Review, Gallery, Booking

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    gallery_images = Gallery.objects.all()[:3]
    return render(request, 'home.html', {'gallery_images': gallery_images})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_price = booking.room.price_per_night * nights
            booking.save()
            messages.success(request, "Бронирование успешно создано!")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def reviews_view(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв отправлен на модерацию!")
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'reviews.html', {'reviews': reviews, 'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            if request.user.is_authenticated:
                contact_request.user = request.user
            contact_request.save()
            messages.success(request, "Ваш запрос отправлен!")
            return redirect('home')
    else:
        form = ContactRequestForm()
    return render(request, 'contact.html', {'form': form})

def room_list_view(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'room_list.html', {'rooms': rooms})

def room_info_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'room_info.html', {'room': room})