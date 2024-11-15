from django.urls import path

from .views import (
    home,
    add_client,
    get_clients_size,
    main,
    attempt_assign_role,
    check_user,
)

app_name = "app"

urlpatterns = [
    path("", home, name="home"),
    path("check_user", check_user, name="check_user"),
    path("add_client", add_client, name="add_client"),
    path("get_clients_size", get_clients_size, name="get_clients_size"),
    path("main", main, name="main"),
    path("attempt_assign_role/<str:role>", attempt_assign_role, name="attempt_assign_role"),
]
