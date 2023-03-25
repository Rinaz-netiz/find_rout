from django import forms
from find_route.trains.models import Train
from find_route.cities import City


class TrainForm(forms.ModelForm):
    """Класс сравнивает полученные данные, с данными из бд на уникальность"""
    name = forms.CharField(label='Номер поезда', widget=forms.TextInput(attrs={
        'class': 'form-control',  # Типы полей в html <input/> теге
        'placeholder': 'Введите номер поезда'
    }))
    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Время в пути'
    }))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={
                                           'class': 'form-control',
                                       }))  # для Foreign Key, позволяет выбирать из списка
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control',
                                     }))  # для Foreign Key, позволяет выбирать из списка

    # Привязываем форму к модели
    class Meta:
        model = Train
        fields = '__all__'  # Все поля, присутствующие в данной модели
