from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Services, Specialists, WorkSchedule, Bookings, Reviews
from datetime import date

DAY_OF_WEEK_MAP = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье'
}

def home(request):
    query = request.GET.get('query', '')
    popular_services = Services.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]
    all_services = Services.objects.all()
    today = date.today()
    today_schedule = WorkSchedule.objects.filter(
        day_of_week=today.strftime('%A')
    ).select_related('specialist')
    selected_service_id = request.GET.get('service_id')
    specialists = []
    if selected_service_id:
        specialists = Specialists.objects.filter(services__id=selected_service_id)
    latest_reviews = Reviews.objects.select_related('user', 'service').order_by('-created_at')[:3]
    recommended_specialists = Specialists.objects.filter(
    rating__gt=4.0,
    workschedule__day_of_week=today.strftime('%A')
    ).distinct()
    return render(request, 'autoservice/home.html', {
        'popular_services': popular_services,
        'all_services': all_services,
        'today_schedule': today_schedule,
        'specialists': specialists,
        'selected_service_id': selected_service_id,
        'latest_reviews': latest_reviews,
    })

def search_services(request):
    query = request.GET.get('query', '')
    services = Services.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'autoservice/search_results.html', {'services': services, 'query': query})

def service_list(request):
    services = Services.objects.all()
    return render(request, 'autoservice/service_list.html', {'services': services})

def service_detail(request, id):
    service = get_object_or_404(Services, id=id)
    return render(request, 'autoservice/service_detail.html', {'service': service})