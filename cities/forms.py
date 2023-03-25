from django import forms
from find_route.cities.models import City


class HtmlForm(forms.Form):
    """Класс тестовый, для формы"""
    name = forms.CharField(label='Город')


class CityForm(forms.ModelForm):
    """Класс сравнивает полученные данные, с данными из бд на уникальность"""
    name = forms.CharField(label='Город', widget=forms.TextInput(attrs={
        'class': 'form-control',  # Типы полей в html <input/> теге
        'placeholder': 'Введите название города'
    }))

    # Привязываем форму к модели
    class Meta:
        model = City
        fields = ('name', )  # Поля, которые должны быть отражены
