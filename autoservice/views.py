from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Services, Specialists, WorkSchedule, Bookings
from datetime import date
from django.db.models import Q
from django.db.models import Avg

def home(request):
    # Популярные услуги (Top-5 по количеству бронирований)
    popular_services = Services.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]

    # Все услуги для выпадающего списка
    all_services = Services.objects.all()

    # Расписание на сегодня
    today = date.today()
    today_schedule = WorkSchedule.objects.filter(
        day_of_week=today.strftime('%A')
    ).select_related('specialist')

    # Поиск специалистов по услуге
    selected_service_id = request.GET.get('service_id')
    specialists = []
    if selected_service_id:
        specialists = Specialists.objects.filter(services__id=selected_service_id)

    return render(request, 'autoservice/home.html', {
        'popular_services': popular_services,
        'all_services': all_services,
        'today_schedule': today_schedule,
        'specialists': specialists,
        'selected_service_id': selected_service_id,
    })

# Поиск услуг
def search_services(request):
    query = request.GET.get('query', '')
    services = Services.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'autoservice/search_results.html', {'services': services, 'query': query})


def book_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    specialists = Specialists.objects.filter(services=service)
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        time_slot = request.POST.get('time_slot')
        booking_date = date.fromisoformat(booking_date)
        time_slot = time.fromisoformat(time_slot)
        # Проверка расписания специалистов
        day_of_week = booking_date.strftime('%A')
        available_specialists = WorkSchedule.objects.filter(
            specialist__in=specialists,
            day_of_week=day_of_week,
            start_time__lte=time_slot,
            end_time__gte=time_slot
        )
        # Проверка существующих бронирований
        existing_bookings = Bookings.objects.filter(
            service=service,
            booking_date=booking_date,
            time_slot=time_slot
        )
        if available_specialists and not existing_bookings:
            # Создать бронирование
            pass

def service_detail(request, id):
    service = get_object_or_404(Services, id=id)
    avg_rating = Reviews.objects.filter(service=service).aggregate(Avg('rating'))['rating__avg']
    return render(request, 'autoservice/service_detail.html', {'service': service, 'avg_rating': avg_rating})