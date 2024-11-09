from enum import Enum
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET


class Clients:
    clients: list[str] = []

    @staticmethod
    def add_client(client):
        Clients.clients.append(client)

    @staticmethod
    def get_size():
        return len(Clients.clients)


class RoleType(Enum):
    INVESTIGATOR = "investigator"
    LOOKOUT = "lookout"
    SHERIFF = "sheriff"
    POTION_MASTER = "potion_master"
    ESCORT = "escort"
    MEDIUM = "medium"
    DEAD = "dead"


class Role:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def home(request) -> HttpRequest:
    return render(request, "app/home.html")


@require_POST
def add_client(request) -> HttpResponse:
    # get form data
    form = request.POST
    username = form.get("username")
    # store anonymous user
    request.session["username"] = username
    Clients.add_client(username)
    print("Amount of clients: ", len(Clients.clients))
    return HttpResponse(status=200)


@require_GET
def get_clients_size(request):
    return JsonResponse({"clients_size": Clients.get_size()})
