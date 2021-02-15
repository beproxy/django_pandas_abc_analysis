from django.urls import include, path
from testdb import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.data_to_csv_view, name='data_to_csv'),
]
