from django.db import models


class Route(models.Model):
    """Модель поезда"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название маршрута')
    travel_times = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                  related_name='route_from_city_set',
                                  verbose_name='Откуда')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE,
                                related_name='route_to_city_set',
                                verbose_name='Куда')  # 'trains.City' чтобы предотватить перекрестный импорт
    trains = models.ManyToManyField('trains.Train',
                                    verbose_name='Список поездов')  # Несколько укзаний на внешнюю таблицу

    def __str__(self):
        """Вывод по запросу имени поезда, вместо его id"""
        return f'Маршрут {self.name} из города {self.from_city}'

    class Meta:
        """Изменение отображения в Админке"""
        verbose_name = 'Маршрут'  # отображение в ед. числе
        verbose_name_plural = 'Маршруты'  # отображение во мн. числе
        ordering = ['travel_times']  # сортировка по именам
