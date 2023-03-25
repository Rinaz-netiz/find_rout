from django.core.exceptions import ValidationError
from django.test import TestCase
from find_route.routes import views as routes_view
from find_route.routes.forms import RouteForm
from find_route.routes.utils import dfs_paths, get_graph
from find_route.cities import views as cities_view

# Create your tests here.
from django.urls import reverse

from find_route.cities.models import City
from find_route.trains.models import Train


class AllTestsCase(TestCase):
    def setUp(self) -> None:  # метод для проверки бд
        self.city_A = City.objects.create(name='A')  # создаем города
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        lst = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5),
            Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4),
        ]

        Train.objects.bulk_create(lst)

    def test_model_city_duplicate(self):  # метод должен начинаться на test, чтобы он вызвался при тестах
        """Тестирование возникновения ошибки при создании дубля города"""
        city = City(name="A")
        with self.assertRaises(ValidationError):  # со встроенным try except, в скобках() - исключение, которое ловим
            city.full_clean()  # на этой строчке код, который будет вызывать ислючение
            # python manage.py test - чтобы вызвать тесты

    def test_model_train_duplicate(self):
        """Тестирование возникновения ошибки при создании дубля поезда"""
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=999)
        with self.assertRaises(ValidationError):  # со встроенным try except, в скобках() - исключение, которое ловим
            train.full_clean()  # на этой строчке код, который будет вызывать ислючение
            # python manage.py test - чтобы вызвать тесты

    def test_model_train_train_duplicate(self):
        """Тестирование возникновения ошибки при создании дубля поезда времени"""
        train = Train(name='t143', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Измените время в пути']}, e.message_dict)  # Проверка raise ошибок
            self.assertIn('Измените время в пути', e.messages)

    def test_home_routes_views(self):
        # client - эмулирование работы браузера
        response = self.client.get(reverse('home'))  # создание дубликата функции home
        self.assertEqual(200, response.status_code)  # проверка на удачный запрос

        # проверка на использование правильного шаблона
        self.assertTemplateUsed(response, template_name='routes/home.html')

        # проверка view функции
        self.assertEqual(response.resolver_match.func, routes_view.home)

    def test_cbv_detail_views(self):
        # client - эмулирование работы браузера
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.id}))
        self.assertEqual(200, response.status_code)  # проверка на удачный запрос

        # проверка на использование правильного шаблона
        self.assertTemplateUsed(response, template_name='cities/detail.html')

        # проверка view функции
        self.assertEqual(response.resolver_match.func.__name__, cities_view.CityDetailView.as_view().__name__)

    def test_find_all_routes(self):
        """Тест utils из routes"""
        qs = Train.objects.all()
        graph = get_graph(qs)
        all_routes = list(dfs_paths(graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_routes), 4)

    def test_valid_route_form(self):
        """Проверка формы на is_valid()"""
        data = {'from_city': self.city_A.id,
                'to_city': self.city_B.id,
                'cities': [self.city_E.id, self.city_D.id],
                'travelling_time': 9}
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_route_form(self):
        """Проверка формы на not is_valid()"""
        data = {'from_city': self.city_A.id,
                'to_city': self.city_B.id,
                'cities': [self.city_E.id, self.city_D.id]}
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_message_error_more_time(self):
        """Првоерка на вызываемую ошибку"""
        data = {'from_city': self.city_A.id,
                'to_city': self.city_E.id,
                'cities': [self.city_C.id],
                'travelling_time': 9}
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Время в пути больше заданного', 1, 200)

    def test_message_error_from_cities(self):
        """Првоерка на вызываемую ошибку"""
        data = {'from_city': self.city_B.id,
                'to_city': self.city_E.id,
                'cities': [self.city_C.id],
                'travelling_time': 349}
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Маршрут через эти города не возможен', 1, 200)


