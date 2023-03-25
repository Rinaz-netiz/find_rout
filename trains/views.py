from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (DetailView, CreateView, UpdateView, DeleteView, ListView)

from find_route.trains.models import Train
from find_route.trains.forms import TrainForm


"""Импорт избранных вьюх"""
__all__ = (
    'home', 'TrainListView',
    'TrainDetailView',
    'TrainCreateView',
    'TrainUpdateView',
    'TrainDeleteView',
)


def home(request, pk=None):
    """Отображаетв весь список городов или определенного значения"""
    # form = TrainForm()  # дефолтная форма
    qs = Train.objects.all()  # Забрать все объекты из бд
    """Пагинация"""
    lst = Paginator(qs, 2)  # 2 Кол-во элемнтов на странице
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'trains/home.html', context)


class TrainListView(ListView):
    """Главная страница с пагинацией"""
    paginate_by = 5  # Сколько городв показывать на странице
    model = Train
    template_name = 'trains/home.html'  # Шаблон класса


class TrainDetailView(DetailView):
    """Вьюшка, похожая на home, но ввиде класса и показывает отдельный город"""
    queryset = Train.objects.all()  # Забрать все объекты из бд
    template_name = 'trains/detail.html'  # Шаблон класса


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Вьюшка, для приема и сохранения данных"""
    model = Train
    form_class = TrainForm  # Использование готовой формы
    template_name = 'trains/home.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект
    success_message = "Поезд успешно добавлен"  # Сообщении после редактирования города


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Вьюшка, для приема и изменения данных"""
    model = Train
    form_class = TrainForm  # Использование готовой формы
    template_name = 'trains/update.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект
    success_message = "Номер поезда успешно отредактирован"  # Сообщении после редактирования города


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюшка, для приема и удаления данных"""
    model = Train
    template_name = 'trains/delete.html'  # Шаблон класса
    success_url = reverse_lazy('trains:home')  # Адресс, на который нужно будет сделать редирект

    def get(self, request, *args, **kwargs):
        messages.success(request,
                         'Поезд успешно удален')  # Сообщение пользователю в классе, где нет страницы подтверждения
        return self.delete(request, *args, **kwargs)
