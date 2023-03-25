from django.urls import path
from find_route.cities.views import *

urlpatterns = [
    # path('', home, name='home'),  # name - позволяет формировать адреса на страницу
    path('', CityListView.as_view(), name='home'),
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),  # в адресе будет целое число, и оно будет помещено в переменную pk
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    path('add/', CityCreateView.as_view(), name='create'),
]
