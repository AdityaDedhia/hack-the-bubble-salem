from django.urls import path

from .views import home, add_client, get_clients_size, main

app_name = "app"

urlpatterns = [
    path("", home, name="home"),
    path("add_client", add_client, name="add_client"),
    path("get_clients_size", get_clients_size, name="get_clients_size"),
    path("main", main, name="main"),
]
