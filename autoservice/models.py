from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.DurationField(verbose_name="Длительность")
    status = models.CharField(max_length=50, verbose_name="Статус")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25, verbose_name="Имя")
    email = models.CharField(max_length=25, verbose_name="Электронная почта")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    role = models.CharField(max_length=30, verbose_name="Роль")
    registration_date = models.DateField(verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name

class Specialists(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25, verbose_name="Имя")
    experience = models.CharField(max_length=255, verbose_name="Опыт")
    specialization = models.CharField(max_length=255, verbose_name="Специализация")
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Рейтинг")
    services = models.ManyToManyField(Services, verbose_name="Услуги", blank=True)

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return self.name

class Bookings(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь")  # Заменили user_id
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга")  # Заменили service_id
    booking_date = models.DateField(verbose_name="Дата бронирования")
    time_slot = models.TimeField(verbose_name="Временной слот")
    status = models.CharField(max_length=50, verbose_name="Статус")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование от {self.booking_date} для {self.user.name}"

class Reviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь")  # Заменили user_id
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга")  # Заменили service_id
    review_text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.name} на {self.created_at}"

class WorkSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    specialist = models.ForeignKey(Specialists, on_delete=models.CASCADE, verbose_name="Специалист")  # Заменили specialist_id
    day_of_week = models.CharField(max_length=20, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    time_zone = models.CharField(max_length=50, verbose_name="Часовой пояс")

    class Meta:
        verbose_name = "Расписание работы"
        verbose_name_plural = "Расписания работы"

    def __str__(self):
        return f"Расписание для {self.specialist.name} на {self.day_of_week}"

class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь")
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ('user', 'service')  

    def __str__(self):
        return f"{self.user.name} добавил {self.service.title} в избранное"