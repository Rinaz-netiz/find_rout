from django.urls import path
from find_route.trains.views import *

urlpatterns = [
    # path('', home, name='home'),  # name - позволяет формировать адреса на страницу
    path('', TrainListView.as_view(), name='home'),
    path('create/', TrainCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),  # в адресе будет целое число, и оно будет помещено в переменную pk
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
]
