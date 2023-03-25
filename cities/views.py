from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from find_route.cities.models import City
from find_route.cities.forms import CityForm

"""Импорт избранных вьюх"""
__all__ = (
    'home',
    'CityDetailView',
    'CityCreateView',
    'CityUpdateView',
    'CityDeleteView',
    'CityListView',
)


def home(request, pk=None):
    """Отображаетв весь список городов или определенного значения"""

    # получение формы в post
    if request.method == 'POST':
        form = CityForm(request.POST)  # Подключение формы и передаем значения
        if form.is_valid():  # Проверка полученных данных, на свопадение с колонками формы
            print(form.cleaned_data)
            form.save()  # Привязанную форму сохраняем

    # if pk:
        """ 
            city = City.objects.get(id=pk) - выпадает в ошибку, если нет такого pk
            
            from django.shortcuts import get_object_or_404 - Выбрасывание ошибки 404
            get_object_or_404(City, id=pk)
         """
        # city = City.objects.filter(id=pk).first()  # не get, потому что поиск по адресной строки выбросит ошибку,
        # если значение не валидно
        # return render(request, 'trains/detail.html', {'object': city})

    form = CityForm()  # дефолтная форма
    qs = City.objects.all()  # Забрать все объекты из бд
    """Пагинация"""
    lst = Paginator(qs, 2)  # 2 Кол-во элемнтов на странице
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    """Вьюшка, похожая на home, но ввиде класса и показывает отдельный город"""
    queryset = City.objects.all()  # Забрать все объекты из бд
    template_name = 'cities/detail.html'  # Шаблон класса


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Вьюшка, для приема и сохранения данных"""
    model = City
    form_class = CityForm  # Использование готовой формы
    template_name = 'cities/home.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект
    success_message = "Город успешно добавлен"  # Сообщении после редактирования города


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Вьюшка, для приема и изменения данных"""
    model = City
    form_class = CityForm  # Использование готовой формы
    template_name = 'cities/update.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект
    success_message = "Город успешно отредактирован"  # Сообщении после редактирования города


class CityDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюшка, для приема и удаления данных"""
    model = City
    template_name = 'cities/delete.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Город успешно удален')  # Сообщение пользователю в классе, где нет страницы подтверждения
        return self.delete(request, *args, **kwargs)


class CityListView(ListView):
    """Главная страница с пагинацией"""
    paginate_by = 2  # Сколько городв показывать на странице
    model = City
    template_name = 'cities/home.html'  # Шаблон класса

    def get_context_data(self, **kwargs):  # метод передачи доп. информации на странцу
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form  # доп. информация
        return context

