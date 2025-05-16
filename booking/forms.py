from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Booking, Review, ContactRequest, Room

# Форма регистрации (уже есть)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'})
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not User.objects.filter(username=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")

        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("Неправильный email или пароль.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user

class BookingForm(forms.ModelForm):
    ROOM_TYPE_CHOICES = [
        ('', 'Выберите тип номера'),
        ('standard', 'Standard'),
        ('improved', 'Improved'),
        ('lux', 'Lux'),
        ('presidential', 'Presidential'),
    ]
    room_type = forms.ChoiceField(choices=ROOM_TYPE_CHOICES, label="Тип номера", required=True)
    room_number = forms.CharField(
        label="Номер комнаты (оставьте пустым для случайного выбора)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Например, 131'})
    )

    class Meta:
        model = Booking
        fields = ['room_type', 'room_number', 'check_in_date', 'check_out_date', 'guest_count', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'guest_count': forms.NumberInput(attrs={'min': 1}),
            'special_requests': forms.Textarea(attrs={'placeholder': 'Ваши пожелания'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room_type = cleaned_data.get('room_type')
        room_number = cleaned_data.get('room_number')
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        print(f"Cleaning form: room_type={room_type}, room_number={room_number}, check_in={check_in_date}, check_out={check_out_date}")

        if not room_type:
            raise ValidationError("Пожалуйста, выберите тип номера.")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError("Дата заезда должна быть раньше даты выезда.")

        if room_number:
            print(f"Checking room: type={room_type}, number={room_number}")
            room = Room.objects.filter(
                room_type__name__iexact=room_type,
                room_number=room_number,
                is_available=True
            ).first()
            if not room:
                raise ValidationError(f"Номер {room_number} для типа '{room_type}' недоступен или не существует.")
            overlapping_bookings = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed'],
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            )
            if overlapping_bookings.exists():
                raise ValidationError(f"Номер {room_number} уже забронирован на выбранные даты.")
            cleaned_data['selected_room'] = room
        else:
            pass

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'placeholder': 'Ваш отзыв'}),
        }

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение'}),
        }