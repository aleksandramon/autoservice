from django.contrib import admin
from .models import Services, Users, Specialists, Bookings, Reviews, WorkSchedule

# Админка для Услуги
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'status', 'display_duration')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    date_hierarchy = None  # Нет дат в модели
    list_display_links = ('title',)

    @admin.display(description="Длительность")
    def display_duration(self, obj):
        return str(obj.duration)

# Админка для Пользователи
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'registration_date')
    list_filter = ('role', 'registration_date')
    search_fields = ('name', 'email')
    date_hierarchy = 'registration_date'
    list_display_links = ('name',)

# Админка для Специалисты
@admin.register(Specialists)
class SpecialistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'experience', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'specialization')
    list_display_links = ('name',)

# Админка для Бронирования
@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'service_id', 'booking_date', 'time_slot', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user_id', 'service_id')
    date_hierarchy = 'booking_date'
    list_display_links = ('id',)

# Админка для Отзывы
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'service_id', 'rating', 'created_at')
    list_filter = ('created_at', 'rating')
    search_fields = ('review_text',)
    date_hierarchy = 'created_at'
    list_display_links = ('id',)
    readonly_fields = ('created_at',)

# Админка для Расписание работы
@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialist_id', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('specialist_id',)
    list_display_links = ('id',)