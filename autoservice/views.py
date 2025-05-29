from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Services, Specialists, WorkSchedule, Bookings
from datetime import date
from django.db.models import Q

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