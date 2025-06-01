from django.contrib import admin
from .models import Services, Users, Specialists, Bookings, Reviews, WorkSchedule

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'status', 'display_duration', 'last_booked')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    list_display_links = ('title',)

    @admin.display(description="Длительность")
    def display_duration(self, obj):
        return str(obj.duration)

    @admin.display(description="Последнее бронирование")
    def last_booked(self, obj):
        last_booking = Bookings.objects.filter(service=obj).order_by('-booking_date').first()
        if last_booking:
            return last_booking.booking_date
        return "Нет бронирований"

    def save_model(self, request, obj, form, change):
        last_booking = Bookings.objects.filter(service=obj).order_by('-booking_date').first()
        if last_booking and last_booking.booking_date < timezone.now().date() - timedelta(days=30):
            obj.status = "Неактивна"
        elif not last_booking:
            obj.status = "Неактивна"
        else:
            obj.status = "Активна"
        super().save_model(request, obj, form, change)
    
class BookingInline(admin.TabularInline):
    model = Bookings
    extra = 1 
    fields = ('service', 'booking_date', 'time_slot', 'status')
    raw_id_fields = ('service',)    

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'registration_date')
    list_filter = ('role', 'registration_date')
    search_fields = ('name', 'email')
    date_hierarchy = 'registration_date'
    list_display_links = ('name',)
    inlines = [BookingInline]

@admin.register(Specialists)
class SpecialistsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'experience', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'specialization')
    list_display_links = ('name',)
    filter_horizontal = ('services',)

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'service_id', 'booking_date', 'time_slot', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user_id', 'service_id')
    date_hierarchy = 'booking_date'
    list_display_links = ('id',)
    raw_id_fields = ('user', 'service')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'service_id', 'rating', 'created_at')
    list_filter = ('created_at', 'rating')
    search_fields = ('review_text',)
    date_hierarchy = 'created_at'
    list_display_links = ('id',)
    readonly_fields = ('created_at',)

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialist_id', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('specialist_id',)
    list_display_links = ('id',)