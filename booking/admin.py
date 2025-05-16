from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import RoomType, RoomTypeImage, Room, RoomImage, Booking, Review, Gallery, Service, BookingService, ContactRequest

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'capacity')
    search_fields = ('name',)

@admin.register(RoomTypeImage)
class RoomTypeImageAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'image', 'caption')
    list_filter = ('room_type',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('room_number',)

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image', 'caption')
    list_filter = ('room',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price', 'confirm_link')
    list_filter = ('status', 'check_in_date')
    search_fields = ('user__username', 'room__room_number')

    def confirm_link(self, obj):
        if obj.status == 'pending':
            url = reverse('confirm_booking', args=[obj.id])
            return format_html('<a href="{}">Подтвердить</a>', url)
        return '-'
    confirm_link.short_description = 'Действие'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating')
    search_fields = ('user__username', 'comment')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ('booking', 'service', 'quantity')
    list_filter = ('service',)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')