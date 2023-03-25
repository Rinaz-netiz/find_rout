from typing import Dict

from find_route.trains.models import Train


def dfs_paths(graph, start, goal):
    """Поиск всего набора возможных маршрутов"""
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    """Добавление графов из qs"""
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())  # не делать проверку, есть ли такой ключ или нет
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> Dict:
    """Функция по поиску маршрутов"""
    context = {'form': form}
    # qs = Train.objects.all()
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travel_time = data['travelling_time']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(list(all_ways)):
        # нет ни одного маршрута для данного поиска
        raise ValueError('Маршрута, удовлетворяющего условие не существует')
    if cities:
        # если есть города, через которые нужно проехать
        _cities = [city.id for city in cities]
        right_ways = []
        for route in all_ways:
            if all(city in route for city in _cities):
                right_ways.append(route)
        if not right_ways:
            # когда список маршрутов пуст
            raise ValueError('Маршрут через эти города не возможен')
    else:
        right_ways = all_ways

    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in right_ways:
        tmp = {}
        tmp['trains'] = []
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= travel_time:
            # если общее время в пути, меньше заданного,
            # то добавляем маршрут в общий спсиок
            routes.append(tmp)
    if not routes:
        # если список пуст, то нет таких маршрутов,
        # которые удовлетворяли бы заданными условиям
        raise ValueError('Время в пути больше заданного')
    # Сортировка по времени:
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(r['total_time'] for r in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context
