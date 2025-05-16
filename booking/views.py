from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, BookingForm, ReviewForm, ContactRequestForm
from .models import Room, RoomType, Review, Gallery, Booking
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Вы вошли в систему.")
            logger.info(f"User {user.username} registered and logged in.")
            return redirect('home')
        else:
            logger.warning(f"Failed registration attempt: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)  # Передаем data для POST-запроса
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            logger.info(f"User {user.username} logged in.")
            return redirect('home')
        else:
            messages.error(request, "Неверный email или пароль.")
            logger.warning(f"Failed login attempt: {form.errors}")
    else:
        form = EmailAuthenticationForm()  # Пустая форма для GET-запроса
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')

@login_required
def home_view(request):
    gallery_images = Gallery.objects.all()[:3]
    return render(request, 'home.html', {'gallery_images': gallery_images})

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

            logger.debug(f"Form data: room_type={room_type}, room_number={room_number}, check_in={check_in_date}, check_out={check_out_date}")

            # Проверка дат
            nights = (check_out_date - check_in_date).days
            if nights <= 0:
                messages.error(request, "Дата выезда должна быть позже даты заезда.")
                logger.warning("Invalid dates: check-out date is not after check-in date.")
                return render(request, 'booking.html', {'form': form})

            if room_number:
                booking.room = form.cleaned_data.get('selected_room')
            else:
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
                logger.debug(f"Available rooms for {room_type}: {list(available_rooms)}")
                if not available_rooms.exists():
                    messages.error(request, "Нет доступных номеров для выбранного типа на эти даты.")
                    logger.warning(f"No available rooms for room_type={room_type} on dates {check_in_date} to {check_out_date}.")
                    return render(request, 'booking.html', {'form': form})
                booking.room = available_rooms.first()

            if not booking.room:
                messages.error(request, "Не удалось выбрать номер. Пожалуйста, попробуйте снова.")
                logger.error("Failed to assign a room during booking.")
                return render(request, 'booking.html', {'form': form})

            booking.total_price = booking.room.price_per_night * nights
            booking.save()
            messages.success(request, f"Бронирование успешно создано! Вам назначен номер {booking.room.room_number}.")
            logger.info(f"Booking created: ID={booking.id}, Room={booking.room.room_number}, User={request.user.username}")
            return redirect('my_bookings')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        if booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Бронирование успешно отменено.')
            logger.info(f"Booking cancelled: ID={booking.id}, User={request.user.username}")
        else:
            messages.error(request, 'Нельзя отменить бронирование с этим статусом.')
            logger.warning(f"Attempt to cancel non-pending booking: ID={booking.id}, Status={booking.status}")
    return redirect('my_bookings')

@staff_member_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, f'Бронирование #{booking.id} успешно подтверждено.')
            logger.info(f"Booking confirmed: ID={booking.id}, Admin={request.user.username}")
        else:
            messages.error(request, 'Нельзя подтвердить бронирование с этим статусом.')
            logger.warning(f"Attempt to confirm non-pending booking: ID={booking.id}, Status={booking.status}")
        return redirect('admin:booking_booking_changelist') 
    return render(request, 'confirm_booking.html', {'booking': booking})

def reviews_view(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Пожалуйста, войдите, чтобы оставить отзыв.")
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв отправлен на модерацию!")
            logger.info(f"Review submitted: User={request.user.username}, Rating={review.rating}")
            return redirect('reviews')
        else:
            logger.warning(f"Review form validation failed: {form.errors}")
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
            logger.info(f"Contact request submitted: Email={contact_request.email}")
            return redirect('home')
        else:
            logger.warning(f"Contact form validation failed: {form.errors}")
    else:
        form = ContactRequestForm()
    return render(request, 'contact.html', {'form': form})

def room_list_view(request):
    room_types = RoomType.objects.all()
    rooms = []
    for room_type in room_types:
        room = Room.objects.filter(room_type=room_type, is_available=True).first()
        if room:
            rooms.append(room)
    logger.debug(f"Rooms displayed on room list: {rooms}")
    return render(request, 'room_list.html', {'rooms': rooms})

def room_info_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    logger.debug(f"Room info accessed: Room ID={pk}")
    return render(request, 'room_info.html', {'room': room})