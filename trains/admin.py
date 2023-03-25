from django.contrib import admin
from .models import Train


class TrainAdmin(admin.ModelAdmin):
    """Класс улучшения страницы /admin/"""
    class Meta:
        model = Train
    list_display = ('name', 'from_city', 'to_city', 'travel_time', )  # наюор атрибутов, отображающихся на сайте
    list_editable = ('travel_time', )  # Поя, которые можно сразу редактировать, не желательно для ForeignKey


admin.site.register(Train, TrainAdmin)
