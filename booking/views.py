from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, BookingForm, ReviewForm, ContactRequestForm
from .models import Room, RoomType, Review, Gallery, Booking
import random

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
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            room_type = form.cleaned_data['room_type']
            room_number = form.cleaned_data['room_number']

            print(f"Form data: room_type={room_type}, room_number={room_number}, check_in={check_in_date}, check_out={check_out_date}")

            # Если номер указан, он уже проверен в форме
            if room_number:
                booking.room = form.cleaned_data.get('selected_room')
            else:
                # Выбираем случайный доступный номер из указанного типа
                available_rooms = Room.objects.filter(
                    room_type__name__iexact=room_type,
                    is_available=True
                ).exclude(
                    id__in=Booking.objects.filter(
                        status__in=['pending', 'confirmed'],
                        check_in_date__lt=check_out_date,
                        check_out_date__gt=check_in_date
                    ).values_list('room__id', flat=True)
                )
                print(f"Available rooms: {list(available_rooms)}")
                if not available_rooms.exists():
                    messages.error(request, "Нет доступных номеров для выбранного типа на эти даты.")
                    return render(request, 'booking.html', {'form': form})
                booking.room = random.choice(available_rooms)

            # Проверяем, что room установлен
            if not booking.room:
                messages.error(request, "Не удалось выбрать номер. Пожалуйста, попробуйте снова.")
                return render(request, 'booking.html', {'form': form})

            # Рассчитываем стоимость
            nights = (check_out_date - check_in_date).days
            if nights <= 0:
                messages.error(request, "Дата выезда должна быть позже даты заезда.")
                return render(request, 'booking.html', {'form': form})
            booking.total_price = booking.room.price_per_night * nights
            booking.save()
            messages.success(request, f"Бронирование успешно создано! Вам назначен номер {booking.room.room_number}.")
            return redirect('my_bookings')
        else:
            # Если форма невалидна, возвращаем ее с ошибками
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
            print(f"Form errors: {form.errors}")
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
    # Получаем все типы номеров
    room_types = RoomType.objects.all()
    
    # Выбираем по одному номеру для каждого типа
    rooms = []
    for room_type in room_types:
        # Берем первый доступный номер для данного типа
        room = Room.objects.filter(room_type=room_type, is_available=True).first()
        if room:
            rooms.append(room)

    return render(request, 'room_list.html', {'rooms': rooms})

def room_info_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'room_info.html', {'room': room})