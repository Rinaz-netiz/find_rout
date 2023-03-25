from django.core.exceptions import ValidationError
from django.db import models
from find_route.cities import City


class Train(models.Model):
    """Модель поезда"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set', verbose_name='Откуда')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='to_city_set',
                                verbose_name='Куда')  # 'trains.City' чтобы предотватить перекрестный импорт

    def __str__(self):
        """Вывод по запросу имени поезда, вместо его id"""
        return f'Поезд №{self.name} из города {self.from_city}'

    class Meta:
        """Изменение отображения в Админке"""
        verbose_name = 'Поезд'  # отображение в ед. числе
        verbose_name_plural = 'Поезда'  # отображение во мн. числе
        ordering = ['travel_time']  # сортировка по именам

    def clean(self):
        """Делаем проверку на одинковость времени в пути одних и тех же городов,
        проверка названий городов"""
        if self.from_city == self.to_city:
            raise ValidationError('Изменить город прибытия')
        qs = Train.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.pk)
        # Train == self.__class__
        """Работает до тех пор, пока создаются новые записи, но с сохранением не работает, 
            поэтому вызывается метод exclude(), что бы он исключал эту запись с определенными параметрами"""
        if qs.exists():  # Если есть хотя бы одна запись
            raise ValidationError('Измените время в пути')

    def save(self, *args, **kwargs):  # метод сохранения данных в бд
        self.clean()  # проверка данных
        super().save(*args, **kwargs)  # вызов стандартного поведения через "super()"


# class TrainTest(models.Model):
#     """Модель поезда (тесты)"""
#     name = models.CharField(max_length=50, unique=True, verbose_name='Номер поезда')
#     from_city = models.ForeignKey(City, on_delete=models.CASCADE,
#                                   related_name='from_city',
#                                   verbose_name='Откуда')
