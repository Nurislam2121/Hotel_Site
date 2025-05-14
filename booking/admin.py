from django.contrib import admin
from .models import RoomType, Room, Booking, Review, Gallery, Service, BookingService, ContactRequest, RoomImage

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'capacity')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'room_type')
    search_fields = ('room_number',)

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'caption')
    search_fields = ('room__room_number', 'caption')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'status')
    list_filter = ('status', 'check_in_date')
    search_fields = ('user__username', 'room__room_number')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating')
    search_fields = ('user__username', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Одобрить выбранные отзывы"

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ('booking', 'service', 'quantity')
    search_fields = ('booking__id', 'service__name')

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')