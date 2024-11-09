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


ROLE_LIMITS = {
    RoleType.INVESTIGATOR: 2,
    RoleType.LOOKOUT: 4,
    RoleType.SHERIFF: 2,
    RoleType.POTION_MASTER: 1,
}


class Player:
    # store map of role to number of players
    ROLE_TO_PLAYERS: dict[RoleType, list[str]] = {
        RoleType.INVESTIGATOR: [],
        RoleType.LOOKOUT: [],
        RoleType.SHERIFF: [],
        RoleType.POTION_MASTER: [],
    }

    def __init__(self, username: str):
        self.username = username
        self.role = None

    def attempt_assign_role(self, role: RoleType):
        if len(Player.ROLE_TO_PLAYERS[role]) >= ROLE_LIMITS[role]:
            return False
        Player.ROLE_TO_PLAYERS[role].append(self.username)
        self.role = role
        return True


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


@require_POST
def attempt_assign_role(request):
    form = request.POST

    username = form.get("username")
    role = form.get("role")

    if not Player.attempt_assign_role(username, role):
        return HttpResponse(status=400)
    return HttpResponse(status=200)


def main(request):
    # Get user
    username = request.session.get("username")

    return render(request, "app/main.html")
