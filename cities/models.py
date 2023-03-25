from django.db import models
from django.urls import reverse


class City(models.Model):
    """Модель города с уникальными названиями"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    def __str__(self):
        """Вывод по запросу имени города, вместо его id"""
        return self.name

    class Meta:
        """Изменение отображения в Админке"""
        verbose_name = 'Город'  # отображение в ед. числе
        verbose_name_plural = 'Города'  # отображение во мн. числе
        ordering = ['name']  # сортировка по именам

    def get_absolute_url(self):  # Функция, для переадресации по умолчанию
        return reverse('trains:detail', kwargs={'pk': self.pk})
