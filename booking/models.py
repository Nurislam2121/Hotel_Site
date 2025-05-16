from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название типа номера")
    description = models.TextField(verbose_name="Описание")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена за ночь")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    image = models.ImageField(upload_to='room_types/', blank=True, null=True, verbose_name="Изображение типа номера")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"

class RoomTypeImage(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='type_images', verbose_name="Тип номера")
    image = models.ImageField(upload_to='room_type_images/', verbose_name="Изображение")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Подпись")

    def __str__(self):
        return f"Изображение для {self.room_type.name}"

    class Meta:
        verbose_name = "Изображение типа номера"
        verbose_name_plural = "Изображения типов номеров"

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="Тип номера")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    description = models.TextField(verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name="Изображение номера")

    def __str__(self):
        return f"Номер {self.room_number} ({self.room_type.name})"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images', verbose_name="Номер")
    image = models.ImageField(upload_to='room_images/', verbose_name="Изображение")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Подпись")

    def __str__(self):
        return f"Изображение для {self.room.room_number}"

    class Meta:
        verbose_name = "Изображение номера"
        verbose_name_plural = "Изображения номеров"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Номер")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    check_out_date = models.DateField(verbose_name="Дата выезда")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    guest_count = models.PositiveIntegerField(verbose_name="Количество гостей")
    special_requests = models.TextField(blank=True, null=True, verbose_name="Особые пожелания")

    def clean(self):
        if self.check_in_date and self.check_out_date and self.check_in_date >= self.check_out_date:
            raise ValidationError("Дата заезда должна быть раньше даты выезда.")
        if self.guest_count and self.guest_count > 8:
            raise ValidationError("Слишком много гостей. Максимум 8 человек на номер. Пожалуйста, забронируйте 2 или более номера.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронь #{self.id} от {self.user.username} (Номер {self.room.room_number})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Бронирование")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата написания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    def __str__(self):
        return f"Отзыв от {self.user.username} ({self.rating} звезд)"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/', verbose_name="Изображение")
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название")
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Категория")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return self.title or f"Изображение #{self.id}"

    class Meta:
        verbose_name = "Фотогалерея"
        verbose_name_plural = "Фотогалерея"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Бронирование")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.service.name} для брони #{self.booking.id}"

    class Meta:
        verbose_name = "Услуга бронирования"
        verbose_name_plural = "Услуги бронирований"

class ContactRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Запрос от {self.name} ({self.email})"

    class Meta:
        verbose_name = "Запрос на обратную связь"
        verbose_name_plural = "Запросы на обратную связь"