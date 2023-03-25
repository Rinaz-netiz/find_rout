from django import forms
from find_route.cities.models import City
from find_route.routes.models import Route
from find_route.trains.models import Train


class RouteForm(forms.Form):
    """Класс сравнивает полученные данные"""
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={
                                           'class': 'form-control js-example-basic-single'
                                       }))  # для Foreign Key, позволяет выбирать из списка
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control js-example-basic-single'
                                     }))  # для Foreign Key, позволяет выбирать из списка
    cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(),
                                            required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'}))
    travelling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Время в пути'
    }))


class RouteModelForm(forms.ModelForm):
    """Форма для загрузки данных в модель"""
    name = forms.CharField(
        label='Название маршрута',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Типы полей в html <input/> теге
            'placeholder': 'Введите название маршрута'
        }))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    trains = forms.ModelMultipleChoiceField(
        label='Через города', queryset=Train.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control d-none'}))  # d-none не отображать
    travel_times = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = '__all__'
