from django.db import models

class Booking(models.Model):
    BILLARD_TYPES = [
        ('russian', 'Русский бильярд'),
        ('american', 'Американский пул'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    billiard_type = models.CharField(max_length=20, choices=BILLARD_TYPES, verbose_name='Тип бильярда')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.surname} - {self.billiard_type}"