from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from find_route.cities.models import City
from find_route.routes.forms import RouteForm, RouteModelForm
from find_route.routes.models import Route
from find_route.routes.utils import get_routes
from find_route.trains.models import Train
from django.contrib.auth.decorators import login_required


# @login_required
def home(request):
    """Домашняя страница с формой"""
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    """Функция для получения данных или вывода ошибки"""
    if request.method == "POST":
        form = RouteForm(request.POST)  # С данными из request.POST
        if form.is_valid():
            try:
                context = get_routes(request, form)  # Получение данных
            except ValueError as er:
                messages.error(request, er)  # Отправка сообщения пользователю об неправильно заполненной форме
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:  # если пользователь ввел руками url в адресной строке
        form = RouteForm()
        messages.error(request, "Нет данных для поиска")
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    """Функция для получения данных или вывода ошибки"""
    if request.method == "POST":
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_list = [int(t) for t in trains if t.isdigit()]  # isdigit() возвращает True , если все символы в
            # строке str являются цифрами и есть хотя бы один символ
            qs = Train.objects.filter(id__in=trains_list).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()  # из qs в dict через метод .in_bulk()
            form = RouteModelForm(  # заполнение формы
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_times': total_time,
                    'trains': qs,
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:  # если пользователь ввел руками url в адресной строке
        messages.error(request, "Невозможно сохранить не существующий маршрут")
        return redirect('home')


def save_route(request):
    """Функция для получения данных или вывода ошибки"""
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('home')
        return render(request, 'routes/create.html', {'form': form})
    else:  # если пользователь ввел руками url в адресной строке
        messages.error(request, "Невозможно сохранить не существующий маршрут")
        return redirect('home')


class RouteListView(ListView):
    """Главная страница с пагинацией"""
    paginate_by = 10  # Сколько городв показывать на странице
    model = Route
    template_name = 'routes/list.html'  # Шаблон класса


class RouteDetailView(DetailView):
    """Вьюшка, похожая на home, но ввиде класса и показывает отдельный город"""
    queryset = Route.objects.all()  # Забрать все объекты из бд
    template_name = 'routes/detail.html'  # Шаблон класса


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    """Вьюшка, для приема и удаления данных"""
    model = Route
    # template_name = 'trains/delete.html'  # Шаблон класса
    success_url = reverse_lazy('home')  # Адресс, на который нужно будет сделать редирект

    def get(self, request, *args, **kwargs):
        messages.success(request,
                         'Маршрут успешно удален')  # Сообщение пользователю в классе, где нет страницы подтверждения
        return self.delete(request, *args, **kwargs)
