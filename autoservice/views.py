from django.shortcuts import render, get_object_or_404
from .models import Services  # Импортируем Services вместо Post

def service_list(request):
    services = Services.objects.all()  # Получаем все услуги
    return render(request, 'autoservice/service_list.html', {'services': services})

def service_detail(request, id):
    service = get_object_or_404(Services, id=id)
    return render(request, 'autoservice/service_detail.html', {'service': service})